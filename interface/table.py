import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from server.server import Server

class TagTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, text, lineId):
        super(TagTableWidgetItem, self).__init__(text)
        if text == "None":
            self.setText("")
        self.lineId = lineId

class IntItemDelegate(QtWidgets.QItemDelegate):
    def __init__(self):
        super(IntItemDelegate, self).__init__()
    
    def createEditor(self, parent, option, index):
        lineEdit = QtWidgets.QLineEdit(parent)
        reg = QRegExp("[0-9]+")
        validator = QRegExpValidator(reg, lineEdit)
        lineEdit.setValidator(validator)
        return lineEdit

class TagTable(QTableWidget):
    def __init__(self, id):
        super(TagTable, self).__init__()
        self.id = id
        self.wasChanged = False
        self.changeItems = list()
        self.lineIds = list()
        self.colNamesOnSql = ["tag", "type", "signal", "pid", "version"]
        self.loadTableFromServer()
        self.setValues()
        self.setHeaders()
        self.resizeWidth()
        self.setItemDelegateForColumn(4, IntItemDelegate())

        self.itemChanged.connect(self.onItemChanged)
    
    def loadTableFromServer(self):
        server = Server()
        self.table =  [list(line) for line in server.getLinesFromList(self.id)]
        for line in self.table:
            self.lineIds.append(line[0])
            line.pop(0)
    
    def setValues(self):
        nrow, ncolumn = len(self.table), len(self.table[0])
        self.setRowCount(nrow)
        self.setColumnCount(ncolumn)
        
        for i, row in enumerate(self.table):
            for j, column in enumerate(row):
                item = TagTableWidgetItem(str(column), self.lineIds[i])
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

    def onItemChanged(self, item):
        self.wasChanged = True
        self.changeItems.append(item) if item not in self.changeItems else None

    def save(self):
        server = Server()
        for item in self.changeItems:
            column = self.colNamesOnSql[item.column()]
            value = item.text() if item.column() != 4 else int(item.text())
            server.updateLine(column, value, item.lineId)
