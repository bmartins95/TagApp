from PyQt5 import QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtGui import QIcon

from server.server import Server

class CreateProjectDialog(QtWidgets.QDialog):
    def __init__(self):
        super(CreateProjectDialog, self).__init__()
        self.setWindowTitle("Criar Projeto")
        self.setGeometry(100, 100, 300, 50)
        self.createForm()
        self.createButtonBox()
        self.setMainLayout()     
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
    
    def createButtonBox(self):
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.getInfo)
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

    def getInfo(self):
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


class CreateProjectAction(QAction):
    def __init__(self, parent):
        super(CreateProjectAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/create_project.png"), 
            "Criar projeto",
            parent)
        self.setShortcut('Ctrl+N')
        self.triggered.connect(self.createProject)

    def createProject(self):
        dialog = CreateProjectDialog()
        dialog.exec_()


    