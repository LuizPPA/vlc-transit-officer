from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QFileDialog


class MediaPlayerController:
    SUPPORTED_FILES_FORMATS = '(*.mp4 *.mkv)'

    def __init__(self):
        pass

    def open_video(self, main_window, media_player):
        video_path, _ = QFileDialog.getOpenFileName(main_window, "Open Video", "~",
                                                    "Video Files %s" % self.SUPPORTED_FILES_FORMATS)
        if video_path != '':
            url = QUrl.fromLocalFile(video_path)
            media_player.setMedia(QMediaContent(url))
