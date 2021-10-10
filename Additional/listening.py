import socket
import time

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    connection, addr = sock.accept()
    with connection:
        print('Connected by', addr)
        while True:
            data = connection.recv(1024).decode()
            print(data)