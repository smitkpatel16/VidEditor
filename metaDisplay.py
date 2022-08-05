from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPen
from PyQt6.QtGui import QBrush
# create a qgraphicsview widget to display reel of images array
# ===============================================================================
# MetaDisplay -
# ===============================================================================


class MetaDisplay(QGraphicsView):
    # constructor
    def __init__(self, parent=None):
        super(MetaDisplay, self).__init__(parent)
        self.display = QGraphicsScene()
        self.setScene(self.display)
        self.__count = 0
        self.__pen = QPen(Qt.GlobalColor.green, 3)
        self.__brush = QBrush(QColor(127, 127, 255, 127))
        self.__r = None
        self.__totalW = 0

    # add image to the scene
    def addImage(self, qImg):
        pm = QPixmap.fromImage(qImg)
        pmi = self.display.addPixmap(pm)
        pmi.setPos(self.__count * pm.width(), 0)
        if not self.__r:
            self.__r = self.display.addRect(
                0, 0, pm.width(), pm.height(), self.__pen, self.__brush)
            self.__r.setZValue(10000)
        self.__count += 1
        self.__totalW += pm.width()

    def setDuration(self, duration):
        self.__duration = duration

    def setActive(self, c):
        p = c/self.__duration
        p = p*self.__totalW
        self.__r.setPos(p, 0)
