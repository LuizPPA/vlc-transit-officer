import vlc
import sys
import os
import winreg
import socket
import tkinter
from tkinter import *
import tkinter.filedialog

from helpers.server import Server
from helpers.client import Client
from constants import BUFSIZE, DEFAULT_ADDR, DEFAULT_PORT

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


def open_host_server(peers = 1):
    server = Server(DEFAULT_ADDR, DEFAULT_PORT)
    server.serve(peers)
    return server

def open_file_prompt(root):
    root.filename = tkinter.filedialog.askopenfilename(filetypes=(
        ('Video files', '*.mp4'), ('Video files', '*.mov'), ('Video files', '*.mkv'))
    )
    return root.filename

def client_app():
    #TODO: break method down into smaller chunks
    global main_window
    main_window.destroy()
    client_window = tkinter.Tk()
    client_window.title(CLIENT_WINDOW_NAME)
    client_window.geometry('300x50')
    client_window.resizable(False, False)
    video_path = open_file_prompt(client_window)
    player = vlc.MediaPlayer(video_path)
    host = input()
    client = Client(host, DEFAULT_PORT)
    server = client.connect()

    command = -1
    while command != 0:
        command = int(server.recv(BUFSIZE))
        execute(player, command)
    player.stop()

    client_window.mainloop()


def host_app():
    #TODO: break method down into smaller chunks
    global main_window
    main_window.destroy()
    host_window = tkinter.Tk()
    host_window.title(HOST_WINDOW_NAME)
    host_window.geometry('300x50')
    host_window.resizable(False, False)
    
    video_path = open_file_prompt(host_window)
    player = vlc.MediaPlayer(video_path)
    server = open_host_server()

    command = -1
    while command != 0:
        command = int(input())
        server.broadcast(str(command))
        execute(player, command)
    player.stop()

    host_window.mainloop()

def execute(player, command):
    if command == 1:
        if player.is_playing():
            player.pause()
        else:
            player.play()

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
