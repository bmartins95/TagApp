from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

class CreateProjectDialog(QtWidgets.QDialog):
    def __init__(self):
        super(CreateProjectDialog, self).__init__()
        self.setWindowTitle("Criar Projeto")
        self.setGeometry(100, 100, 100, 50)
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.createForm()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

    

class CreateProjectAction(QAction):
    def __init__(self, parent):
        super(CreateProjectAction, self).__init__( 
            QIcon("./interface/shortcuts/icons/create_folder.png"), 
            "Criar Projeto",
            parent)
        self.setShortcut('Ctrl+N')
        self.triggered.connect(self.createProject)

    def createProject(self):


    