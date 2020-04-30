try:
    import vlc
except ImportError:
    raise ImportError('no %s module, %s' % ('vlc.py', _PyPI('Python-VLC')))
    
import socket
import tkinter
import tkinter.filedialog

root = tkinter.Tk()
# root.withdraw()
root.filename = tkinter.filedialog.askopenfilename(filetypes = (('Video files', '*.mp4'), ('Video files', '*.mov'), ('Video files', '*.mkv')))

# serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serv.bind(('0.0.0.0', 8080))
# serv.listen(5)
p = vlc.MediaPlayer(root.filename)
p.play()
#     conn, addr = serv.accept()

while True:
    op = input('Op: ')
    if op == '0':
        # conn.send('0')
        p.stop()
        break
    elif op == '1':
        # conn.send('1')
        if p.is_playing():
            p.pause()
        else:
            p.play()

# conn.close()