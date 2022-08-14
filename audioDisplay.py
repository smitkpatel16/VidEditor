import wave
import numpy as np
from PyQt6.QtWidgets import QWidget
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from processTools import SelectionLine
from PyQt6.QtWidgets import QGraphicsItem


class AudioGraph(FigureCanvas):
    def __init__(self, width=5, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_axis_off()
        self.__vl = self.axes.axvline(0, ls='-', color='r', lw=1, zorder=10)
        self.__duration = 0
        self.__totalW = 0
        self.__sl = []
    #     self.addSelection()

    # def addSelection(self):
    #     l1 = SelectionLine(0, 0, 0, 80)
    #     l1.setPos(0, 0)
    #     l1.setZValue(10000)
    #     l1.setFlag(
    #         QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
    #     self.__sl.append(l1)

    #     l2 = SelectionLine(0, 0, 0, 80)
    #     l2.setPos(10, 0)
    #     l2.setZValue(10000)
    #     l2.setFlag(
    #         QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
    #     self.__sl.append(l2)
    #     self.figure.addItem(l1)
    #     self.figure.addItem(l2)

    def setDuration(self, duration):
        self.__duration = duration
        self.setAudioPosition(0)

    def setAudioPosition(self, pos):
        if self.__duration:
            p = pos/self.__duration
            p = p*self.__totalW
            self.__vl.set_xdata([p, p])
            self.draw()

    def plotAudio(self, audioPath):
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
        # actual plotting
        self.__totalW = len(signal)/f_rate
        self.axes.plot(time, signal)
        self.draw()
