from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox

from server.server import Server

class Dialog(QDialog):
    """A template dialog class that defines default functions such as, 
    createProjectDict, createForm, createButtonBox, setMainLayout and 
    moveToCenter.
    """
    def __init__(self):
        super(Dialog, self).__init__()
        self.setWindowTitle("Default Title")
        self.setGeometry(100, 100, 300, 50)
        self.createProjectDict()
        self.createForm()
        self.createButtonBox()
        self.setMainLayout()     
    
    def createProjectDict(self):
        """Creates the dictionary projectDict that uses the names of the 
        projects as keys and their ids as values. Only the projects currently 
        available on the database are added to projectDict.
        """
        server = Server()
        table = server.getTable("projects")
        self.projectIds = [project[0] for project in table]
        self.projectNames = [project[1] for project in table]
        self.projectDict = dict(zip(self.projectNames, self.projectIds))
    
    def createForm(self):
        """Creates a form widget named formLayout."""
        layout = QtWidgets.QFormLayout()
        self.formLayout = QtWidgets.QWidget()
        self.formLayout.setLayout(layout)
    
    def createButtonBox(self):
        """Creates a widget named buttonBox that contains an OK and a Cancel 
        button."""
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setMainLayout(self):
        """Joins formLayout and buttonBox in a single widget and sets it as the
        dialog layout."""
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def moveToCenter(self):
        """Moves the dialog window to the center of the screen."""
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())