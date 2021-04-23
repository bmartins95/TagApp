from PyQt5 import QtWidgets, QtGui

from .tab import Tab
from .tree import ProjectTree
from .table import TagTable
from .menu.menu import MenuBar
from .shortcuts.project import OpenProjectAction, CreateProjectAction
from .shortcuts.list import CreateListAction, SaveListAction, SaveAllListsAction


class MainWindow(QtWidgets.QMainWindow):
    """Creates a window with a MenuBar, Shortcuts, Tab and a ProjectTree."""
    def __init__(self, QApplication):
        super(MainWindow, self).__init__()
        self.setResolution(QApplication)
        self.setWindowTitle("TAGApp")
        self.showMaximized()
        self.createCentralWidget()
        self.createToolBar()
        self.createMenuBar()

    def setResolution(self, QApplication):
        """Sets the resolution to the screen max resolution."""
        screenResolution = QApplication.desktop().screenGeometry()
        self.width = screenResolution.width()
        self.height = screenResolution.height()
        self.setGeometry(0, 0, self.width, self.height)

    def createCentralWidget(self):
        """Creates the CentralWidget using the ProjectTree widget and the 
        TabWidget.
        """
        self.tree = ProjectTree()
        self.tabs = Tab()

        centralWidget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.tree)
        layout.addWidget(self.tabs, 2)
        centralWidget.setLayout(layout)
        
        self.setCentralWidget(centralWidget)
    
    def createToolBar(self):
        """Creates a ToolBar and adds some shortcuts."""
        self.toolbar = self.addToolBar('Atalhos')
        self.toolbar.addAction(OpenProjectAction(self))
        self.toolbar.addAction(CreateProjectAction(self))
        self.toolbar.addAction(CreateListAction(self, self.tree.updateTree))
        self.toolbar.addAction(SaveListAction(self, self.tabs.saveList))
        self.toolbar.addAction(SaveAllListsAction(self, self.tabs.saveAllLists))
    
    def createMenuBar(self):
        """Builds the MenuBar defined in interface.menu.MenuBar."""
        menu = MenuBar(self)    
        self.setMenuBar(menu)
    
    def openList(self, listId):
        """If the list is not already open, the function builds the TagTable 
        widget and adds it to the Tab widget.
        """        
        if listId not in self.tabs.openListIds:
            self.tabs.openListIds.append(listId)
            tableWidget = TagTable(listId)
            tableName = tableWidget.getTableName()
            self.tabs.addTab(tableWidget, tableName)
    
    def openProject(self, projectId):
        """If the project is not already ipen the function adds it to the 
        ProjectTree widget.
        """
        if projectId not in self.tree.projectIds.values():
            self.tree.addTree(projectId)
            self.tree.addBranches(projectId)
            self.tree.setOpenListFunction(self.openList)

    def closeProject(self, projectId):
        """Removes the project from the ProjectTree."""
        self.tree.removeBranches(projectId)
        self.tree.removeTree(projectId)       
