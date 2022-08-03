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
        self.__iw = 0

    # add image to the scene
    def addImage(self, qImg):
        pm = QPixmap.fromImage(qImg)
        pmi = self.display.addPixmap(pm)
        pmi.setPos(self.__count * pm.width(), 0)
        if not self.__r:
            self.__r = self.display.addRect(
                0, 0, pm.width(), pm.height(), self.__pen, self.__brush)
            self.__r.setZValue(10000)
            self.__iw = pm.width()
        self.__count += 1

    def setActive(self, c):
        print("setActive", c)
        self.__r.setPos(c * self.__iw, 0)
