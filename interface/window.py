from PyQt5 import QtWidgets, QtGui

from .tab import Tab
from .tree import ProjectTree
from .table import TagTable
from .menu.menu import MenuBar
from .shortcuts.project import OpenProjectAction, CreateProjectAction
from .shortcuts.list import CreateListAction, SaveListAction, SaveAllListsAction


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, QApplication):
        super(MainWindow, self).__init__()
        self.setResolution(QApplication)
        self.setWindowTitle("TAGApp")
        self.showMaximized()
        self.createCentralWidget()
        self.createToolBar()
        self.createMenuBar()

    def setResolution(self, QApplication):
        screenResolution = QApplication.desktop().screenGeometry()
        self.width = screenResolution.width()
        self.height = screenResolution.height()
        self.setGeometry(0, 0, self.width, self.height)

    def createCentralWidget(self):
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
        self.toolbar = self.addToolBar('Atalhos')
        self.toolbar.addAction(OpenProjectAction(self))
        self.toolbar.addAction(CreateProjectAction(self))
        self.toolbar.addAction(CreateListAction(self, self.tree.updateTree))
        self.toolbar.addAction(SaveListAction(self, self.tabs.saveList))
        self.toolbar.addAction(SaveAllListsAction(self, self.tabs.saveAllLists))
    
    def createMenuBar(self):
        menu = MenuBar(self)    
        self.setMenuBar(menu)
    
    def openList(self, listId):        
        if listId not in self.tabs.openListIds:
            self.tabs.openListIds.append(listId)
            tableWidget = TagTable(listId)
            tableName = tableWidget.getTableName()
            self.tabs.addTab(tableWidget, tableName)
    
    def openProject(self, projectId):
        if projectId not in self.tree.projectIds.values():
            self.tree.addTree(projectId)
            self.tree.addBranches(projectId)
            self.tree.setOpenListFunction(self.openList)

    def closeProject(self, projectId):
        self.tree.removeBranches(projectId)
        self.tree.removeTree(projectId)       
