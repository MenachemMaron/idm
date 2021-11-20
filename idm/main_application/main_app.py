import tkinter as tk
import requests
import socket
import threading
import json
import shutil
from urllib.request import Request, urlopen

url_notifier = threading.Condition()

def open_window(json_data):
    root = tk.Tk()
    root.geometry("400x400")

    tk_create_button("Download", lambda event: download_file(json_data), root)
    tk_create_button("Close", lambda event: root.destroy(), root)

    root.mainloop()


def tk_create_button(gui_text, exec_event, window):
    button = tk.Button(window, text=gui_text)
    button.pack()
    button.bind("<Button-1>", exec_event)


def download_file(json_data):
    url = json_data['final_url']

    response = requests.head(url, allow_redirects=True)
    size = response.headers.get('content-length', 0)
    print(size)

    with open(url[url.rfind("/") + 1 :], "ab") as out_file:
        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                # 'Range': 'bytes=<start>'
                # 'Range': 'bytes=<start>,<end>'
                # 'Range': 'bytes=0-10000'
            },
        )
        with urlopen(req) as response:
            shutil.copyfileobj(response, out_file)


def splitting_algorithm(json_data, threads_count):
    url = json_data['final_url']

    response = requests.head(url, allow_redirects=True)
    size = response.headers.get('content-length', 0)
    print(size)

    used_fragments = 0
    fragment_size = size // threads_count
    for i in range(threads_count):
            # threading.Thread(target=download_file, args=(json_data, size, used+fragments, used_fragments+fragment_size)).start()
            if used_fragments + fragment_size*2 > size:
                # TODO: проверить на правильность вычислений
                print(f'downloading {used_fragments}-{size}')
                break
            else:
                print(f'downloading {used_fragments}-{used_fragments+fragment_size-1}')
            used_fragments += fragment_size 


def listen_for_server():
    print('listen_for_server started')

    HOST = '127.0.0.1'
    PORT = 65433
    global global_json_data

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))

        while True:
            sock.listen(1)
            (new_socket1, address1) = sock.accept()

            json_data = new_socket1.recv(4096).decode()
            if json_data != b'' and json_data is not None:
                print(json.loads(json_data))
                global_json_data = json.loads(json_data)
                url_notifier.acquire()
                url_notifier.notify()
                url_notifier.release()
                print('listen_for_server notified')


def main_proc():
    print('main_proc started')
    while True:
        url_notifier.acquire()
        url_notifier.wait()
        print('main_proc notified')
        url_notifier.release()

        open_window(global_json_data)


def main():
    threading.Thread(target = listen_for_server).start()
    threading.Thread(target = main_proc).start()
    

if __name__ == "__main__":
    main()
