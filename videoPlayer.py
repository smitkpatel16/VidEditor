from PyQt6.QtWidgets import QWidget
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtWidgets import QVBoxLayout


class VidPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.videoPlayer = QMediaPlayer(self)
        self.__meidaDevices = QMediaDevices(self)
        self.__videoWidget = QVideoWidget(self)
        self.audio = QAudioOutput(self)
        self.videoPlayer.setVideoOutput(self.__videoWidget)
        self.videoPlayer.setAudioOutput(self.audio)
        self.__updateAudioOutputs()
        self.__arrangeWidgets()
        self.__connectSignals()

    def __arrangeWidgets(self):
        self.__layout.addWidget(self.__videoWidget)

    def __connectSignals(self):
        self.__meidaDevices.audioOutputsChanged.connect(
            self.__updateAudioOutputs)

    def __updateAudioOutputs(self):
        ao = self.__meidaDevices.defaultAudioOutput()
        self.audio.setDevice(ao)

    def initUI(self):
        self.setWindowTitle('Video Editor')
        self.resize(800, 600)
        self.show()
