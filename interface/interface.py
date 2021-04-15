import sys

from PyQt5 import QtWidgets


class GuiWindow(QtWidgets.QMainWindow):
    def __init__(self, QApplication):
        super(GuiWindow, self).__init__()
        width, height = self.getResolution(QApplication)
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle("PyQt5 Teste")

    def getResolution(self, QApplication):
        screenResolution = QApplication.desktop().screenGeometry()
        return screenResolution.width(), screenResolution.height()