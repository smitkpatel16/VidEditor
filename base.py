# import QMainWindow and QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QVBoxLayout

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction

from videoPlayer import VidPlayer
from mediaControl import MediaControls


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

        open = QAction("Open", self)
        self.__fileMenu.addAction(open)
        open.triggered.connect(self.__openFile)

        self.setCentralWidget(CentralWidget())
        self.centralWidget().addWidget(self.__vidPlayer)
        self.centralWidget().addWidget(self.__mediaControls)

        self.__connectSignals()

        self.show()

    def __openFile(self):
        file_name = QFileDialog.getOpenFileName(
            self, "Open File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        self.__vidPlayer.videoPlayer.setSource(
            QUrl.fromLocalFile(file_name[0]))
        # self.centralWidget().__video_player.play()

    def __connectSignals(self):
        self.__mediaControls.play.connect(self.__vidPlayer.videoPlayer.play)
        self.__mediaControls.pause.connect(self.__vidPlayer.videoPlayer.pause)
        self.__mediaControls.stop.connect(self.__vidPlayer.videoPlayer.stop)
        self.__mediaControls.seek.connect(
            self.__vidPlayer.videoPlayer.setPosition)
        self.__mediaControls.volume.connect(
            self.__vidPlayer.audio.setVolume)
        self.__mediaControls.mute.connect(
            self.__vidPlayer.audio.setMuted)


# |-----------------------------------------------------------------------------|
# main executor :- runApplication
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VideoEditorMainWindow()
    sys.exit(app.exec())
