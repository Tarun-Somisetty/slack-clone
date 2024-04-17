import socket
import threading

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
client.connect(('slack-v2-nlb-e41d69097e82d2b0.elb.us-east-1.amazonaws.com', 80))

# client.connect(('chat-nlb-5643809567ab2cde.elb.us-east-2.amazonaws.com', 80))
# client.connect(('34.226.219.185', 80))
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

# import socket
# import threading

# # ALB DNS name
# ALB_DNS_NAME = 'slack-v1-854080905.us-east-1.elb.amazonaws.com'
# SERVER_PORT = 5000  # The port your server is listening on

# def receive_messages(client_socket):
#     """
#     Continuously listens for messages from the server and prints them.
#     """
#     while True:
#         try:
#             message = client_socket.recv(1024).decode('utf-8')
#             print(message)
#         except Exception as e:
#             print(f"Error receiving message: {e}")
#             client_socket.close()
#             break


# def start_client():
#     """
#     Connects to the server through the ALB and starts threads for sending and receiving messages.
#     """
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((ALB_DNS_NAME, SERVER_PORT))

#     # Start a thread for receiving messages
#     receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
#     receive_thread.start()

#     # Start a thread for sending messages
#     send_thread = threading.Thread(target=send_messages, args=(client_socket,))
#     send_thread.start()

# if __name__ == "__main__":
#     start_client()

