import socket
import os
import sys

parent_path = "C:/Users/mohammad reza/Desktop/CN"
buffer_size = 4096

def existName(name):
    cnt = 0
    with open('names.txt') as f:
        lines = f.readlines()
        for line in lines:
            name1 , pass1 = line.split()
            if(name == name1):
                print(cnt)
                cnt =cnt + 1
    if(cnt > 0):
        return True
    else:
        return False
def checkPass(name , password):
    with open('names.txt') as f:
        lines = f.readline()
        while lines:
            name1 , pass1 = lines.split()
            if(name == name1):
                if(password == pass1):
                    return True
                else:
                    return False
def makedir(name):
    current_path = os.path.join(parent_path, name)
    os.mkdir(current_path)
    return current_path

def histo(user_path , command):
    path = os.path.join(user_path, "history"+".txt")
    with open(path, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(command)

def server_program():
    # get the hostname
    current_path = ""
    user_path = ""
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    ACK = 1
    while(ACK == 1):
        conn.recv(1024).decode()
        menu = ('''1) login
                      2) register''')
        conn.send(menu.encode())
        ack = conn.recv(1024).decode()
        if(int(ack) == 1):
            S = 1
            while (S == 1):
                pinname = "enter name"
                conn.send(pinname.encode())
                name = conn.recv(1024).decode()
                if(existName(str(name))):
                    pinpass = "enter pass"
                    conn.send(pinpass.encode())
                    password = conn.recv(1024).decode()
                    if(checkPass(name , password)):
                        pin = "You are logged in"
                        conn.send(pin.encode())
                        nothing = conn.recv(1024).decode()
                        user_path = os.path.join(parent_path, name)    
                        current_path = user_path
                        ACK = 2
                        S = 2
                    else:
                        pin = "You info is wrong try again/Press OK to continue"
                        conn.send(pin.encode())
                        nothing = conn.recv(1024).decode()

        elif(int(ack) == 2):
            print("we are here")
            pinname = "enter name"
            conn.send(pinname.encode())
            name = conn.recv(1024).decode()
            print(name)
            if(existName(str(name))):
                pinpass = "error this account is already been"
                conn.send(pinpass.encode())
                name = conn.recv(1024).decode()
            else:
                pinpass = "enter pass"
                conn.send(pinpass.encode())
                password = conn.recv(1024).decode()
                with open("names.txt", "a+") as file_object:
                    # Move read cursor to the start of file.
                    file_object.seek(0)
                    # If file is not empty then append '\n'
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")
                    # Append text at the end of file
                    file_object.write(name + "  " + password)
                    user_path = os.path.join(parent_path, name)
                    current_path = user_path
                    os.mkdir(current_path)
                    path = os.path.join(current_path, "history"+".txt")
                    f = open(path  , "a")
                    f.close()
                ACK = 2
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        pinpass = "enter command"
        conn.send(pinpass.encode())
        command = conn.recv(1024).decode()
        if not command:
            # if data is not received break
            break
        if(command == "makerepo"):
            print(current_path)
            pinpass = "enter repository name"
            conn.send(pinpass.encode())
            data1 = conn.recv(1024).decode()
            current_path = os.path.join(current_path, data1)
            os.mkdir(current_path)
            command = command + "  The Repository name : " + data1
            histo( user_path , command)
        if(command.startswith("commit&push")):
            out , msg ,  filepath = command.split(" ")
            current_path = os.path.join(current_path, filepath)
            with open(current_path, 'wb') as f:
                print('file opened')
                while True:
                    print('receiving data...')
                    data = conn.recv(1024)
                    print('data=%s', (data))
                    if not data:
                        break
                    # write data to a file
                    f.write(data)
                command = command + "  Commit the " + msg +" and push the : " + filepath
                histo( user_path , command)
        if(command.startswith("pull")):
            out , msg ,  filepath = command.split(" ")
            current_path = os.path.join(current_path, filepath)
            f = open(current_path,'rb')
            l = f.read(1024)
            while (l):
                conn.send(l)
                # print('Sent ',repr(l))
                l = f.read(1024)
            command = command + "  Pull the : " + filepath
            histo( user_path , command)

        if(command.startswith("go")):
            out ,  filepath = command.split(" ")
            current_path = os.path.join(current_path, filepath)
            print(current_path)

        if(command.startswith("download")):
            out ,  filepath = command.split(" ")
            print(filepath)
            with open(filepath, 'rb') as file_to_send:
                for data in file_to_send:
                    conn.sendall(data)
            print("from connected user: " + str(data))
        
        # data = input(' -> ')
        # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()