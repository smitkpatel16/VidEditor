import wave
import numpy as np
from PyQt6.QtWidgets import QWidget
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class AudioGraph(FigureCanvas):
    def __init__(self, width=5, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_axis_off()

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
        self.axes.plot(time, signal)
        self.draw()
