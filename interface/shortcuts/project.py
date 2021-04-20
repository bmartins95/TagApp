from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegExpValidator

from interface.shortcuts.dialog import MyDialog
from server.server import Server

class CreateProjectDialog(MyDialog):
    def __init__(self):
        super(CreateProjectDialog, self).__init__()
        self.setWindowTitle("Criar Projeto")
        self.setGeometry(100, 100, 300, 50)
        self.moveToCenter()
        
    def createForm(self):
        self.name = QtWidgets.QLineEdit()
        self.description = QtWidgets.QLineEdit()

        reg = QRegExp("[a-z-A-Z-0-9_ ]+")
        validator1 = QRegExpValidator(reg, self.name)
        validator2 = QRegExpValidator(reg, self.description)
        self.name.setValidator(validator1)
        self.description.setValidator(validator2)

        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Nome"), self.name)
        layout.addRow(QtWidgets.QLabel("Descrição"), self.description)
        self.formGroupBox = QtWidgets.QGroupBox("")
        self.formGroupBox.setLayout(layout)

    def accept(self):
        isNameEmpty = self.name.text().isspace() or not self.name.text()
        if self.checkProjectExist() and not isNameEmpty:
            server = Server()
            server.addProject(self.name.text(), self.description.text())
            self.close()
        elif isNameEmpty:
            self.close()
            error = QtWidgets.QErrorMessage()
            error.showMessage("O campo nome é obrigatório!")
            error.exec_()
        else:
            self.close()
            error = QtWidgets.QErrorMessage()
            error.showMessage("Este nome já está sendo utilizado!")
            error.exec_()

    def checkProjectExist(self):
        server = Server()
        projects = [project[1] for project in server.getTable("projects")]
        return self.name.text() not in projects

class OpenProjectDialog(MyDialog):
    def __init__(self, openProject):
        super(OpenProjectDialog, self).__init__()
        self.openProject = openProject
        self.setWindowTitle("Abrir Projeto")
        self.setGeometry(100, 100, 300, 50)
        self.moveToCenter()
        
    def createProjectDict(self):
        server = Server()
        table = server.getTable("projects")
        self.projectIds = [project[0] for project in table]
        self.projectNames = [project[1] for project in table]
        self.projectDict = dict(zip(self.projectNames, self.projectIds))
    
    def createForm(self):
        self.projectBox = QtWidgets.QComboBox()
        self.projectBox.addItems(self.projectNames)
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Projeto"), self.projectBox)
        self.formGroupBox = QtWidgets.QGroupBox("")
        self.formGroupBox.setLayout(layout)

    def accept(self):
        self.close()
        self.openProject(self.projectDict[self.projectBox.currentText()])

class CreateProjectAction(QAction):
    def __init__(self, parent):
        super(CreateProjectAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/create_project.png"), 
            "Criar projeto",
            parent)
        self.setShortcut('Ctrl+P')
        self.triggered.connect(self.createProject)

    def createProject(self):
        dialog = CreateProjectDialog()
        dialog.exec_()

class OpenProjectAction(QAction):
    def __init__(self, parent):
        super(OpenProjectAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/open_project.png"), 
            "Abrir projeto",
            parent)
        self.parent = parent
        self.setShortcut('Ctrl+O')
        self.triggered.connect(self.openProject)

    def openProject(self):
        dialog = OpenProjectDialog(self.parent.openProject)
        dialog.exec_()


    