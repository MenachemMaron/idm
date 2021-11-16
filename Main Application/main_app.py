import tkinter as tk
import requests
import socket
import threading

url_notifier = threading.Condition()

def open_window(url):
    root = tk.Tk()
    root.geometry("400x400")

    tk_create_button("Download", lambda event: download_file(url), root)
    tk_create_button("Close", lambda event: root.destroy(), root)

    root.mainloop()


def tk_create_button(gui_text, exec_event, window):
    button = tk.Button(window, text=gui_text)
    button.pack()
    button.bind("<Button-1>", exec_event)


def download_file(url):
    # resume_header = ({'Range': f'bytes=0-199'})
    # req = requests.get(url, stream=True, headers=resume_header)
    req = requests.get(url, stream=True)

    print(req.content, len(req.content))


def listen_for_server():
    print('listen_for_server started')

    HOST = '127.0.0.1'
    PORT = 65433
    global global_url

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))

        while True:
            sock.listen(1)
            (new_socket1, address1) = sock.accept()
            final_url = new_socket1.recv(4096)
            if final_url != b'' and final_url is not None:
                print(final_url.decode())
                global_url = final_url.decode()
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
        
        print(global_url)
        open_window(global_url)


def main():
    threading.Thread(target = listen_for_server).start()
    threading.Thread(target = main_proc).start()
    

if __name__ == "__main__":
    main()
