import wave
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QScrollArea


class AudioGraph(QWidget):
    def __init__(self, parent=None):
        super(AudioGraph, self).__init__(parent)
        fig = Figure(figsize=(5, 1), dpi=100)
        self.__canvas = FigureCanvas(fig)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.__canvas)
        self.layout().addWidget(self.scroll)
        policy = QSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Expanding)
        self.__canvas.setSizePolicy(policy)
        self.axes = self.__canvas.figure.add_subplot(111)
        self.__canvas.figure.subplots_adjust(
            left=0.0, right=1.0, bottom=0.0, top=1.0, hspace=0.0, wspace=0.0)
        self.axes.set_axis_off()
        self.__vl = None
        fig.canvas.mpl_connect('motion_notify_event', self.__mouseMove)
        fig.canvas.mpl_connect('button_press_event', self.__select)
        fig.canvas.mpl_connect('button_release_event', self.__unselect)
        self.__duration = 0
        self.__totalW = 0
        self.__selection = []
        self.__sl = []
        self.__selectedMarker = None
        # self.addSelection()

    def __select(self, event):
        for sl in self.__sl:
            c = sl.contains(event)[0]
            if c:
                self.__selectedMarker = sl
                self.__selectedMarker.set_color('b')
                self.__canvas.draw()

    def __unselect(self, event):
        self.__selectedMarker.set_color('r')
        self.__selectedMarker = None
        self.__canvas.draw()

    def __mouseMove(self, event):
        c = []
        for sl in self.__sl:
            c.append(sl.contains(event)[0])
        if any(c):
            QApplication.setOverrideCursor(Qt.CursorShape.SizeHorCursor)
        else:
            QApplication.restoreOverrideCursor()
        if self.__selectedMarker:
            self.__selectedMarker.set_xdata([event.xdata, event.xdata])
            self.__highlight()
            self.__canvas.draw()

    def __highlight(self):
        for p in self.__selection:
            p.remove()
        self.__selection.clear()
        self.__sl = sorted(self.__sl, key=lambda p: p.get_xdata()[0])
        for i, j in enumerate(range(0, len(self.__sl), 2)):
            x = self.__sl[j].get_xdata()[0]
            w = self.__sl[i*2+1].get_xdata()[0]-x
            h = self.axes.get_ylim()[1]-self.axes.get_ylim()[0]
            rect = Rectangle((x, self.axes.get_ylim()[
                             0]), w, h, facecolor='r', alpha=0.5)
            self.__selection.append(rect)
            self.axes.add_patch(rect)
            rect.set_zorder(100)

    def addSelection(self):
        self.__sl.append(self.axes.axvline(
            0, ls='-', color='r', lw=3, zorder=100))
        self.__sl.append(self.axes.axvline(
            self.__totalW/10, ls='-', color='r', lw=3, zorder=100))
        self.__highlight()
        self.__canvas.draw()

    def setDuration(self, duration):
        self.__duration = duration
        self.setAudioPosition(0)

    def setAudioPosition(self, pos):
        if self.__duration and self.__vl:
            p = pos/self.__duration
            p = p*self.__totalW
            self.__vl.set_xdata([p, p])
            self.__canvas.draw()

    def plotAudio(self, audioPath):
        self.__vl = self.axes.axvline(0, ls='-', color='g', lw=3, zorder=10)
        # reading the audio file
        raw = wave.open(audioPath)

        # reads all the frames
        # -1 indicates all or max frames
        signal = raw.readframes(-1)
        signal = np.frombuffer(signal, dtype="int16")

        # gets the frame rate
        f_rate = raw.getframerate()

        # to Plot the x-axis in seconds
        # you need get the frame rate
        # and divide by size of your signal
        # to create a Time Vector
        # spaced linearly with the size
        # of the audio file
        time = np.linspace(
            0,  # start
            len(signal) / f_rate,
            num=len(signal)
        )
        self.__canvas.figure.set_size_inches(
            (len(time)/f_rate), 1, forward=True)
        self.__canvas.resize((len(time)/f_rate)*100, 100)
        # actual plotting
        self.__totalW = len(signal)/f_rate
        self.axes.plot(time, signal)
        print((len(time)/f_rate))
        self.__canvas.draw()
