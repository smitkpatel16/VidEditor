from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout


class VidEditorMainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self._videoPlayer = QMediaPlayer(self)
        self.__video_widget = QVideoWidget(self)
        self._videoPlayer.setVideoOutput(self.__video_widget)
        self.__playBtn = QPushButton("Play")
        self.__playBtn.setCheckable(True)
        self.__playBtn.clicked.connect(self.__playVideo)
        self.__arrangeWidgets()

    def __arrangeWidgets(self):
        self.__layout.addWidget(self.__video_widget)
        self.__layout.addWidget(self.__playBtn)

    def __playVideo(self):
        if self.__playBtn.isChecked():
            self._videoPlayer.play()
        else:
            self._videoPlayer.pause()

    def initUI(self):
        self.setWindowTitle('Video Editor')
        self.resize(800, 600)
        self.show()
