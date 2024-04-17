import socket
import threading
import sys

def receive_messages(sock):
    """ Continuously listens for incoming messages from the server. """
    while True:
        try:
            message = sock.recv(4096).decode('utf-8')
            if message:
                print(f"\nReceived: {message}\n")
            else:
                print("\nServer connection was lost.")
                break
        except Exception as e:
            print(f"\nError receiving message: {e}\n")
            break

def send_messages(client_socket):
    """
    Handles sending messages and group commands to the server.
    """
    while True:
        message = input("Enter command or message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        if message.startswith('/create_group'):
            # Example input: /create_group #myfriends alice bob charlie
            client_socket.send(message.encode('utf-8'))
        elif message.startswith('/join_group') or message.startswith('/leave_group'):
            # Example input: /join_group #myfriends
            client_socket.send(message.encode('utf-8'))
        else:
            # Normal messages or group messages (group messages start with #groupname:)
            recipient, text = message.split(':', 1)
            client_socket.send(f"{recipient}:{text}".encode('utf-8'))

    print("Exiting message sender...")

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = '44.208.27.219'
    server_port = 80

    try:
        client.connect((server_address, server_port))
    except Exception as e:
        print(f"Failed to connect to server {server_address} on port {server_port}: {e}")
        sys.exit(1)

    identifier = input("Enter your identifier: ")
    client.send(identifier.encode('utf-8'))

    print("Connected to the server. You can start sending messages.")
    
    # Start receiving messages in a separate thread
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    # Handle sending messages in the main thread
    send_messages(client)

    # Once send_messages loop is exited, close the connection
    print("\nDisconnecting...")
    client.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
