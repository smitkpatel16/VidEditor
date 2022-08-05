from mediaControl import MediaControls
from metaDisplay import MetaDisplay
from mediaPlayer import MediaPlayer
from processTools import ExtractImages
from processTools import checkDuration
from audioDisplay import AudioGraph
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
        self.__avPlayer = MediaPlayer()
        self.setGeometry(300, 300, 800, 600)
        # Add a menu bar
        self.__menuBar = self.menuBar()
        self.__fileMenu = self.__menuBar.addMenu("File")
        self.__reelDisplay = MetaDisplay()
        openVideo = QAction("Open Video", self)
        self.__fileMenu.addAction(openVideo)
        openVideo.triggered.connect(self.__openVideoFile)

        openAudio = QAction("Open Audio", self)
        self.__fileMenu.addAction(openAudio)
        openAudio.triggered.connect(self.__openAudioFile)

        self.setCentralWidget(CentralWidget())
        self.centralWidget().addWidget(self.__avPlayer)
        policy = QSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Expanding)
        self.__avPlayer.setSizePolicy(policy)
        self.__reelDisplay.setMaximumHeight(100)
        self.centralWidget().addWidget(self.__reelDisplay)
        self.centralWidget().addWidget(self.__mediaControls)

        self.__threads = []
        self.__imageExtract = ExtractImages()
        self.__showAudio = AudioGraph()
        self.centralWidget().addWidget(self.__showAudio)
        self.__connectSignals()
        self.show()
    # close the video player thread if active

    def closeEvent(self, event):
        # self.__avPlayer.stop()
        event.accept()

    def __openVideoFile(self):
        fileName = QFileDialog.getOpenFileName(
            self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if fileName[0]:
            self.__avPlayer.videoPlayer.setSource(
                QUrl.fromLocalFile(fileName[0]))
            duration = checkDuration(fileName[0])
            s = int(duration.split(':')[0])*3600 + \
                int(duration.split(':')[1])*60 + \
                int(duration.split(':')[2])
            self.__mediaControls.setVideoDuration(s*1000)
            self.__imageExtract.fPath = fileName[0]
            self.__threads.append(QThread(self))
            t = self.__threads[-1]
            self.__imageExtract.moveToThread(t)
            self.__imageExtract.finished.connect(t.quit)
            self.__imageExtract.finished.connect(
                self.__imageExtract.deleteLater)
            self.__reelDisplay.setDuration(s*1000)
            t.finished.connect(t.deleteLater)
            t.started.connect(self.__imageExtract.run)
            t.start()
        # self.centralWidget().__video_player.play()

    def __openAudioFile(self):
        fileName = QFileDialog.getOpenFileName(
            self, "Open Audio", "", "Audio Files (*.mp3 *.wav *.flac)")
        if fileName[0]:
            self.__avPlayer.audioPlayer.setSource(
                QUrl.fromLocalFile(fileName[0]))
            duration = checkDuration(fileName[0])
            s = int(duration.split(':')[0])*3600 + \
                int(duration.split(':')[1])*60 + \
                int(duration.split(':')[2])
            self.__mediaControls.setAudioDuration(s*1000)
            self.__showAudio.plotAudio(fileName[0])
            self.__showAudio.setDuration(s*1000)

    def __connectSignals(self):
        self.__mediaControls.playVideo.connect(
            self.__avPlayer.videoPlayer.play)
        self.__mediaControls.pauseVideo.connect(
            self.__avPlayer.videoPlayer.pause)
        self.__mediaControls.playAudio.connect(
            self.__avPlayer.audioPlayer.play)
        self.__mediaControls.pauseAudio.connect(
            self.__avPlayer.audioPlayer.pause)

        self.__mediaControls.playAll.connect(
            self.__avPlayer.videoPlayer.play)
        self.__mediaControls.playAll.connect(
            self.__avPlayer.audioPlayer.play)
        self.__mediaControls.pauseAll.connect(
            self.__avPlayer.videoPlayer.pause)
        self.__mediaControls.pauseAll.connect(
            self.__avPlayer.audioPlayer.pause)

        self.__mediaControls.seekVideo.connect(self.__avPlayer.seekVideo)
        self.__mediaControls.seekAudio.connect(self.__avPlayer.seekAudio)
        self.__mediaControls.adjustVolume.connect(self.__avPlayer.adjustVolume)
        self.__imageExtract.reelImage.connect(self.__reelDisplay.addImage)

        self.__avPlayer.audioPlayer.audioPlayPosition.connect(
            self.__mediaControls.setAudioPlayPosition)
        self.__avPlayer.videoPlayer.videoPlayPosition.connect(
            self.__mediaControls.setVideoPlayPosition)
        self.__avPlayer.videoPlayer.videoPlayPosition.connect(
            self.__reelDisplay.setActive)
        self.__avPlayer.audioPlayer.audioPlayPosition.connect(
            self.__showAudio.setAudioPosition)

        self.__avPlayer.videoPlayer.mediaStatusChanged.connect(
            self.__mediaControls.setVideoState)
        self.__avPlayer.audioPlayer.mediaStatusChanged.connect(
            self.__mediaControls.setAudioState)


# |-----------------------------------------------------------------------------|
# main executor :- runApplication
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VideoEditorMainWindow()
    sys.exit(app.exec())
