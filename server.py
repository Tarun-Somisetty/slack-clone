import socket
import threading

clients = {}  

def handle_client(client_socket):
    try:
        identifier = client_socket.recv(4096).decode('utf-8')
        clients[identifier] = client_socket
        print(f"Client {identifier} connected")

        while True:
            message = client_socket.recv(4096).decode('utf-8')
            if not message:
                break
            
            # Reciever : Message 
            recipient, text = message.split(':', 1)
            if recipient in clients:
                clients[recipient].send(text.encode('utf-8'))
            else:
                client_socket.send(f"Recipient {recipient} not found.".encode('utf-8'))

    except Exception as e:
        print(f"Error with client {identifier}: {e}")

    finally:
        client_socket.close()
        clients.pop(identifier, None)
        print(f"Client {identifier} disconnected")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('34.226.219.185', 80))
server.listen(10)

while True:
    client_socket, _ = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
