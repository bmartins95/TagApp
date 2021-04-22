from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QAction, QDialogButtonBox

class HelpDialog(QDialog):
    def __init__(self, version, creator):
        super(HelpDialog, self).__init__()
        self.version = version
        self.creator = creator
        
        self.setWindowTitle("Informações")
        self.createLabels()
        self.createButtonBox()
        self.setMainLayout() 
        self.moveToCenter()   
    
    def createLabels(self):
        self.labelWidget = QtWidgets.QWidget()
        
        layout = QtWidgets.QVBoxLayout()
        appName = QtWidgets.QLabel("TAGApp")
        version = QtWidgets.QLabel(self.version)
        creator = QtWidgets.QLabel(self.creator)

        appName.setAlignment(Qt.AlignHCenter)
        version.setAlignment(Qt.AlignHCenter)
        creator.setAlignment(Qt.AlignHCenter)
        
        layout.addWidget(appName)
        layout.addWidget(version)
        layout.addWidget(creator)
        
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        appName.setFont(boldFont)
        
        self.labelWidget.setLayout(layout)
    
    def createButtonBox(self):
        buttons = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.setCenterButtons(True)

    def setMainLayout(self):
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.labelWidget)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def moveToCenter(self):
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())


class OpenHelpDialogAction(QAction):
    def __init__(self, parent, version, creator, name="Sobre o app"):
        super(OpenHelpDialogAction, self).__init__( 
            QtGui.QIcon(""), 
            name,
            parent)
        self.version = version
        self.creator = creator
        self.triggered.connect(self.openHelpDialog)

    def openHelpDialog(self):
        dialog = HelpDialog(self.version, self.creator)
        dialog.exec_()

