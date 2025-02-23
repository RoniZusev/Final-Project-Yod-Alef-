import socket
from threading import Thread

# Configuration
MaxConnections = 20
Listening_port = 1729

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
            # Receive message from any client
            message, client_addr = Server_Socket.recvfrom(1024)
            message = message.decode()

            if client_addr not in clients:
                clients.append(client_addr)
                print(f'{client_addr} added to clients list.')

            if not message:
                continue  # Skip empty messages

            print(f'[request from {client_addr}] {message}')
            response = "\nthe answer is hello: " + message
            Server_Socket.sendto(response.encode(), client_addr)  # Send response to client

            # Broadcast message to all clients except the sender
            broadcast(f'{client_addr} {message}', sender_addr=client_addr)
        except Exception as e:
            print(f'Error: {e}')
            break

    print('Server shutdown.')

if __name__ == "__main__":
    print(f'Server is listening on port {Listening_port}')
    Thread(target=handle_client).start()  # Start the main message handling
