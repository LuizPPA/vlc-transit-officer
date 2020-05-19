import platform
import queue
import os
import subprocess
import sys
import queue

from PyQt5 import QtWidgets, QtGui, QtCore
import vlc


class Player(QtWidgets.QMainWindow):

    def __init__(self, title='Vlc Transit Officer', master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle(title)

        self.instance = vlc.Instance()
        self.media = None
        self.mediaplayer = self.instance.media_player_new()
        self.buffer = queue.Queue()

        self.create_ui()
        self.is_paused = False
        self.is_mute = False

        self.play_pause_callback = lambda: None
        self.stop_callback = lambda: None

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)
        self.timer.timeout.connect(self.update_time_label)

    def create_ui(self):
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        # Create the time display
        self.timelabel = QtWidgets.QLabel("00:00:00", self)

        # Create the position slider (QSlider)
        self.positionslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.positionslider.sliderMoved.connect(self.set_position)
        self.positionslider.sliderMoved.connect(self.update_time_label)

        # Create the play button and connect it to the play/pause function
        self.playbutton = QtWidgets.QPushButton()
        self.playbutton.setFixedWidth(30)
        self.playbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playbutton.clicked.connect(self.play_pause)

        # Create the stop button and connect it to the stop function
        self.stopbutton = QtWidgets.QPushButton()
        self.stopbutton.setFixedWidth(30)
        self.stopbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop))
        self.stopbutton.clicked.connect(self.stop)

        # Create the mute button and connect it to the mute function
        self.mutebutton = QtWidgets.QPushButton()
        self.mutebutton.setFixedWidth(30)
        self.mutebutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaVolume))
        self.mutebutton.clicked.connect(self.mute)

        self.top_control_box = QtWidgets.QHBoxLayout()

        # Add the time and position slider to the 1st controls layout
        self.top_control_box.addWidget(self.timelabel)
        self.top_control_box.addWidget(self.positionslider)

        self.bottom_control_box = QtWidgets.QHBoxLayout()

        # Add the buttons to the 2nd controls layout
        self.bottom_control_box.addWidget(self.playbutton)
        self.bottom_control_box.addWidget(self.stopbutton)
        self.bottom_control_box.addWidget(self.mutebutton)

        self.vboxlayout = QtWidgets.QVBoxLayout()

        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addLayout(self.top_control_box)
        self.vboxlayout.addLayout(self.bottom_control_box)

        self.widget.setLayout(self.vboxlayout)

        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        # Create actions to load a new media file
        open_action = QtWidgets.QAction("Load Video", self)
        file_menu.addAction(open_action)
        open_action.triggered.connect(self.open_file)

        self.set_controls_available(False)

    def set_position(self):
        # Set the media position to where the slider was dragged
        self.timer.stop()
        pos = self.positionslider.value()

        if pos >= 0:
            current_time = self.mediaplayer.get_time()

            if current_time == -1:
                self.timer.start()
                return

        self.mediaplayer.set_position(pos * .001)
        self.timer.start()

    def play_pause(self):
        if self.play_pause_callback:
            self.play_pause_callback()
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setIcon(self.style().standardIcon(
                QtWidgets.QStyle.SP_MediaPlay))
            self.is_paused = True
            self.timer.stop()
        else:
            self.mediaplayer.play()
            self.playbutton.setIcon(self.style().standardIcon(
                QtWidgets.QStyle.SP_MediaPause))
            self.timer.start()
            self.is_paused = False

    def stop(self):
        self.mediaplayer.stop()
        self.playbutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.mutebutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaVolume))
        self.is_mute = False

        time = QtCore.QTime(0, 0, 0, 0)
        self.timelabel.setText(time.toString())

        # Reset the media position slider
        self.positionslider.setValue(0)
        self.timer.stop()
        if self.stop_callback:
            self.stop_callback()

    def mute(self):
        if self.is_mute:
            self.mediaplayer.audio_set_volume(100)
            self.mutebutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaVolume))
            self.is_mute = False
        else:
            self.mediaplayer.audio_set_volume(0)
            self.mutebutton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaVolumeMuted))
            self.is_mute = True

    def open_file(self):
        dialog_txt = "Choose Media File"
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, dialog_txt, os.path.expanduser('~'))
        if not filename[0]:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename[0])

        # Put the media in the media player
        self.mediaplayer.set_media(self.media)

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        self.setWindowTitle("Playing: {}".format(self.media.get_meta(0)))

        if platform.system() == "Linux":  # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.set_controls_available(True)

    def update_ui(self):
        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        media_pos = int(self.mediaplayer.get_position() * 1000)
        self.positionslider.setValue(media_pos)

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            if not self.is_paused:
                self.stop()

    def update_time_label(self):
        mtime = QtCore.QTime(0, 0, 0, 0)
        self.time = mtime.addMSecs(self.mediaplayer.get_time())
        self.timelabel.setText(self.time.toString())

    def set_controls_available(self, state):
        self.playbutton.setEnabled(state)
        self.stopbutton.setEnabled(state)
        self.mutebutton.setEnabled(state)


def main():
    app = QtWidgets.QApplication(sys.argv)
    player = Player()

    player.show()
    player.resize(1024, 768)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
