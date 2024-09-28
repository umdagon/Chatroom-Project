"""\

This module is a Server of the chatroom.

Special objects:

Be sure you have enabled port forwarding to allow WAN connections.

shortcomings:
1.Authorization process allowing to the clients only to connect by the order.
2.Receiving of the message will remove a written text in dialogue row.

"""

import socket
import select
import time


# def server_terminal():
#     while True:
#         a = input('_')
#         if a == 'shutdown':
#             exit()


# Feature will be used to attach the time when the message has arrived to a clients.
def message_time():
    y = time.localtime().tm_year
    mon = time.localtime().tm_mon
    d = time.localtime().tm_mday
    h = time.localtime().tm_hour
    minute = time.localtime().tm_min
    s = time.localtime().tm_sec
    return f'[{d}/{mon}/{y}  {h}:{minute}:{s}]'


def chatroom():
    users = {}  # Users dictionary
    username_socket = {}  # Client sockets and nickname dictionary

    # Get nickname from username_socket dictionary.
    def get_username(cs):
        return username_socket[cs]

    # Sign in function
    def sign_user(cs, info):
        try:
            cs.send("Sign in:\n ".encode())
            cs.send("Enter Username: ".encode())
            username = cs.recv(100).decode()
            cs.send("Enter Password: ".encode())
            password = cs.recv(100).decode()
            if username in users and users[username] == password:
                cs.send("Welcome to the chatroom!:\n".encode())
                socket_list.append(cs)
                print(f'{username}, connected!\n')
            elif username in users:
                cs.send("Wrong password!\n1.Try again.\n2.log in\n".encode())
                request = cs.recv(100).decode()
                if request == '1':
                    try:
                        sign_user(cs, info)
                    except:
                        print("Sign in error after wrong password.")
                        cs.close()
                else:
                    try:
                        register_user(cs, info)
                    except:
                        print("Register error after wrong password.")
                        cs.close()
            else:
                cs.send("User does not exist!\n1.Try again.\n2.log in\n".encode())
                request = cs.recv(100).decode()
                if request == '1':
                    try:
                        sign_user(cs, info)
                    except:
                        print("Sign in error after wrong password.")
                        cs.close()
                else:
                    try:
                        register_user(cs, info)
                    except:
                        print("Register error after wrong password.")
                        cs.close()
        except Exception as err:
            print(f"Sign in error: {err}")
            authorization(cs, info)

    # Log in function
    def register_user(cs, info):
        try:
            cs.send("Choose username: ".encode())
            username = cs.recv(1024).decode()
            cs.send("Set password:".encode())
            pass1 = cs.recv(1024).decode()
            cs.send("Confirm password:".encode())
            pass2 = cs.recv(1024).decode()
            if pass1 == pass2:
                if username in users:
                    cs.send("Username already exists, try again!".encode())
                    try:
                        register_user(cs, info)
                    except:
                        print("Same username register error!")
                else:
                    users.update({username: pass1})
                    username_socket.update({cs: username})
                    print(f'User {username} added.'
                          f'{users}')
                    try:
                        sign_user(cs, info)
                    except:
                        print("sign in error after registration")
        except Exception as err:
            print(f'Registration error:{err}, please try again.')
            authorization(cs, info)

    # Check if the user disconnected from the server to avoid errors
    def exit_check():
        if message == '!exit':
            notified_socket.send('!exit'.encode())
            print(f'The client {client_info[0]}:{client_info[1]}, has disconnected from the server')
            socket_list.remove(notified_socket)
            notified_socket.close()
            return True
        return False

    # Authorization before accepting the socket
    def authorization(cs, info):
        print(f'Connection established with {info[0]}:{info[1]}')
        cs.send(f"Welcome to the chatroom: \n1.log in\n2.sign in\n3.Cancel".encode())
        userinput = cs.recv(1024).decode()
        if userinput == "1":
            register_user(cs, info)
        elif userinput == "2":
            sign_user(cs, info)
        else:
            cs.send("Disconnected from the server!".encode())
            cs.close()
    # Creating a socket
    server = socket.socket()
    # Configure the socket so we can allow reconnection.
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 1337))
    server.listen()

    socket_list = [server]

    while True:
        # Monitoring socket list, waiting for events input output.
        read_sockets, _, except_sockets = select.select(socket_list, [], socket_list)

        # Exam of sockets that ready for a read
        for notified_socket in read_sockets:
            if notified_socket == server:  # Checking if there is a new connection.
                # Starting authorization process, accepting if successful.
                client_socket, client_info = server.accept()
                authorization(client_socket, client_info)
            else:
                try:  # If the current socket is ready to read but not the server, means that we have a client socket
                    # sending an information to the server. We're going to receive the messages and send them back.
                    #
                    # BROADCAST function:
                    #
                    message = notified_socket.recv(1024).decode()
                    if message:
                        nickname = get_username(client_socket)
                        if exit_check():
                            continue
                        print(f"{message_time()}{nickname}: {message}")
                        for client_socket in socket_list:
                            if client_socket != server and client_socket != notified_socket:
                                client_socket.send(f"{message_time()} {nickname}: {message}".encode())
                    else:
                        print(f"Error occurred with {client_info[0]}:{client_info[1]}.")
                        socket_list.remove(notified_socket)
                        notified_socket.close()
                except Exception as e:
                    print(f"{e} {client_info[0]}:{client_info[1]}.")
                    socket_list.remove(notified_socket)
                    notified_socket.close()
        for notified_socket in except_sockets:
            socket_list.remove(notified_socket)
            notified_socket.close()


if __name__ == "__main__":
    chatroom()
