from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import pyqtSignal
from processTools import SelectionLine


# create a qgraphicsview widget to display reel of images array
# ===============================================================================
# MetaDisplay -
# ===============================================================================


class MetaDisplay(QGraphicsView):
    selectionMarked = pyqtSignal(tuple)
    clearSelection = pyqtSignal()

    # constructor
    def __init__(self, parent=None):
        super(MetaDisplay, self).__init__(parent)
        self.display = QGraphicsScene()
        self.setScene(self.display)
        self.__count = 0
        self.__pen = QPen(Qt.GlobalColor.green, 3)
        self.__r = None
        self.__totalW = 0
        self.__sl = []
        self.__selection = []
        self.__duration = 0

    # add selection range

    def addSelection(self):
        l1 = SelectionLine(0, 0, 0, 80)
        l1.setPos(0, 0)
        l1.setZValue(10000)
        l1.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.__sl.append(l1)

        l2 = SelectionLine(0, 0, 0, 80)
        l2.setPos(10, 0)
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

        for i, j in enumerate(range(0, len(self.__sl), 2)):
            x = self.__sl[j].scenePos().x()
            y = 0
            w = self.__sl[i*2+1].scenePos().x()-x
            h = 80
            start = (x/self.__totalW) * self.__duration
            end = ((x+w)/self.__totalW) * self.__duration
            self.selectionMarked.emit((int(start), int(end)))
            self.__selection.append(self.display.addRect(x, y, w, h, QPen(
                Qt.GlobalColor.red, 1), QBrush(QColor(255, 127, 127, 127))))
            # add image to the scene

    def addImage(self, qImg):
        pm = QPixmap.fromImage(qImg)
        pmi = self.display.addPixmap(pm)
        pmi.setPos(self.__count * pm.width(), 0)
        if not self.__r:
            self.__r = self.display.addLine(
                0, 0, 0, pm.height(), self.__pen)
            self.__r.setZValue(5000)
        self.__count += 1
        self.__totalW += pm.width()

    def setDuration(self, duration):
        self.__duration = duration

    def setActive(self, c):
        if self.__duration:
            p = round(c/self.__duration, 3)
            p = p*self.__totalW
            self.__r.setPos(p, 0)
