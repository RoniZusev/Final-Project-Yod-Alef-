import socket
from threading import Thread
import sqlite3
import pickle

MaxConnections = 20
Listening_port = 1729

def initialize_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('RONI', '1234')")
    conn.commit()
    conn.close()

initialize_database()

Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Server_Socket.bind(("0.0.0.0", Listening_port))

clients = {}

def broadcast_positions():
    """Broadcast all player positions to all clients."""
    if not clients:
        return
    try:
        positions = {}
        for addr, info in clients.items():
            if "id" in info:
                positions[info["id"]] = {
                    "x": info["player_x"],
                    "y": info["player_y"]
                }
        data = pickle.dumps(positions)
        for client in clients:
            Server_Socket.sendto(b"POSITIONS:" + data, client)
    except Exception as e:
        print(f"Broadcast error: {e}")

def handle_client():
    print(f"Server listening on port {Listening_port}")

    while True:
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            message, client_addr = Server_Socket.recvfrom(1024)
            message = message.decode().strip()

            if client_addr not in clients:
                clients[client_addr] = {"player_x": 0.0, "player_y": 0.0}
                print(f'{client_addr} added to clients list.')

            if message.startswith("ATTEMPT:"):
                print("🔑 Login attempt detected")
                message2 = message.replace("ATTEMPT: ", "").strip()
                try:
                    username1, password1 = message2.split(" , ")
                except ValueError:
                    print("❌ Invalid login format")
                    Server_Socket.sendto("failed".encode(), client_addr)
                    continue

                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username1, password1))
                result = cursor.fetchone()

                if result:
                    Server_Socket.sendto("success".encode(), client_addr)
                else:
                    Server_Socket.sendto("failed".encode(), client_addr)

            elif message.startswith("PLAYER_ID:"):
                player_id = message.split(":")[1].strip()
                clients[client_addr]["id"] = player_id
                print(f"{client_addr} set ID to {player_id}")

            elif message.startswith("POSITION:"):
                try:
                    player_data = message.split(":")[1]
                    player_x, player_y = map(float, player_data.split(","))
                    clients[client_addr]["player_x"] = player_x
                    clients[client_addr]["player_y"] = player_y

                    broadcast_positions()
                except Exception as e:
                    print(f"Error processing position update: {e}")

            elif message:
                print(f'[request from {client_addr}] {message}')
                response = "!" + message
                Server_Socket.sendto(response.encode(), client_addr)

            conn.close()

        except Exception as e:
            print(f'Error: {e}')
            break

    print('Server shutdown.')

if __name__ == "__main__":
    print(f"Server is starting on port {Listening_port}...")
    Thread(target=handle_client).start()
