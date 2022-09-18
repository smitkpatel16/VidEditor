# qt dailog box to select or update audio file
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt


# ==============================================================================
# SelectAudio - class to select or update audio wave
# ==============================================================================
class SelectAudio(QDialog):
    def __init__(self, parent):
        super(SelectAudio, self).__init__(
            parent, Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle('Select Audio')
        self.setLayout(QVBoxLayout())
        self.initUI()
        self.overridePath = None
        self.__connectSignals()

    def initUI(self):
        self.__basicSelect = QGroupBox("Audio", self)
        self.__basicSelect.setLayout(QGridLayout(self))
        w = QPushButton("Ovewrite Existing", self)
        w.setCheckable(True)
        w.setChecked(False)
        self.__basicSelect.layout().addWidget(w, 0, 0)
        w = QPushButton("Add New", self)
        w.setCheckable(True)
        self.__basicSelect.layout().addWidget(w, 0, 1)
        w.setChecked(True)
        self.layout().addWidget(self.__basicSelect)
        self.__c = QComboBox(self)
        self.__c.hide()
        self.__c.activated.connect(self.__selectedPath)
        self.layout().addWidget(self.__c)

        hb = QHBoxLayout(self)
        self.layout().addLayout(hb)
        ok = QPushButton("OK", self)
        hb.addWidget(ok)
        ok.clicked.connect(self.__final)
        cancel = QPushButton("Cancel", self)
        hb.addWidget(cancel)
        cancel.clicked.connect(self.__final)

    def updatePaths(self, existingPaths):
        self.__c.clear()
        self.__c.addItems(existingPaths)
        self.__c.hide()

    def __final(self):
        if self.sender().text() == "OK":
            self.accept()
        else:
            self.reject()

    def __connectSignals(self):
        for child in self.__basicSelect.children():
            if isinstance(child, QPushButton):
                child.clicked.connect(self.__onSelect)

    def __onSelect(self):
        if self.sender().text() == "Ovewrite Existing":
            self.__c.show()
            self.overridePath = self.__c.currentText()
        else:
            self.overridePath = None

    def __selectedPath(self, i):
        self.overridePath = self.__c.currentText()
