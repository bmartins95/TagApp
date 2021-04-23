from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QKeySequence

from .dialog import Dialog
from server.server import Server

class CreateProjectDialog(Dialog):
    """Opens a dialog that allows projects to be created."""
    def __init__(self):
        super(CreateProjectDialog, self).__init__()
        self.setWindowTitle("Criar Projeto")
        self.setGeometry(100, 100, 300, 50)
        self.moveToCenter()
        
    def createForm(self):
        """Creates the form widget the project name and description."""
        self.name = QtWidgets.QLineEdit()
        self.description = QtWidgets.QLineEdit()

        reg = QRegExp("[a-z-A-Z-0-9\u00C0-\u00FF\s]+")
        validator1 = QRegExpValidator(reg, self.name)
        validator2 = QRegExpValidator(reg, self.description)
        self.name.setValidator(validator1)
        self.description.setValidator(validator2)

        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Nome"), self.name)
        layout.addRow(QtWidgets.QLabel("Descrição"), self.description)
        self.formLayout = QtWidgets.QWidget()
        self.formLayout.setLayout(layout)

    def accept(self):
        """If the name is not used by another project and the string is not
        empty, the function add the project to the database.
        """
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

    def checkProjectExist(self) -> bool:
        """Checks if the name is used by another project."""
        server = Server()
        projects = [project[1] for project in server.getTable("projects")]
        return self.name.text() not in projects

class OpenProjectDialog(Dialog):
    """Opens a dialog that allows project to be loaded from the database to the
    ProjectTree. Receives the openProject function from 
    interface.window.MainWindow.
    """
    def __init__(self, openProject):
        super(OpenProjectDialog, self).__init__()
        self.openProject = openProject
        self.setWindowTitle("Abrir Projeto")
        self.setGeometry(100, 100, 300, 50)
        self.moveToCenter()
    
    def createForm(self):
        """Creates the form that contains a QComboBox with the names of all the
        projects currently available in the database.
        """
        self.projectBox = QtWidgets.QComboBox()
        self.projectBox.addItems(self.projectNames)
        
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Projeto"), self.projectBox)
        self.formLayout = QtWidgets.QWidget()
        self.formLayout.setLayout(layout)

    def accept(self):
        """Load the project into the ProjectTree."""
        self.close()
        isNotNone = self.projectBox.currentText() is not None
        isNotEmpty = self.projectBox.currentText()
        if isNotNone and isNotEmpty:
            self.openProject(self.projectDict[self.projectBox.currentText()])

class CloseProjectDialog(Dialog):
    """Opens a dialog that allows projects to be closed, i.e. removed from the
    ProjectTree. Receives the function closeProject from 
    interface.window.MainWindow.
    """
    def __init__(self, closeProject, getOpenProjectNames):
        self.closeProject = closeProject
        self.getOpenProjectNames = getOpenProjectNames
        super(CloseProjectDialog, self).__init__()
        self.setWindowTitle("Fechar Projeto")
        self.setGeometry(100, 100, 300, 50)
        self.moveToCenter()
    
    def createForm(self):
        """Creates the form that contains a QComboBox with the names of all the
        projects currently available in the database.
        """
        self.projectBox = QtWidgets.QComboBox()
        self.projectBox.addItems(self.getOpenProjectNames())
        
        layout = QtWidgets.QFormLayout()
        layout.addRow(QtWidgets.QLabel("Projeto"), self.projectBox)
        self.formLayout = QtWidgets.QWidget()
        self.formLayout.setLayout(layout)

    def accept(self):
        """Closes the project, i.e. removes it from the ProjectTree."""
        self.close()
        isEmpty = not self.projectBox.currentText() 
        if not isEmpty:
            self.closeProject(self.projectDict[self.projectBox.currentText()])

class CreateProjectAction(QAction):
    """Executes the CreateProjectDialog."""
    def __init__(self, parent, name="Criar projeto"):
        super(CreateProjectAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/create_project.png"), 
            name,
            parent)
        self.triggered.connect(self.createProject)

    def createProject(self):
        dialog = CreateProjectDialog()
        dialog.exec_()

class OpenProjectAction(QAction):
    """Executes the OpenProjectDialog."""
    def __init__(self, parent, name="Abrir projeto"):
        super(OpenProjectAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/open_project.png"), 
            name,
            parent)
        self.parent = parent
        self.triggered.connect(self.openProject)

    def openProject(self):
        dialog = OpenProjectDialog(self.parent.openProject)
        dialog.exec_()

class CloseProjectAction(QAction):
    """Executes the CloseProjectDialog. Sends closeProject function and 
    getOpenProjectNames to the CloseProjectDialog class."""
    def __init__(self, parent, getOpenProjectNames, name="Fecha projeto"):
        super(CloseProjectAction, self).__init__( 
            QIcon(""), 
            name,
            parent)
        self.getOpenProjectNames = getOpenProjectNames
        self.parent = parent
        self.setShortcut(QKeySequence('Ctrl+X'))
        self.triggered.connect(self.closeProject)

    def closeProject(self):
        dialog = CloseProjectDialog(self.parent.closeProject, 
            self.getOpenProjectNames)
        dialog.exec_()


    