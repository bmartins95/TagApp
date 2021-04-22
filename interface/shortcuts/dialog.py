from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox

from server.server import Server

class MyDialog(QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        self.setWindowTitle("Default Title")
        self.setGeometry(100, 100, 300, 50)
        self.createProjectDict()
        self.createForm()
        self.createButtonBox()
        self.setMainLayout()     
    
    def createProjectDict(self):
        server = Server()
        table = server.getTable("projects")
        self.projectIds = [project[0] for project in table]
        self.projectNames = [project[1] for project in table]
        self.projectDict = dict(zip(self.projectNames, self.projectIds))
    
    def createForm(self):
        layout = QtWidgets.QFormLayout()
        self.formLayout = QtWidgets.QWidget()
        self.formLayout.setLayout(layout)
    
    def createButtonBox(self):
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setMainLayout(self):
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def moveToCenter(self):
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())