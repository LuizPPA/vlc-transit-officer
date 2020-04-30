import vlc
import sys
import os
import winreg 
import socket
import tkinter
import tkinter.filedialog


def init_win_path():
    vlc_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\VideoLAN\VLC')
    vlc_path =  winreg.QueryValueEx(vlc_reg_key, 'InstallDir')[0]

    if vlc_path not in sys.path:
        sys.path.append(vlc_path)

def main(): 
    init_win_path()

    # root = tkinter.Tk()
    # # root.withdraw()
    # root.filename = tkinter.filedialog.askopenfilename(filetypes = (('Video files', '*.mp4'), ('Video files', '*.mov'), ('Video files', '*.mkv')))

    # # serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # # serv.bind(('0.0.0.0', 8080))
    # # serv.listen(5)
    # p = vlc.MediaPlayer(root.filename)
    # p.play()
    # #     conn, addr = serv.accept()

    # while True:
    #     op = input('Op: ')
    #     if op == '0':
    #         # conn.send('0')
    #         p.stop()
    #         break
    #     elif op == '1':
    #         # conn.send('1')
    #         if p.is_playing():
    #             p.pause()
    #         else:
    #             p.play()

    # # conn.close()


if __name__ == "__main__":
    main()    
    
    