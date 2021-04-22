from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QKeySequence


from server.server import Server
from .dialog import MyDialog

class CreateListDialog(MyDialog):
    def __init__(self, updateTree):
        super(CreateListDialog, self).__init__()
        self.updateTree = updateTree
        self.setWindowTitle("Criar Lista")
        self.setGeometry(100, 100, 400, 80)
        self.moveToCenter()   
    
    def createForm(self):
        self.projectBox = QtWidgets.QComboBox()
        self.projectBox.addItems(self.projectNames)
  
        self.name = QtWidgets.QLineEdit()
    
        reg = QRegExp("[a-zA-Z0-9\u00C0-\u00FF\s]+")
        validator = QRegExpValidator(reg, self.name)
        self.name.setValidator(validator)

        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Selecione o projeto:"), self.projectBox)
        layout.addRow(QtWidgets.QLabel("Nome da lista:"), self.name)
        self.formLayout = QtWidgets.QWidget()
        self.formLayout.setLayout(layout)

    def accept(self):
        self.close()
        isNameUsed =  self.checkListNameIsUsed()
        isNameEmpty = self.name.text().isspace() or not self.name.text()
        if not isNameUsed and not isNameEmpty:
            server = Server()
            listName = self.name.text()
            projectId = self.projectDict[self.projectBox.currentText()]
            server.addList(listName, projectId)
            
            listId = server.getListIdFromProject(listName, projectId)
            server.addLine("", "", "", "", "NULL", listId)

            self.updateTree(self.projectBox.currentText())
        elif isNameEmpty:
            error = QtWidgets.QErrorMessage()
            error.showMessage("O campo nome é obrigatório!")
            error.exec_()
        elif isNameUsed:
            error = QtWidgets.QErrorMessage()
            error.showMessage("Este nome já está sendo utilizado!")
            error.exec_()

    def checkListNameIsUsed(self):
        server = Server()
        listName = self.name.text()
        projectId = self.projectDict[self.projectBox.currentText()]
        id = server.getListIdFromProject(listName, projectId)
        return id > 0


class CreateListAction(QAction):
    def __init__(self, parent, updateTree):
        super(CreateListAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/create_list.png"), 
            "Criar lista",
            parent)
        self.updateTree = updateTree
        self.triggered.connect(self.createList)

    def createList(self):
        dialog = CreateListDialog(self.updateTree)
        dialog.exec_()

class SaveListAction(QAction):
    def __init__(self, parent, saveList, name="Salvar lista"):
        super(SaveListAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/save_list.png"), 
            name,
            parent)
        self.setShortcut(QKeySequence('Ctrl+S'))
        self.triggered.connect(saveList)

class SaveAllListsAction(QAction):
    def __init__(self, parent, saveAllLists, name="Salvar todas as listas"):
        super(SaveAllListsAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/save_all.png"), 
            name,
            parent)
        self.triggered.connect(saveAllLists)



    