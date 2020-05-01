import vlc
import sys
import os
import winreg
import socket
import tkinter
from tkinter import *
import tkinter.filedialog

from helpers.connection_controller import ConnectionController

APP_NAME = 'VLC Transit Officer'
CLIENT_WINDOW_NAME = 'Client'
HOST_WINDOW_NAME = 'Host'
main_window = None

def init_win_path():
    vlc_reg_key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\VideoLAN\VLC')
    vlc_path = winreg.QueryValueEx(vlc_reg_key, 'InstallDir')[0]

    if vlc_path not in sys.path:
        sys.path.append(vlc_path)


def open_host_server():
    # TODO
    cn = ConnectionController('25.4.28.237', 8080)
    cn.serve(1)
    message = input()
    cn.broadcast(message)
    print(cn)

    pass

def open_file_prompt():
    # TODO
    # root.withdraw()
    # root.filename = tkinter.filedialog.askopenfilename(filetypes=(
    #     ('Video files', '*.mp4'), ('Video files', '*.mov'), ('Video files', '*.mkv')))
    return None

def client_app():
    global main_window
    main_window.destroy()
    host = input()
    cn = ConnectionController(host, 8080)
    server = cn.connect()
    data = server.recv(4096)
    print(data)
    client_window = tkinter.Tk()
    client_window.title(CLIENT_WINDOW_NAME)
    client_window.geometry('300x50')
    client_window.resizable(False, False)

    video_path = open_file_prompt()

    client_window.mainloop()


def host_app():
    global main_window
    main_window.destroy()
    host_window = tkinter.Tk()
    host_window.title(HOST_WINDOW_NAME)
    host_window.geometry('300x50')
    host_window.resizable(False, False)
    
    video_path = open_file_prompt()
    
    open_host_server()

    host_window.mainloop()

def main():
    init_win_path()

    global main_window
    main_window = tkinter.Tk()
    main_window.title(APP_NAME)
    main_window.geometry('300x50')
    main_window.resizable(False, False)

    btn_client = Button(main_window, text='Client', command=client_app)
    btn_client.grid(column=0, row=0)

    btn_host = Button(main_window, text='Host', command=host_app)
    btn_host.grid(column=1, row=0)

    main_window.mainloop()

if __name__ == '__main__':
    main()
