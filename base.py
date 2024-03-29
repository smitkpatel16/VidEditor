import qdarktheme
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtMultimedia import QMediaPlayer
from buildTimeline import BuildTimeline
from mediaControl import MediaControls
from metaDisplay import MetaDisplay
from mediaPlayer import MediaPlayer
from processTools import ExtractImages
from processTools import checkDuration
from processTools import checkDurationAudio
from processTools import extractAudio


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
        self.__reelDisplay = MetaDisplay()
        self.__timeline = BuildTimeline()
        self.__threads = []
        self.__audioPath = None
        policy = QSizePolicy(QSizePolicy.Policy.Expanding,
                             QSizePolicy.Policy.Expanding)
        self.__avPlayer.setSizePolicy(policy)

        self.__initUI()

        self.__connectSignals()
        # Add a menu bar
        self.__createMenu()
        self.show()

    def __initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setCentralWidget(CentralWidget())
        self.centralWidget().addWidget(self.__avPlayer)
        self.__reelDisplay.setMaximumHeight(400)
        self.centralWidget().addWidget(self.__reelDisplay)
        self.centralWidget().addWidget(self.__mediaControls)
        self.centralWidget().addWidget(self.__timeline)

    def __createMenu(self):
        self.__menuBar = self.menuBar()
        self.__fileMenu = self.__menuBar.addMenu("File")

        openVideo = QAction("Open Video", self)
        self.__fileMenu.addAction(openVideo)
        openVideo.triggered.connect(self.__openVideoFile)

        openAudio = QAction("Open Audio", self)
        self.__fileMenu.addAction(openAudio)
        openAudio.triggered.connect(self.__openAudioFile)

        self.__selectMenu = self.__menuBar.addMenu("Select")

        selectVideo = QAction("Select Video", self)
        self.__selectMenu.addAction(selectVideo)
        selectVideo.triggered.connect(self.__reelDisplay.addSelection)

        selectAudio = QAction("Select Audio", self)
        self.__selectMenu.addAction(selectAudio)
        # selectAudio.triggered.connect(self.__showAudio.addSelection)

    def closeEvent(self, event):
        # self.__avPlayer.stop()
        event.accept()

    def __openVideoFile(self):
        fileName = QFileDialog.getOpenFileName(
            self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if fileName[0]:
            self.__imageExtract = ExtractImages()
            self.__reelDisplay.clearDisplay()
            self.__imageExtract.reelImage.connect(self.__reelDisplay.addImage)
            self.__avPlayer.videoPlayer.setSource(
                QUrl.fromLocalFile(fileName[0]))
            self.__audioPath = extractAudio(filePath=fileName[0])
            duration = checkDuration(fileName[0])
            s = duration
            # s = int(duration.split(':')[0])*3600 + \
            #     int(duration.split(':')[1])*60 + \
            #     int(duration.split(':')[2])
            self.__mediaControls.setVideoDuration(s*1000)
            self.__imageExtract.fPath = fileName[0]
            self.__threads.append(QThread(self))
            t = self.__threads[-1]
            self.__imageExtract.moveToThread(t)
            self.__imageExtract.finished.connect(t.quit)
            self.__imageExtract.finished.connect(
                self.__imageExtract.deleteLater)
            self.__imageExtract.finished.connect(self.__displayAudioWave)
            self.__reelDisplay.setDuration(s*1000)
            t.finished.connect(t.deleteLater)
            t.started.connect(self.__imageExtract.run)
            t.start()
        # self.centralWidget().__video_player.play()

    def __displayAudioWave(self):
        duration = checkDurationAudio(self.__audioPath)
        self.__reelDisplay.plotAudio(self.__audioPath, duration*1000)
        self.__avPlayer.audioPlayer.setSource(
            QUrl.fromLocalFile(self.__audioPath))
        self.__mediaControls.setAudioDuration(duration*1000)

    def __openAudioFile(self):
        fileName = QFileDialog.getOpenFileName(
            self, "Open Audio", "", "Audio Files (*.wav)")
        if fileName[0]:
            # this is intentionally done to sync up with video opening
            self.__audioPath = fileName[0]
            self.__displayAudioWave()

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
        self.__avPlayer.videoPlayer.stopped.connect(
            self.__mediaControls.stopVideo)

        self.__mediaControls.seekVideo.connect(self.__avPlayer.seekVideo)
        self.__mediaControls.seekAudio.connect(self.__avPlayer.seekAudio)
        self.__mediaControls.adjustVolume.connect(self.__avPlayer.adjustVolume)

        self.__avPlayer.audioPlayer.positionChanged.connect(
            self.__mediaControls.setAudioPlayPosition)
        self.__avPlayer.videoPlayer.mediaStatusChanged.connect(
            self.__mediaControls.setVideoState)
        self.__avPlayer.videoPlayer.mediaStatusChanged.connect(
            self.__setVideoState)
        self.__avPlayer.audioPlayer.mediaStatusChanged.connect(
            self.__mediaControls.setAudioState)

        self.__reelDisplay.selectionMarked.connect(
            self.__avPlayer.videoPlayer.addSelection)
        self.__reelDisplay.clearSelection.connect(
            self.__avPlayer.videoPlayer.clearSelection)
        self.__reelDisplay.selectionMarked.connect(
            self.__timeline.addSelectionVideo)
        self.__reelDisplay.clearSelection.connect(
            self.__timeline.clearSelectionVideo)

    def __setVideoState(self, state):
        self.__mediaControls.setVideoState(state)
        if state == QMediaPlayer.MediaStatus.EndOfMedia:
            self.__avPlayer.videoPlayer.positionChanged.disconnect()
        if state == QMediaPlayer.MediaStatus.BufferedMedia or state == QMediaPlayer.MediaStatus.BufferingMedia:
            self.__avPlayer.videoPlayer.positionChanged.connect(
                self.__mediaControls.setVideoPlayPosition)
            self.__avPlayer.videoPlayer.positionChanged.connect(
                self.__reelDisplay.setActive)
            self.__avPlayer.videoPlayer.positionChanged.connect(
                self.__timeline.seekSliderVideo)


# |-----------------------------------------------------------------------------|
# main executor :- runApplication
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VideoEditorMainWindow()
    app.setStyleSheet(qdarktheme.load_stylesheet())
    sys.exit(app.exec())
