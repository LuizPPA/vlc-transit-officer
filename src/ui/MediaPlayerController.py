from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QFileDialog


class MediaPlayerController:
    SUPPORTED_FILES_FORMATS = '(*.mp4 *.mkv)'

    def __init__(self, player):
        self.enable_play_pause_callback = player.enable_play_pause_callback
        self.enable_stop_callback = player.enable_stop_callback

        self.is_allowed_to_play_pause = False
        self.is_allowed_to_stop = False
        self.is_playing = False
        self.enable_play_pause(False)
        self.enable_stop(False)

    def open_video(self, main_window, media_player):
        video_path, _ = QFileDialog.getOpenFileName(main_window, "Open Video", "~",
                                                    "Video Files %s" % self.SUPPORTED_FILES_FORMATS)
        if video_path != '':
            url = QUrl.fromLocalFile(video_path)
            media_player.setMedia(QMediaContent(url))
            self.enable_play_pause(True)

    def enable_play_pause(self, state):
        self.is_allowed_to_play_pause = state
        self.enable_play_pause_callback(state)

    def enable_stop(self, state):
        self.is_allowed_to_stop = state
        self.enable_stop_callback(state)

    def play_pause_video(self, media_player):
        if self.is_allowed_to_play_pause:
            if self.is_playing:
                media_player.pause()
            else:
                media_player.play()
                self.enable_stop(True)

            self.is_playing = not self.is_playing

    def stop_video(self, media_player):
        if self.is_allowed_to_stop:
            media_player.stop()
            self.is_playing = False
            self.enable_stop(False)
