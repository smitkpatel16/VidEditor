from PyQt6.QtWidgets import QWidget
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal


class VideoPlayer(QMediaPlayer):
    stopped = pyqtSignal()

    def __init__(self, parent=None):
        self.__selection = []
        self.__selectionPlay = 0
        super().__init__(parent)
        self.positionChanged.connect(self.__positionChanged)

    def __positionChanged(self, position):
        if self.__selection and self.__selectionPlay < len(self.__selection):
            if position >= self.__selection[self.__selectionPlay][1]:
                self.__selectionPlay += 1
                if self.__selectionPlay == len(self.__selection):
                    self.__selectionPlay = 0
                    self.stop()
                self.setPosition(self.__selection[self.__selectionPlay][0])

    def clearSelection(self):
        self.__selectionPlay = 0
        self.__selection.clear()

    def addSelection(self, selections):
        for se in selections:
            start = se[0]
            if not self.__selection:
                self.setPosition(start)
            self.__selection.append(se)


class AudioPlayer(QMediaPlayer):
    stopped = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class MediaPlayer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.videoPlayer = VideoPlayer(self)
        self.audioPlayer = AudioPlayer(self)
        self.__meidaDevices = QMediaDevices(self)
        self.__videoWidget = QVideoWidget(self)
        self.__audio = QAudioOutput(self)
        self.videoPlayer.setVideoOutput(self.__videoWidget)
        self.audioPlayer.setAudioOutput(self.__audio)
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
        self.__audio.setDevice(ao)

    def initUI(self):
        self.setWindowTitle('Video Editor')
        self.resize(800, 600)
        self.show()

    def seekVideo(self, position):
        self.videoPlayer.setPosition(position)

    def seekAudio(self, position):
        self.audioPlayer.setPosition(position)

    def adjustVolume(self, volume):
        self.__audio.setVolume(volume)
