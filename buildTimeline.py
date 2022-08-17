from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt

# ===============================================================================
# BuildTimeline- Widget that is used to add selections of audio and video
# ===============================================================================


class BuildTimeline(QWidget):
    # override the constructor
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__layout = QHBoxLayout()
        self.__selectionVideo = []
        self.setLayout(self.__layout)
        self.initUI()

    def initUI(self):
        self.__finalSlider = QSlider(Qt.Orientation.Horizontal)
        self.__finalSlider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.__layout.addWidget(self.__finalSlider)

    def addSelectionVideo(self, selection):
        dur = 0
        for se in selection:
            start = se[0]
            end = se[1]
            self.__selectionVideo.append((start, end))
            dur += end - start
        self.__finalSlider.setRange(0, dur)

    def addSelectionAudio(self, selection):
        dur = 0
        for se in selection:
            start = se[0]
            end = se[1]
            self.__selectionAudio.append((start, end))
            du += end - start
        self.__finalSlider.setRange(0, dur)

    def clearSelectionVideo(self):
        self.__selectionVideo.clear()
        self.__finalSlider.setRange(0, 0)

    def clearSelectionAudio(self):
        self.__selectionAudio.clear()
        self.__finalSlider.setRange(0, 0)

    def seekSliderVideo(self, position):
        dur = 0
        for se in self.__selectionVideo:
            if position >= se[0] and position <= se[1]:
                self.__finalSlider.setValue(position - se[0] + dur)
            else:
                dur += se[1] - se[0]

    def seekSliderAudio(self, position):
        self.__finalSlider.setValue(position)
