from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegExpValidator

from server.server import Server

class CreateListDialog(QtWidgets.QDialog):
    def __init__(self, updateTree):
        super(CreateListDialog, self).__init__()
        self.updateTree = updateTree
        self.setWindowTitle("Criar Lista")
        self.setGeometry(100, 100, 300, 50)
        self.buildProjectDict()
        self.createForm()
        self.createButtonBox()
        self.setMainLayout()     
        self.moveToCenter()   
        
    def buildProjectDict(self):
        server = Server()
        table = server.getTable("projects")
        self.projectIds = [project[0] for project in table]
        self.projectNames = [project[1] for project in table]
        self.projectDict = dict(zip(self.projectNames, self.projectIds))
    
    def createForm(self):
        self.projectBox = QtWidgets.QComboBox()
        self.projectBox.addItems(self.projectNames)
  
        self.name = QtWidgets.QLineEdit()
    
        reg = QRegExp("[a-z-A-Z-0-9_ ]+")
        validator = QRegExpValidator(reg, self.name)
        self.name.setValidator(validator)

        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Selecione o projeto:"), self.projectBox)
        layout.addRow(QtWidgets.QLabel("Nome da lista:"), self.name)
        self.formGroupBox = QtWidgets.QGroupBox("")
        self.formGroupBox.setLayout(layout)
    
    def createButtonBox(self):
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setMainLayout(self):
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def moveToCenter(self):
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())

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
            self.close()
        elif isNameEmpty:
            self.close()
            error = QtWidgets.QErrorMessage()
            error.showMessage("O campo nome é obrigatório!")
            error.exec_()
        elif isNameUsed:
            self.close()
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
        self.dialog = CreateListDialog(updateTree)
        self.triggered.connect(self.createList)

    def createList(self):
        self.dialog.exec_()


    