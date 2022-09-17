# mediaControls widget for the video player
from enum import Enum
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QDial
from PyQt6.QtWidgets import QLabel
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt


class MediaControls(QWidget):
    playVideo = pyqtSignal()
    pauseVideo = pyqtSignal()
    playAudio = pyqtSignal()
    pauseAudio = pyqtSignal()
    playAll = pyqtSignal()
    pauseAll = pyqtSignal()
    stopAll = pyqtSignal()
    seekVideo = pyqtSignal(int)
    seekAudio = pyqtSignal(int)
    adjustVolume = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MediaControls, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Media Controls')
        self.resize(200, 100)
        self.__layout = QHBoxLayout()
        self.__controls1 = QVBoxLayout()
        self.__controls2 = QVBoxLayout()
        self.__controls3 = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__playBtn = QPushButton('Play')
        self.__playBtn.setCheckable(True)
        self.__playBtn.setChecked(False)
        self.__playBtn.setEnabled(False)

        self.__playVideoBtn = QPushButton('Play Video')
        self.__playAudioBtn = QPushButton('Play Audio')
        self.__stopBtn = QPushButton('Stop All')

        self.__playVideoBtn.setCheckable(True)
        self.__playVideoBtn.setChecked(False)
        self.__playAudioBtn.setCheckable(True)
        self.__playAudioBtn.setChecked(False)
        self.__playAudioBtn.setEnabled(False)
        self.__playVideoBtn.setEnabled(False)

        self.__stopBtn.setEnabled(False)
        self.__videoLabel = QLabel('00/00')
        self.__audioLabel = QLabel('00/00')
        self.__volSlider = QDial()
        self.__volSlider.setNotchesVisible(True)
        self.__volSlider.setRange(0, 100)
        self.__volSlider.setValue(50)

        self.__arrangeWidgets()
        self.__connectSignals()
        self.videoDuration = 0
        self.audioDuration = 0
        self.show()

    def setVideoDuration(self, duration):
        self.videoDuration = duration
        self.__playVideoBtn.setEnabled(True)
        self.__enableAllPlay()

    def setAudioDuration(self, duration):
        self.audioDuration = duration

        self.__playAudioBtn.setEnabled(True)
        self.__enableAllPlay()

    def __enableAllPlay(self):
        if self.videoDuration and self.audioDuration:
            self.__playBtn.setEnabled(True)

    def setVideoPlayPosition(self, position):
        s = position/1000
        self.__videoLabel.setText('{}/{}s'.format(s, self.videoDuration/1000))

    def setAudioPlayPosition(self, position):
        s = position/1000
        self.__audioLabel.setText('{}/{}s'.format(s, self.audioDuration/1000))

    def setVideoState(self, state):
        if state == QMediaPlayer.MediaStatus.EndOfMedia:
            self.__playVideoBtn.setChecked(False)
            self.__playVideoBtn.setText('Play Video')
            self.__videoLabel.setText('0s/{}s'.format(self.videoDuration/1000))
        if not self.__playVideoBtn.isChecked() and not self.__playAudioBtn.isChecked():
            self.__playBtn.setChecked(False)
            self.__playBtn.setText('Play')

    def setAudioState(self, state):
        if state == QMediaPlayer.MediaStatus.EndOfMedia:
            self.__playAudioBtn.setChecked(False)
            self.__playAudioBtn.setText('Play Audio')
            self.__audioLabel.setText('0s/{}s'.format(self.audioDuration/1000))
        if not self.__playVideoBtn.isChecked() and not self.__playAudioBtn.isChecked():
            self.__playBtn.setChecked(False)
            self.__playBtn.setText('Play')

    def stop(self):
        self.__stop()

    def stopVideo(self):
        self.__stopVideo()

    def stopAudio(self):
        self.__stopAudio()

    def __stopVideo(self):
        self.__playVideoBtn.setChecked(False)
        self.__playVideoBtn.setText('Play Video')

    def __stopAudio(self):
        self.__playAudioBtn.setChecked(False)
        self.__playAudioBtn.setText('Play Audio')

    def __arrangeWidgets(self):
        self.__layout.addWidget(self.__playBtn)
        self.__layout.addLayout(self.__controls1)
        self.__controls1.addWidget(self.__playVideoBtn)
        self.__controls1.addWidget(self.__playAudioBtn)
        self.__layout.addWidget(self.__stopBtn)
        self.__layout.addLayout(self.__controls3)
        self.__controls3.addWidget(self.__videoLabel)
        self.__controls3.addWidget(self.__audioLabel)
        self.__layout.addWidget(self.__volSlider)

    def __connectSignals(self):
        self.__playVideoBtn.clicked.connect(self.__playVideo)
        self.__playAudioBtn.clicked.connect(self.__playAudio)
        self.__stopBtn.clicked.connect(self.__stop)
        self.__volSlider.valueChanged.connect(self.__setVolume)
        self.__playBtn.clicked.connect(self.__play)

    def __play(self):
        if self.__playBtn.isChecked():
            self.__playBtn.setText('Pause')
            self.__playAudioBtn.setChecked(True)
            self.__playAudioBtn.setText('Pause Audio')
            self.__playVideoBtn.setChecked(True)
            self.__playVideoBtn.setText('Pause Video')
            self.__stopBtn.setEnabled(True)
            self.playAll.emit()
        else:
            self.__playBtn.setText('Play')
            self.__playAudioBtn.setChecked(False)
            self.__playAudioBtn.setText('Play Audio')
            self.__playVideoBtn.setChecked(False)
            self.__playVideoBtn.setText('Play Video')
            self.__stopBtn.setEnabled(False)
            self.pauseAll.emit()

    def __playVideo(self):
        if self.__playVideoBtn.isChecked():
            self.__playVideoBtn.setText('Pause Video')
            self.playVideo.emit()
        else:
            self.__playVideoBtn.setText('Play Video')
            self.pauseVideo.emit()

    def __playAudio(self):
        if self.__playAudioBtn.isChecked():
            self.__playAudioBtn.setText('Pause Audio')
            self.playAudio.emit()
        else:
            self.__playAudioBtn.setText('Play Audio')
            self.pauseAudio.emit()

    def __stop(self):
        self.__playBtn.setChecked(False)
        self.__playBtn.setText('Play')
        self.__stopBtn.setEnabled(False)
        self.__stopVideo()
        self.__stopAudio()

    def __setVolume(self, volume):
        self.adjustVolume.emit(volume)

    def __seekVideo(self, position):
        self.seekVideo.emit(position)

    def __seekAudio(self, position):
        self.seekAudio.emit(position)
