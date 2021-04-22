from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidget
import sip

from server.server import Server

class ProjectTree(QTreeWidget):
    def __init__(self):
        super(ProjectTree, self).__init__()
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        self.projectIds = {}
        self.listsOpen = {}
        self.trees = {}

        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def addTree(self, id):
        server = Server()
        name = server.getProjectName(id)
        self.projectIds[name] = id
        self.trees[name] = QtWidgets.QTreeWidgetItem([name])
        self.addTopLevelItem(self.trees[name])

    def addBranches(self, id):
        server = Server()
        name = server.getProjectName(id)
        branches = server.getListsNameFromProject(id)
        self.listsOpen[name] = branches
        for branch in branches:
            item = QtWidgets.QTreeWidgetItem(branch)
            self.trees[name].addChild(item)
        self.trees[name].setExpanded(True)

    def removeTree(self, id):
        for key in self.projectIds:
            if self.projectIds[key] == id:
                del self.projectIds[key]
                sip.delete(self.trees[key])
                del self.trees[key]
                break

    def removeBranches(self, id):
        for key in self.projectIds:
            if self.projectIds[key] == id:
                del self.listsOpen[key]
                break

    def onItemDoubleClicked(self, it, col):
        if it.parent() is not None:
            server = Server()
            listName = it.text(col)
            projectId = self.projectIds[str(it.parent().text(col))]
            listId = server.getListIdFromProject(listName, projectId)
            self.openList(listId)
 
    def setOpenListFunction(self, func):
        self.openList = func

    def getOpenProjectNames(self):
        return self.projectIds.keys()

    def updateTree(self, projectName):
        isProjectOpen = projectName in self.projectIds.keys()
        isTreeUpdated = self.isTreeUpdated(projectName)
        if isProjectOpen and not isTreeUpdated:
            server = Server()
            dbList = server.getListsNameFromProject(self.projectIds[projectName])
            openSet = set(self.listsOpen[projectName])
            toUpdate = [item for item in dbList if item not in openSet]
            for value in toUpdate:
                item = QtWidgets.QTreeWidgetItem(value)
                self.trees[projectName].addChild(item)
            
    def isTreeUpdated(self, projectName):
        server = Server()
        dbList = server.getListsNameFromProject(self.projectIds[projectName])
        
        if len(self.listsOpen[projectName]) != len(dbList):
            return False
        else:
            return sorted(self.listsOpen[projectName]) == sorted(dbList)



