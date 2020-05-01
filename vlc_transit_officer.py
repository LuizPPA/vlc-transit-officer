import vlc
import sys
import os
import winreg
import socket
import tkinter
from tkinter import *
import tkinter.filedialog


APP_NAME = 'VLC Transit Officer'
CLIENT_WINDOW_NAME = 'Client'
HOST_WINDOW_NAME = 'Host'
SELECT_FILE_TITLE = 'Select video file'
VIDEO_FILE_EXTENSIONS = (('Video files', '*.mp4'), ('Video files', '*.mov'), ('Video files', '*.mkv'))
main_window = None



def init_win_path():
    vlc_reg_key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\VideoLAN\VLC')
    vlc_path = winreg.QueryValueEx(vlc_reg_key, 'InstallDir')[0]

    if vlc_path not in sys.path:
        sys.path.append(vlc_path)


def open_host_server():
    # TODO
    pass


def open_file_prompt():
    video_path = tkinter.filedialog.askopenfilename(initialdir="/", title=SELECT_FILE_TITLE, filetypes=VIDEO_FILE_EXTENSIONS)
    video_name = video_path.split('/')[len(video_path.split('/'))-1]
    return video_path, video_name


def client_app():
    global main_window
    main_window.destroy()
    client_window = tkinter.Tk()
    client_window.title(CLIENT_WINDOW_NAME)
    client_window.geometry('300x50')
    client_window.resizable(False, False)

    video_path, video_name = open_file_prompt()

    label_video_name = Label(host_window)
    label_video_name.grid(row=0, column=0)

    label_video_name.configure(text='Arquivo carregado: ' + video_name)
    
    client_window.mainloop()


def host_app():
    global main_window
    main_window.destroy()
    host_window = tkinter.Tk()
    host_window.title(HOST_WINDOW_NAME)
    host_window.geometry('300x50')
    host_window.resizable(False, False)

    video_path, video_name = open_file_prompt()

    label_video_name = Label(host_window)
    label_video_name.grid(row=0, column=0)

    label_video_name.configure(text='Arquivo carregado: ' + video_name)

    open_host_server()

    host_window.mainloop()


def main():
    init_win_path()

    global main_window
    main_window = tkinter.Tk()
    main_window.title(APP_NAME)
    main_window.geometry('300x50')
    main_window.resizable(False, False)

    Button(main_window, text='Client', command=client_app).grid(column=0, row=0)

    Button(main_window, text='Host', command=host_app).grid(column=1, row=0)

    main_window.mainloop()


if __name__ == '__main__':
    main()
