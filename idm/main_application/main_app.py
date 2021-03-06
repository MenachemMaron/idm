"""
main application for IDM project
"""

import tkinter as tk
import requests
import socket
import threading
import json
from urllib.request import Request, urlopen
from queue import Queue
import filecmp

url_notifier = threading.Condition()
queue = Queue()


def open_window(json_data):
    root = tk.Tk()
    root.geometry("400x400")

    tk_create_button("Download", lambda event: splitting_algorithm(json_data, 8), root)
    tk_create_button("Close", lambda event: root.destroy(), root)

    root.mainloop()


def tk_create_button(gui_text, exec_event, window):
    button = tk.Button(window, text=gui_text)
    button.pack()
    button.bind("<Button-1>", exec_event)


def download_file(json_data, size, start_byte, end_byte, index):
    url = json_data['final_url']

    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            # 'Range': 'bytes=<start>'
            # 'Range': 'bytes=<start>,<end>'
            'Range': f'bytes={start_byte}-{end_byte}'
        },
    )

    with urlopen(req) as response:
        print('downloaded ' + str(index))
        data = response.read()
        file_part = [str(index), data]
        queue.put(file_part)


def splitting_algorithm(json_data, threads_count):
    url = json_data['final_url']

    response = requests.head(url, allow_redirects=True)
    size = response.headers.get('content-length', 0)
    print(size)

    used_fragments = 0
    fragment_size = int(size) // int(threads_count)

    threads = []
    for i in range(threads_count):
        if used_fragments + fragment_size * 2 > int(size):
            last_thread = threading.Thread(target=download_file,
                                           args=(json_data, int(size), used_fragments, int(size), i))
            threads.append(last_thread)
            print(f'downloading {used_fragments}-{size}')
            break
        else:
            threads.append(threading.Thread(target=download_file, args=(
                json_data, int(size), used_fragments, used_fragments + fragment_size - 1, i)))
            print(f'downloading {used_fragments}-{used_fragments + fragment_size - 1}')
        used_fragments += fragment_size

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with open(url[url.rfind("/") + 1:], "ab") as out_file:
        all_parts = list(queue.queue)
        sorted_items = sorted(all_parts, reverse=False)
        for item in sorted_items:
            out_file.write(item[1])
            print(f'added {item[0]}')

    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"})
    comp_data = urlopen(request)

    with open("testing.exe", "wb") as file:
        file.write(comp_data.read())

    print(filecmp.cmp('testing.exe', 'setup-lightshot.exe'))


def listen_for_server():
    print('listen_for_server started')

    host = '127.0.0.1'
    port = 65433
    global global_json_data

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))

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
    threading.Thread(target=listen_for_server).start()
    threading.Thread(target=main_proc).start()


if __name__ == "__main__":
    main()
