import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidget

from server.server import Server

class ProjectTree(QTreeWidget):
    def __init__(self):
        super(ProjectTree, self).__init__()
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        self.projectIds = {}
        self.trees = []

        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def addTree(self, id):
        server = Server("./server/database/teste.db")
        name = server.getProjectName(id)
        self.projectIds[name] = id
        self.trees.append(QtWidgets.QTreeWidgetItem([name]))
        self.addTopLevelItem(self.trees[-1])
    
    def addBranches(self, id):
        server = Server("./server/database/teste.db")
        branches = server.getListsFromProject(id)
        for branch in branches:
            item = QtWidgets.QTreeWidgetItem(branch)
            self.trees[-1].addChild(item)
        self.trees[-1].setExpanded(True)

    def onItemDoubleClicked(self, it, col):
        server = Server("./server/database/teste.db")
        listName = it.text(col)
        projectId = self.projectIds[str(it.parent().text(col))]
        listId = server.getListIdFromProject(listName, projectId)
        self.openList(listId)
 
    def setOpenListFunction(self, func):
        self.openList = func
