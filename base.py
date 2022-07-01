# import QMainWindow and QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QApplication

from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtCore import QUrl
from PyQt6 import QtGui
# import QVBoxLayout and QHBoxLayout

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
        self.setGeometry(300, 300, 800, 600)
        # Add a menu bar
        self.__menu_bar = self.menuBar()
        self.__file_menu = self.__menu_bar.addMenu("File")

        open = QtGui.QAction("Open", self)
        self.__file_menu.addAction(open)
        open.triggered.connect(self.__openFile)

        # TODO: Define a central widget
        self.setCentralWidget(VidEditorMainWidget())
        self.show()

    def __openFile(self):
        file_name = QFileDialog.getOpenFileName(
            self, "Open File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        self.centralWidget()._videoPlayer.setSource(
            QUrl.fromLocalFile(file_name[0]))
        # self.centralWidget().__video_player.play()


# |-----------------------------------------------------------------------------|
# main executor :- runApplication
# |-----------------------------------------------------------------------------|
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VidEditorMainWindow()
    sys.exit(app.exec())
