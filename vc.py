import vlc
import sys
import os
import winreg
import socket
import _thread as thread
import tkinter
from tkinter import *
import tkinter.filedialog
from PyQt5 import QtWidgets, QtGui, QtCore

from helpers.server import Server
from helpers.client import Client
from Player import Player
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
    thread.start_new_thread(manage_host_connections, (server, peers))
    return server

def manage_host_connections(server, peers):
    server.serve(peers)

def open_file_prompt(root):
    root.filename = tkinter.filedialog.askopenfilename(filetypes=(
        ('Video files', '*.mp4'), ('Video files', '*.mov'), ('Video files', '*.mkv'))
    )
    return root.filename

def client_app():
    global main_window
    main_window.destroy()
    client_window = tkinter.Tk()
    client_window.title(CLIENT_WINDOW_NAME)
    client_window.geometry('300x50')
    client_window.resizable(False, False)
    
    client = Client(DEFAULT_ADDR, DEFAULT_PORT)
    player = client.create_player()
    player.show()

    entry = Entry(client_window)
    entry.pack()
    btn_connect = Button(client_window, text='Connect', command= lambda: connect_client(client, player, entry.get()))
    btn_connect.pack()

    client_window.mainloop()

def connect_client(client, player, host = DEFAULT_ADDR):
    server = client.connect(host)
    thread.start_new_thread(listen_to_host, (server, player))

def listen_to_host(server, player):
    command = -1
    while command != 0:
        command = server.recv(BUFSIZE)
        execute(player, command)

def host_app():
    global main_window
    main_window.destroy()
    host_window = tkinter.Tk()
    host_window.title(HOST_WINDOW_NAME)
    host_window.geometry('300x50')
    host_window.resizable(False, False)
    
    server = open_host_server()

    player = server.create_player()
    player.show()

    host_window.mainloop()
    

def execute(player, command):
    player.buffer.put(command)

def main():
    init_win_path()
    app = QtWidgets.QApplication(sys.argv)

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
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
