from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import QRegExp, QEvent
from PyQt5.QtGui import QRegExpValidator

from server.server import Server
from interface.shortcuts.list import AddRowToListAction


class TagTableWidgetItem(QtWidgets.QTableWidgetItem):
    """Adds a lineId attribute and sets the text to a empty string if the 
    original text is None.
    """
    def __init__(self, text, lineId: int):
        super(TagTableWidgetItem, self).__init__(text)
        if text == "None":
            self.setText("")
        self.lineId = lineId


class IntItemDelegate(QtWidgets.QItemDelegate):
    """An QItemDelegate child class that allows only numbers to be inserted in
    the QLineEdit widget. This class is used in the version column of the 
    TagTable to filter the data sended by the user.
    """
    def __init__(self):
        super(IntItemDelegate, self).__init__()
    
    def createEditor(self, parent, option, index) -> QtWidgets.QLineEdit:
        """Allow only numbers in the QtWidgets.QLineEdit item."""
        lineEdit = QtWidgets.QLineEdit(parent)
        reg = QRegExp("[0-9]+")
        validator = QRegExpValidator(reg, lineEdit)
        lineEdit.setValidator(validator)
        return lineEdit


class TagTable(QTableWidget):
    """Loads all lines from the database lines table, where the id is the id 
    from which the lines belong. Those lines are later stored in a QTableWidegt
    object which can be later visualized in a Tab widget.
    """
    def __init__(self, id: int):
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
        self.installEventFilter(self)
        
        self.itemChanged.connect(self.onItemChanged)
    
    def loadTableFromServer(self):
        """Loads the lines that belongs to the table with listId = id and stores
        the information in the table variable.
        """
        server = Server()
        self.table =  [list(line) for line in server.getLinesFromList(self.id)]
        for line in self.table:
            self.lineIds.append(line[0])
            line.pop(0)
    
    def setValues(self):
        """Sets the number of row and columns of the widget and inserts the 
        values from table into the TagTable widget.
        """
        nrow, ncolumn = len(self.table), len(self.table[0])
        self.setRowCount(nrow)
        self.setColumnCount(ncolumn)
        
        for i, row in enumerate(self.table):
            for j, column in enumerate(row):
                item = TagTableWidgetItem(str(column), self.lineIds[i])
                self.setItem(i, j, item)
    
    def setHeaders(self):
        """Sets default values for the widget headers."""
        labels = ["TAG", "Tipo", "Sinal", "PID", "Versão"]
        self.setHorizontalHeaderLabels(labels)

    def resizeWidth(self):
        """Resizes the width of the columns to exactly fit the texts, later it
        takes this resized width and increases it by 20 percent.
        """
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        sectionSizes = []
        for i in range(0, self.columnCount()):
            sectionSizes.append(header.sectionSize(i))

        header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        for i in range(0, self.columnCount()):
            self.setColumnWidth(i, round(sectionSizes[i]*1.2))

    def eventFilter(self, source, event):
        """Checks if the right mouse button is pressed over the table, if it is,
        an menu containg the AddRowToListAction is shown.
        """
        if event.type() == QEvent.ContextMenu:
            menu = QtWidgets.QMenu()
            menu.addAction(AddRowToListAction(self))
            menu.exec_(event.globalPos())
            return True
        return super().eventFilter(source, event)

    def addRow(self):
        """Checks if the current number of rows in the TagTable widget is less
        than 50, if it is, a row is added to the lines table on the server and 
        an empty row is added to the TagTable widget.
        """
        if self.rowCount() < 50:
            server = Server()
            server.addLine("", "", "", "", "NULL", self.id)
            
            for value in [line[0] for line in server.getLinesFromList(self.id)]:
                if value not in self.lineIds:
                    newId = value
            
            self.insertRow(self.rowCount())
            for column in range(0, self.columnCount()):
                item = TagTableWidgetItem("", newId)
                self.setItem(self.rowCount(), column, item)
        else:
            error = QtWidgets.QErrorMessage()
            message = "O número máximo de linhas permitidas em uma lista é 50!"
            error.showMessage(message)
            error.exec_()
    
    def getTableName(self) -> str:
        """Searchs for a list that has the same id as the TagTable id on the 
        lists table. Returns the list name.
        """
        server = Server()
        return server.getListName(self.id)

    def save(self):
        """Sends all changes made in the TagTable to the lines table in the 
        server.
        """
        server = Server()
        for item in self.changeItems:
            column = self.colNamesOnSql[item.column()]
            value = item.text() if item.column() != 4 else int(item.text())
            server.updateLine(column, value, item.lineId)
        self.wasChanged = False

    def onItemChanged(self, item):
        """When a item is changed the TagTableWidgetItem is added to changeItems
        and the wasChanged is defined as True.
        """
        self.wasChanged = True
        self.changeItems.append(item) if item not in self.changeItems else None

