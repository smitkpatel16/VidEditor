# mediaControls widget for the video player
from enum import Enum
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt


class MediaControls(QWidget):
    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()
    mute = pyqtSignal()
    seek = pyqtSignal(int)
    volume = pyqtSignal(int)

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
        self.__volSlider = QSlider(Qt.Orientation.Horizontal)
        self.__volSlider.setRange(0, 100)
        self.__volSlider.setValue(50)
        self.__arrangeWidgets()
        self.__connectSignals()
        self.show()

    def __arrangeWidgets(self):
        self.__layout.addWidget(self.__playBtn)
        self.__layout.addWidget(self.__stopBtn)
        self.__layout.addWidget(self.__volSlider)

    def __connectSignals(self):
        self.__playBtn.clicked.connect(self.__play)
        self.__stopBtn.clicked.connect(self.__stop)
        self.__volSlider.valueChanged.connect(self.__setVolume)

    def __play(self):
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
