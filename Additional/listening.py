import socket
import select

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    # sock.listen()
    # connection, addr = sock.accept()
    # with connection:
    #     print('Connected by', addr)
    #     while True:
    #         data = connection.recv(1024).decode()
    #         print(data)
    #         print("\n\n\n\n")

    while True:
        sock.listen(1)
        (new_socket1, address1) = sock.accept()
        data = new_socket1.recv(4096)
        if data != b'' and data != '':
            print(str(data).split('\\r\\n\\r\\n')[1][:-1])