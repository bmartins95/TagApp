import sys

from PyQt5.QtWidgets import QApplication

from interface.window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow(app)
    win.openList(1)
    win.openList(2)
    win.openProject(1)
    win.show()

    sys.exit(app.exec_())