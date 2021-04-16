import sys

from PyQt5 import QtWidgets

sys.path.append('..')
from server.server import Server

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, QApplication):
        super(MainWindow, self).__init__()
        self.width, self.height = self.getResolution(QApplication)
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("PyQt5 Teste")

    def getResolution(self, QApplication):
        screenResolution = QApplication.desktop().screenGeometry()
        return screenResolution.width(), screenResolution.height()

    def openListTable(self, id):
        server = Server("../server/database/teste.db")
        
        table = server.getLinesFromList(id)
        nrow, ncolumn = len(table), len(table[0])
        tableWidget = QtWidgets.QTableWidget(nrow, ncolumn)
        
        for rIndex, row in enumerate(table):
            for cIndex, column in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(column))
                tableWidget.setItem(rIndex, cIndex, item)
            
        
        labels = ["TAG", "Tipo", "Sinal", "PID", "Versão"]
        tableWidget.setHorizontalHeaderLabels(labels)

        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        sectionSizes = []
        for i in range(0, tableWidget.columnCount()):
            sectionSizes.append(header.sectionSize(i))

        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        for i in range(0, tableWidget.columnCount()):
            tableWidget.setColumnWidth(i, round(sectionSizes[i]*1.2))        
        
        widget = QtWidgets.QWidget()
        
        grid = QtWidgets.QGridLayout()
        grid.addWidget(tableWidget, 0, 0) 
        
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow(app)
    win.openListTable(1)

    win.show()
    sys.exit(app.exec_())