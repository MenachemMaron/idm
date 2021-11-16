import socket

REC_HOST = '127.0.0.1'
REC_PORT = 65432
SEND_HOST = '127.0.0.1'
SEND_PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_sock:
    listen_sock.bind((REC_HOST, REC_PORT))

    while True:
        listen_sock.listen(1)

        (new_socket1, address1) = listen_sock.accept()
        data = new_socket1.recv(4096)
        if data != b'' and data != '':
            final_url = str(data).split('\\r\\n\\r\\n')[1][:-1]
            print(final_url)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                send_sock.connect((SEND_HOST, SEND_PORT))
                send_sock.sendall(final_url.encode())

