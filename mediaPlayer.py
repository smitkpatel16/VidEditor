import time
from threading import Thread
from PyQt6.QtWidgets import QWidget
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QMediaDevices
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import pyqtSignal


class VideoPlayer(QMediaPlayer):
    videoPlayPosition = pyqtSignal(int)

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
                    print('end of selection')
                    self.stop()
                    return
                self.setPosition(self.__selection[self.__selectionPlay][0])
        self.videoPlayPosition.emit(position)

    def clearSelection(self):
        self.__selection.clear()

    def addSelection(self, se):
        start = se[0]
        end = se[1]
        if not self.__selection:
            self.setPosition(start)
        self.__selection.append((start, end))


class AudioPlayer(QMediaPlayer):
    audioPlayPosition = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def __createThread(self):
        self.__t = Thread(target=self.__updateAudioPosition)

    def play(self):
        self.__createThread()
        r = super().play()
        self.__t.start()
        return r

    def pause(self):
        r = super().pause()
        self.__t.join()
        return r

    def __updateAudioPosition(self):
        while self.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.audioPlayPosition.emit(self.position())
            time.sleep(0.1)
        self.audioPlayPosition.emit(self.position())


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
        self.audio.setVolume(volume)
