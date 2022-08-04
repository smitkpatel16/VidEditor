import time
from threading import Thread
from PyQt6.QtWidgets import QWidget
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal


class MediaPlayer(QWidget):
    videoPlayPosition = pyqtSignal(int)
    audioPlayPosition = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.videoPlayer = QMediaPlayer(self)
        self.audioPlayer = QMediaPlayer(self)
        self.__meidaDevices = QMediaDevices(self)
        self.__videoWidget = QVideoWidget(self)
        self.audio = QAudioOutput(self)
        self.videoPlayer.setVideoOutput(self.__videoWidget)
        self.audioPlayer.setAudioOutput(self.audio)
        self.__vt = None
        self.__at = None
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

    def __updateVideoPosition(self):
        while self.videoPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.videoPlayPosition.emit(self.videoPlayer.position())
            time.sleep(0.1)

    def __updateAudioPosition(self):
        while self.audioPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.audioPlayPosition.emit(self.audioPlayer.position())
            time.sleep(0.1)

    def initUI(self):
        self.setWindowTitle('Video Editor')
        self.resize(800, 600)
        self.show()

    def playVideo(self):
        self.videoPlayer.play()
        self.__vt = Thread(target=self.__updateVideoPosition)
        self.__vt.start()

    def playAudio(self):
        self.audioPlayer.play()
        self.__at = Thread(target=self.__updateAudioPosition)
        self.__at.start()

    def pauseVideo(self):
        self.videoPlayer.pause()
        if self.__vt:
            self.__vt.join()
            self.__vt = None

    def pauseAudio(self):
        self.audioPlayer.pause()
        if self.__at:
            self.__at.join()
            self.__at = None

    def seekVideo(self, position):
        self.videoPlayer.setPosition(position)

    def seekAudio(self, position):
        self.audioPlayer.setPosition(position)

    def adjustVolume(self, volume):
        self.audio.setVolume(volume)
