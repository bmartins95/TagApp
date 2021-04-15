import sys

from PyQt5 import QtWidgets

from interface import GuiWindow

def window():
    app = QtWidgets.QApplication(sys.argv)

    win = GuiWindow(app)

    win.show()
    sys.exit(app.exec_())

window()