import wave
import numpy as np
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QPolygonF
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QPointF
from processTools import SelectionLine
from audioSelect import SelectAudio


# create a qgraphicsview widget to display reel of images array
# ===============================================================================
# MetaDisplay -
# ===============================================================================


class MetaDisplay(QGraphicsView):
    selectionMarked = pyqtSignal(list)
    clearSelection = pyqtSignal()
    calledCount = 0
    # constructor

    def __init__(self, parent=None):
        super(MetaDisplay, self).__init__(parent)
        self.display = QGraphicsScene()
        self.setScene(self.display)
        self.__pen = QPen(Qt.GlobalColor.green, 3)
        self.__audioPens = [QPen(Qt.GlobalColor.blue, 2), QPen(
            Qt.GlobalColor.red, 2), QPen(Qt.GlobalColor.yellow, 2)]
        self.__selectAudio = SelectAudio(self)
        self.clearDisplay()

    # add selection range

    def clearDisplay(self):
        # to clear out when a new video is opened (only 1 supported currently)
        self.__count = 0
        self.__totalW = 0
        self.__r = None
        self.__sl = []
        self.__selection = []
        self.__duration = 0
        self.__audioWave = []
        self.display.clear()

    def addSelection(self):
        viewportRect = self.viewport().rect()
        visibleSceneRect = self.mapToScene(viewportRect).boundingRect()
        visibleX = visibleSceneRect.x()+visibleSceneRect.width()//2
        l1 = SelectionLine(0, 0, 0, 80)
        l1.setPos(visibleX, 0)
        l1.setZValue(10000)
        l1.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.__sl.append(l1)

        l2 = SelectionLine(0, 0, 0, 80)
        l2.setPos(visibleX+10, 0)
        l2.setZValue(10000)
        l2.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.__sl.append(l2)
        self.display.addItem(l1)
        self.display.addItem(l2)
        self.__highlight()

    # highlight the selected area

    def mouseMoveEvent(self, event):
        self.__highlight()
        return super().mouseMoveEvent(event)

    def __highlight(self):
        for s in self.__selection:
            self.display.removeItem(s)
        self.__selection.clear()
        self.clearSelection.emit()
        self.__sl = sorted(self.__sl, key=lambda p: p.x())
        selection = []
        for i, j in enumerate(range(0, len(self.__sl), 2)):
            x = self.__sl[j].scenePos().x()
            y = 0
            w = self.__sl[i*2+1].scenePos().x()-x
            h = 80
            start = (x/self.__totalW) * self.__duration
            end = ((x+w)/self.__totalW) * self.__duration
            selection.append((start, end))
            self.__selection.append(self.display.addRect(x, y, w, h, QPen(
                Qt.GlobalColor.red, 1), QBrush(QColor(255, 127, 127, 127))))
            # add image to the scene
        self.selectionMarked.emit(selection)

    def addImage(self, qImg):
        pm = QPixmap.fromImage(qImg)
        pmi = self.display.addPixmap(pm)
        pmi.setPos(self.__count * pm.width(), 0)
        self.__count += 1
        self.__totalW += pm.width()

    def setDuration(self, duration):
        self.__duration = duration

    def setActive(self, c):
        if self.__duration:
            # viewportRect = self.viewport().rect()
            # visibleSceneRect = self.mapToScene(viewportRect).boundingRect()
            p = round(c/self.__duration, 3)
            p = p*self.__totalW
            # if p > visibleSceneRect.x() + visibleSceneRect.width() or p < visibleSceneRect.x():
            self.centerOn(p, 0)
            self.__r.setPos(p, 0)

    def plotAudio(self, audioPath, duration):
        if self.__audioWave:
            self.__selectAudio.updatePaths([p[0] for p in self.__audioWave])
            c = self.__selectAudio.exec()
            if c == QDialog.DialogCode.Accepted:
                op = self.__selectAudio.overridePath
            else:
                return
        else:
            op = None
        # reading the audio file
        raw = wave.open(audioPath)

        # reads all the frames
        # -1 indicates all or max frames
        signal = raw.readframes(-1)
        signal = np.frombuffer(signal, dtype="int16")

        # gets the frame rate
        # f_rate = raw.getframerate()

        # to Plot the x-axis in seconds
        # you need get the frame rate
        # and divide by size of your signal
        # to create a Time Vector
        # spaced linearly with the size
        # of the audio file
        time = np.linspace(
            0,  # start
            (duration/self.__duration)*self.__totalW,
            num=len(signal)
        )
        plotted = None
        polyline = QPolygonF()
        if not op:
            align = len(self.__audioWave) + 1
        else:
            for i, v in enumerate(self.__audioWave):
                if v[0] == op:
                    align = i + 1
                    self.display.removeItem(v[1])
        for x, y in zip(time, signal):
            if not plotted:
                plotted = x
                polyline.append(QPointF(x, 160*align+y*0.002))
            else:
                if x-plotted > 1:
                    plotted = None
        p = len(self.__audioWave) % 3
        poly = self.display.addPolygon(
            polyline, self.__audioPens[p])
        self.__audioWave.append((audioPath, poly))

        if op:
            for v in self.__audioWave:
                if v[0] == op:
                    self.__audioWave.remove(v)
                    break

        # readjust the active line length
        if self.__r:
            self.display.removeItem(self.__r)
        self.__r = self.display.addLine(
            0, 0, 0, 80+160*len(self.__audioWave), self.__pen)
        self.__r.setZValue(5000)
