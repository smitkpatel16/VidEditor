from mediaControl import MediaControls
from metaDisplay import MetaDisplay
from videoPlayer import VidPlayer
from processTools import ExtractImages
from processTools import checkDuration
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow

# import QMainWindow and QApplication


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Editor')
        self.resize(800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.show()

    def addWidget(self, widget):
        self.layout.addWidget(widget)


# ===============================================================================
# VideoEditorMainWindow- Inherits from QMainWindow
# ===============================================================================


class VideoEditorMainWindow(QMainWindow):
    '''
    Qt MainWindow for VideoEditor
    '''

    def __init__(self, parent=None):
        super(VideoEditorMainWindow, self).__init__(parent)
        self.setWindowTitle("Video Editor")
        self.__mediaControls = MediaControls()
        self.__vidPlayer = VidPlayer()
        self.setGeometry(300, 300, 800, 600)
        # Add a menu bar
        self.__menuBar = self.menuBar()
        self.__fileMenu = self.__menuBar.addMenu("File")
        self.__reelDisplay = MetaDisplay()
        open = QAction("Open", self)
        self.__fileMenu.addAction(open)
        open.triggered.connect(self.__openFile)

        self.setCentralWidget(CentralWidget())
        self.centralWidget().addWidget(self.__vidPlayer)
        policy = QSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Expanding)
        self.__vidPlayer.setSizePolicy(policy)
        self.__reelDisplay.setMaximumHeight(100)
        self.centralWidget().addWidget(self.__reelDisplay)
        self.centralWidget().addWidget(self.__mediaControls)

        self.__connectSignals()
        self.__w = None
        self.__t = None
        self.show()
    # close the video player thread if active

    def closeEvent(self, event):
        self.__vidPlayer.stop()
        event.accept()

    def __openFile(self):
        file_name = QFileDialog.getOpenFileName(
            self, "Open File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        self.__vidPlayer.videoPlayer.setSource(
            QUrl.fromLocalFile(file_name[0]))
        duration = checkDuration(file_name[0])
        s = int(duration.split(':')[0])*3600 + \
            int(duration.split(':')[1])*60 + \
            int(duration.split(':')[2])
        self.__mediaControls.setDuration(s*1000)
        self.__w = ExtractImages()
        self.__w.fPath = file_name[0]
        self.__t = QThread()
        self.__w.moveToThread(self.__t)
        self.__t.started.connect(self.__w.run)
        self.__w.reelImage.connect(self.__reelDisplay.addImage)
        self.__t.start()
        # self.centralWidget().__video_player.play()

    def __connectSignals(self):
        self.__mediaControls.play.connect(self.__vidPlayer.play)
        self.__mediaControls.pause.connect(self.__vidPlayer.pause)
        self.__mediaControls.stop.connect(self.__vidPlayer.stop)
        self.__mediaControls.seek.connect(
            self.__vidPlayer.videoPlayer.setPosition)
        self.__mediaControls.volume.connect(
            self.__vidPlayer.audio.setVolume)
        self.__mediaControls.mute.connect(
            self.__vidPlayer.audio.setMuted)
        self.__vidPlayer.playPosition.connect(
            self.__mediaControls.setPlayPosition)
        self.__mediaControls.completion.connect(self.__reelDisplay.setActive)


# |-----------------------------------------------------------------------------|
# main executor :- runApplication
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VideoEditorMainWindow()
    sys.exit(app.exec())
