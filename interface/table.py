import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget

from server.server import Server

class TagTable(QTableWidget):
    def __init__(self, id):
        super(TagTable, self).__init__()
        self.id = id    
        self.loadTableFromServer()
        self.setValues()
        self.setHeaders()
        self.resizeWidth()
    
    def loadTableFromServer(self):
        server = Server()
        self.table = server.getLinesFromList(self.id)

    def setValues(self):
        nrow, ncolumn = len(self.table), len(self.table[0])
        self.setRowCount(nrow)
        self.setColumnCount(ncolumn)
        
        for i, row in enumerate(self.table):
            for j, column in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(column))
                self.setItem(i, j, item)
    
    def setHeaders(self):
        labels = ["TAG", "Tipo", "Sinal", "PID", "Versão"]
        self.setHorizontalHeaderLabels(labels)

    def resizeWidth(self):
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        sectionSizes = []
        for i in range(0, self.columnCount()):
            sectionSizes.append(header.sectionSize(i))

        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        for i in range(0, self.columnCount()):
            self.setColumnWidth(i, round(sectionSizes[i]*1.2))

    def getTableName(self):
        server = Server()
        return server.getListName(self.id)