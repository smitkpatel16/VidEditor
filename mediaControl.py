# mediaControls widget for the video player
from enum import Enum
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QDial
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt


class MediaControls(QWidget):
    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()
    mute = pyqtSignal()
    seek = pyqtSignal(int)
    volume = pyqtSignal(int)
    completion = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MediaControls, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Media Controls')
        self.resize(200, 100)
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)
        self.__playBtn = QPushButton('Play')
        self.__stopBtn = QPushButton('Stop')
        self.__playBtn.setCheckable(True)
        self.__playBtn.setChecked(False)
        self.__stopBtn.setEnabled(False)
        self.__label = QLabel('00:00:00')
        self.__volSlider = QDial()
        self.__volSlider.setNotchesVisible(True)
        self.__volSlider.setRange(0, 100)
        self.__volSlider.setValue(50)
        self.__playSlider = QSlider(Qt.Orientation.Horizontal)
        self.__playSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.__arrangeWidgets()
        self.__connectSignals()
        self.duration = 0
        self.show()

    def setDuration(self, duration):
        self.duration = duration
        self.__playSlider.setRange(0, duration)

    def setPlayPosition(self, position):
        self.__playSlider.setValue(position)
        s = position/1000
        h = int(s//3600)
        m = int(s//60)
        s = int(s % 60)
        self.__label.setText('{}h:{}m:{}s'.format(h, m, s))
        self.completion.emit(int(position/self.duration*100))

    def __arrangeWidgets(self):
        self.__layout.addWidget(self.__playBtn)
        self.__layout.addWidget(self.__stopBtn)
        self.__layout.addWidget(self.__playSlider)
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__volSlider)

    def __connectSignals(self):
        self.__playBtn.clicked.connect(self.__play)
        self.__stopBtn.clicked.connect(self.__stop)
        self.__volSlider.valueChanged.connect(self.__setVolume)
        self.__playSlider.sliderMoved.connect(self.__seek)

    def __play(self, playFrom=0):
        if self.__playBtn.isChecked():
            self.__playBtn.setText('Pause')
            self.__stopBtn.setEnabled(True)
            self.play.emit()
        else:
            self.__playBtn.setText('Play')
            self.__stopBtn.setEnabled(False)
            self.pause.emit()

    def __stop(self):
        self.__playBtn.setChecked(False)
        self.__playBtn.setText('Play')
        self.__stopBtn.setEnabled(False)
        self.stop.emit()

    def __setVolume(self, volume):
        self.volume.emit(volume)

    def __seek(self, position):
        self.seek.emit(position)
