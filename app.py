import sys

from PyQt5.QtWidgets import QApplication

from interface.window import MainWindow
from server.server import Server

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow(app)
    win.openList(1)
    win.openList(2)
    win.openProject(1)
    win.show()

    server = Server()
    print(server.getTable("projects"))

    sys.exit(app.exec_())