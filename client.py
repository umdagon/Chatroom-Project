"""\
This module is a Client of the chatroom.

Special objects:

In line 54, configure the IP of the server you trying to connect.
"""



import socket
import threading


def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "!exit":
                print("You have successfully disconnected!")
                client_socket.close()
                break
            if message:
                print("\r" + message + "\n> ", end="")
        except Exception as e:
            if WindowsError :
                print(f'Connection closed!')
                client_socket.close()
                break
            else:
                print("Error receiving message: ", e)
                break

def send_message(client_socket):
    while True:
        message = input(f"> ")
        try:
            # Exit from the chatroom
            if message == "!exit":
                client_socket.send("!exit".encode())
                break
            client_socket.send(message.encode())
        except Exception as e:
            if WindowsError:
                print('Connection closed!')
                client_socket.close()
                break
            else:
                print("Error sending a message: ", e)
                break

if __name__ == "__main__":
    client_socket = socket.socket()
    IPv4 = input("Enter IP of the Server:\n")
    client_socket.connect((IPv4, 1337))
    print("You have successfully connected to the chat room!")

    # Creating a thread so the client can recieve the messages and send at the same time

    thread = threading.Thread(target=receive_message, args=(client_socket,))
    thread.start()

    # Sending a messages in a main thread
    send_message(client_socket)