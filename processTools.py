from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QApplication
import cv2
import math
from pathlib import Path
import win32com.client
sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)

# ===============================================================================
# ProcessTools- A collection of methods for processing audio/video files
# ===============================================================================


class ExtractImages(QObject):
    reelImage = pyqtSignal(QImage)
    fPath = None
    finished = pyqtSignal()

    def run(self):
        """
        Extracts images from a video file and saves them to a folder.
        :param filePath: The path to the video file.
        :param outputPath: The path to the folder where the images will be saved.
        :param imageType: The type of image to extract.
        :return: imageArray
        """
        capture = cv2.VideoCapture(self.fPath)
        # get equally spaced frames from the video
        frameCount = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        fW = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        fH = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        r = fW / fH
        if frameCount < 200:
            frameInterval = 1
        else:
            frameInterval = math.ceil(frameCount / 100)
        success, image = capture.read()
        count = 0

        while success:
            if count % frameInterval == 0 or count == 0:
                height, width, channel = image.shape
                bytesPerLine = 3 * width
                qImg = QImage(image.data, width, height,
                              bytesPerLine, QImage.Format.Format_BGR888)
                self.reelImage.emit(qImg.scaled(r * 80, 80))
            success, image = capture.read()
            count += 1
        self.finished.emit()


def checkDuration(filePath):
    """
    Checks the duration of a video file.
    :param filePath: The path to the video file.
    :return: duration
    """
    # get the meta info for the selected video
    # file = Path(filePath)
    # ns = sh.NameSpace(str(file.parent))
    # item = ns.ParseName(str(file.name))
    # colnum = 0
    # columns = []
    # while True:
    #     colname = ns.GetDetailsOf(None, colnum)
    #     if not colname:
    #         break
    #     columns.append(colname)
    #     colnum += 1
    # metaData = {}

    # for colnum in range(len(columns)):
    #     colval = ns.GetDetailsOf(item, colnum)
    #     if colval:
    #         metaData[columns[colnum].lower()] = colval
    # # length or duration of the video
    # duration = metaData.get('length') or metaData.get('duration')
    # return duration
    capture = cv2.VideoCapture(filePath)
    frameCount = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    frameRate = capture.get(cv2.CAP_PROP_FPS)
    dur = frameCount/frameRate
    return round(dur, 3)

# find duration of the audio file using wave module


def checkDurationAudio(filePath):
    """
    Checks the duration of a audio file.
    :param filePath: The path to the audio file.
    :return: duration
    """
    import wave
    raw = wave.open(filePath)
    f_rate = raw.getframerate()
    f_length = raw.getnframes() / f_rate
    return round(f_length, 3)


# ===============================================================================
# SelectionLine- Inherited QGraphicsLineItem for selection movement
# ===============================================================================
class SelectionLine(QGraphicsLineItem):
    updateHighlight = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPen(QPen(Qt.GlobalColor.red, 3))
        self.setFlags(
            self.GraphicsItemFlag.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)

    def itemChange(self, change, value):
        if change == self.GraphicsItemChange.ItemPositionChange:
            # restrict vertical movement
            value.setY(0)
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.SizeHorCursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        return super().hoverLeaveEvent(event)
