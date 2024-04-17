import socket
import threading

clients = {}  # Tracks connected clients
groups = {}   # Tracks groups and their members

def handle_client(client_socket):
    identifier = None
    try:
        # Initial message from client should be the identifier
        identifier = client_socket.recv(4096).decode('utf-8')
        clients[identifier] = client_socket
        print(f"Client {identifier} connected")

        while True:
            message = client_socket.recv(4096).decode('utf-8')
            if not message:
                break
            
            if message.startswith('/'):
                handle_control_message(identifier, message)
                continue

            # Reciever : Message
            recipient, text = message.split(':', 1)
            
            # Handle group message
            if recipient.startswith('#'):
                if recipient in groups:
                    for member in groups[recipient]:
                        if member != identifier:
                            clients[member].send(f"From {identifier}: {text}".encode('utf-8'))
                else:
                    client_socket.send(f"Group {recipient} not found.".encode('utf-8'))
            else:
                # Handle direct message
                if recipient in clients:
                    clients[recipient].send(text.encode('utf-8'))
                else:
                    client_socket.send(f"Recipient {recipient} not found.".encode('utf-8'))

    except Exception as e:
        print(f"Error with client {identifier}: {e}")

    finally:
        if identifier:
            client_socket.close()
            clients.pop(identifier, None)
            # Remove client from all groups
            for group in groups.values():
                if identifier in group:
                    group.remove(identifier)
            print(f"Client {identifier} disconnected")

def handle_control_message(identifier, message):
    args = message.split()
    command = args[0]
    
    if command == '/create_group' and len(args) > 2:
        group_name = args[1]
        members = args[2:]
        if group_name not in groups:
            groups[group_name] = set(members)
            groups[group_name].add(identifier)  # Add creator to the group
            clients[identifier].send(f"Group {group_name} created with members: {', '.join(members)}".encode('utf-8'))
        else:
            clients[identifier].send(f"Group {group_name} already exists.".encode('utf-8'))
    
    elif command == '/join_group' and len(args) == 2:
        group_name = args[1]
        if group_name in groups:
            groups[group_name].add(identifier)
            clients[identifier].send(f"Joined group {group_name}".encode('utf-8'))
        else:
            clients[identifier].send(f"Group {group_name} does not exist.".encode('utf-8'))
    
    elif command == '/leave_group' and len(args) == 2:
        group_name = args[1]
        if group_name in groups and identifier in groups[group_name]:
            groups[group_name].remove(identifier)
            if not groups[group_name]:  # Delete group if empty
                del groups[group_name]
            clients[identifier].send(f"Left group {group_name}".encode('utf-8'))
        else:
            clients[identifier].send(f"Not a member of group {group_name}".encode('utf-8'))

# Setting up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('172.31.37.250', 80))
server.listen(10)

while True:
    client_socket, _ = server.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
