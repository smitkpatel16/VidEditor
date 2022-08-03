import time
from threading import Thread
from PyQt6.QtWidgets import QWidget
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal


class VidPlayer(QWidget):
    playPosition = pyqtSignal(int)

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
        self.__t = None
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

    def __updatePlay(self):
        while True:
            self.playPosition.emit(self.videoPlayer.position())
            time.sleep(1)

    def initUI(self):
        self.setWindowTitle('Video Editor')
        self.resize(800, 600)
        self.show()

    def play(self):
        self.videoPlayer.play()
        self.__t = Thread(target=self.__updatePlay)
        self.__t.start()

    def pause(self):
        self.videoPlayer.pause()
        self.__t._stop()

    def stop(self):
        self.videoPlayer.stop()
        if self.__t:
            self.__t._stop()
