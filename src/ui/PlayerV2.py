from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPalette
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, \
    QSlider
from PyQt5.QtMultimedia import QMediaPlayer
import sys


class PlayerV2(QWidget):
    WINDOW_TITLE = 'Player V2'
    INITIAL_WIDTH = 1200
    INITIAL_HEIGHT = 900

    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle(self.WINDOW_TITLE)
        self.__init_ui_components()
        self.__center()
        self.show()

    def __init_ui_components(self):
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        video_palette = self.palette()
        video_palette.setColor(QPalette.Background, Qt.black)

        self.video_widget.setAutoFillBackground(True)
        self.video_widget.setPalette(video_palette)
        self.video_widget.show()

        self.play_pause_button = QPushButton('Play/Pause')
        self.stop_button = QPushButton('Stop')
        self.mute_unmute_button = QPushButton('Mute/Unmute')
        self.video_time_counter = QSlider(Qt.Horizontal)

        self.controls_bar = QHBoxLayout()
        self.controls_bar.setContentsMargins(4, 0, 4, 4)

        self.controls_bar.addWidget(self.play_pause_button)
        self.controls_bar.addWidget(self.stop_button)
        self.controls_bar.addWidget(self.mute_unmute_button)
        self.controls_bar.addWidget(self.video_time_counter)

        self.controls_bar_container = QFrame()
        self.controls_bar_container.setMaximumHeight(50)
        self.controls_bar_container.setLayout(self.controls_bar)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.addWidget(self.video_widget)
        self.vertical_layout.addWidget(self.controls_bar_container)
        self.setLayout(self.vertical_layout)

    def __center(self):
        self.resize(self.INITIAL_WIDTH, self.INITIAL_HEIGHT)
        qr = self.frameGeometry()
        position = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(position)
        self.move(qr.topLeft())



def main():
    app = QApplication(sys.argv)
    player = PlayerV2()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
