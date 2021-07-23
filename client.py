import socket
import os
downloadDir = "/tmp"


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        if(message.startswith("pull")):
            client_socket.send(message.encode())
            out ,msg ,  filename = message.split(" ")
            # name = filename.split("/")
            with open("pullfile.txt", 'wb') as f:
                print('file opened')
                while True:
                    print('receiving data...')
                    data = client_socket.recv(1024)
                    # print('data=%s', (data))
                    if not data:
                        break
                    # write data to a file
                    f.write(data)
        if(message.startswith("commit&push")):
            client_socket.send(message.encode())
            out ,msg ,  filename = message.split(" ")
            # name = filename.split("/")
            f = open(filename,'rb')
            l = f.read(1024)
            while (l):
                client_socket.send(l)
                print('Sent ',repr(l))
                l = f.read(1024)
        if(message.startswith("download")):
            client_socket.send(message.encode())
            out ,  filename = message.split(" ")
            with open(os.path.join(downloadDir, filename), 'wb') as file_to_write:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file_to_write.write(data)
                file_to_write.close()
        else:
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response
        # tt = 1
        # while tt > 0:
        #     client_socket.send(message.encode())  # send message
        #     data = client_socket.recv(1024).decode()  # receive response
        #     tt = tt - 1

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()