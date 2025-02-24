import socket
from threading import Thread
import sqlite3

# Configuration
MaxConnections = 20
Listening_port = 1729


# Initialize the database (only for setup, not used in threads)
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


initialize_database()  # Ensure the database is set up before starting the server

# Server socket (UDP)
Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Server_Socket.bind(("0.0.0.0", Listening_port))

clients = []


def broadcast(message, sender_addr):
    """Broadcast a message to all clients except the sender."""
    for client in clients:
        if client != sender_addr:
            Server_Socket.sendto(message.encode(), client)


def handle_client():
    """Handles incoming messages from clients."""
    print(f'Server listening on port {Listening_port}')

    while True:
        try:
            # New SQLite connection for this thread
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            # Receive message from any client
            message, client_addr = Server_Socket.recvfrom(1024)
            message = message.decode().strip()

            if client_addr not in clients:
                clients.append(client_addr)
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

            if not message:
                continue  # Skip empty messages

            print(f'[request from {client_addr}] {message}')
            response = "!" + message
            Server_Socket.sendto(response.encode(), client_addr)  # Send response to client

            # Broadcast message to all clients except the sender
            broadcast(f'{client_addr} {message}', sender_addr=client_addr)

            conn.close()  # Close database connection after processing
        except Exception as e:
            print(f'Error: {e}')
            break

    print('Server shutdown.')


if __name__ == "__main__":
    print(f'Server is listening on port {Listening_port}')
    Thread(target=handle_client).start()  # Start the main message handling
