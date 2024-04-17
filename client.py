import socket
import threading
import os
from dotenv import load_dotenv

load_dotenv()

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(4096).decode('utf-8')
            print(f"\nReceived: {message}\n")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_messages(client_socket):
    """
    Reads messages from the user input and sends them to the server.
    """
    while True:
        message = input("")
        client_socket.send(message.encode('utf-8'))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("About to connect")

client.connect((os.getenv("NLB_DN"), int(os.getenv("NLB_PORT"))))
print("Connection established")


identifier = input("Enter your identifier: ")
client.send(identifier.encode('utf-8'))
        

thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

while True:
    try:
        recipient = input("Enter recipient identifier: ")
        message = input("Enter message: ")
        client.send(f"{recipient}:{message}".encode('utf-8'))
    except KeyboardInterrupt:
        print("\nDisconnecting...")
        break
    except Exception as e:
        print(f"Error sending message: {e}")
        break

client.close()
