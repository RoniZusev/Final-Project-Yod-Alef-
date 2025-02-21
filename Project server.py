
import time
import socket
from threading import Thread
import sqlite3

MaxConnections = 20
Listening_port = 1729

Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server_Socket.bind(("0.0.0.0", Listening_port))

clients = []

def broadcast(massage, sender):
    for client in clients:
        if client!= sender:
            client.send(massage.encode())

def handle_client(client, addrss):
    print(f'{addrss} connected.')
    clients.append(client)
    try:
        while True:
            message = client.recv(1024).decode()
            if not message:
                break
            print(f'[request from {addrss}] {message}')
            back_request = "\nthe answer is hello: " + message
            client.send(back_request.encode())
            broadcast(f'{addrss} {message}', sender=client)
    except Exception as e:
        print(f'{e}')
    finally:
        print(f'{addrss} disconnected')
        clients.remove(client)
        client.close()

def wait_for_connection():
    while True:
        try:
            print('waiting for connections...')
            client, addr = Server_Socket.accept()
            Thread(target=handle_client, args=(client, addr)).start()
        except Exception as e:
            print(e)
            break
    print('server shutdown.')

if __name__ == "__main__":
    Server_Socket.listen(MaxConnections)
    print(f'server is listening on port {Listening_port}')
    accept_thread = Thread(target=wait_for_connection())
    accept_thread.start()
    accept_thread.join()
    Server_Socket.close()



