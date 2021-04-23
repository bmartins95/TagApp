import sip

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTreeWidget

from server.server import Server


class ProjectTree(QTreeWidget):
    """A QTreeWidget that has any open project and all its lists as 
    QTreeWidgetItem.
    """
    def __init__(self):
        super(ProjectTree, self).__init__()
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        self.projectIds = {}
        self.listsOpen = {}
        self.trees = {}

        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def addTree(self, id: int):
        """Takes the projectId searchs for the project name on the server, then
        the function creates a QtWidgets.QTreeWidgetItem using the project name
        and defines this item as an class top level item.
        """
        server = Server()
        name = server.getProjectName(id)
        self.projectIds[name] = id
        self.trees[name] = QtWidgets.QTreeWidgetItem([name])
        self.addTopLevelItem(self.trees[name])

    def addBranches(self, id: int):
        """Searches for all the lists in the server that have id as their 
        projectId. Creates a QTreeWidgetItem for each list and add the item into
        the top level QTreeWidgetItem.
        """
        server = Server()
        name = server.getProjectName(id)
        branches = server.getListsNameFromProject(id)
        self.listsOpen[name] = branches
        for branch in branches:
            item = QtWidgets.QTreeWidgetItem(branch)
            self.trees[name].addChild(item)
        self.trees[name].setExpanded(True)

    def removeTree(self, id: int):
        """Searches for a key in the projectIds dictionary that has the project
        id as a value, when the key is found, this function uses the key to 
        delete entries in projectIds, trees and also to delete the C object 
        stored in trees[key].
        """
        for key in self.projectIds:
            if self.projectIds[key] == id:
                del self.projectIds[key]
                sip.delete(self.trees[key])
                del self.trees[key]
                break

    def removeBranches(self, id: int):
        """Searches for a key in the projectIds dictionary that has the project
        id as a value and uses the key to delete the entry in listsOpen list. 
        """
        for key in self.projectIds:
            if self.projectIds[key] == id:
                del self.listsOpen[key]
                break

    def onItemDoubleClicked(self, it: QtWidgets.QTreeWidgetItem, col: int):
        """When a item in ProjectTree is double clicked this function is 
        activated. The function checks if QTreeWidgetItem has a parent, if the 
        item has a parent the function will search the list id in the database
        and it will create a TagTable in the Tab widget.
        """
        if it.parent() is not None:
            server = Server()
            listName = it.text(col)
            projectId = self.projectIds[str(it.parent().text(col))]
            listId = server.getListIdFromProject(listName, projectId)
            self.openList(listId)
 
    def setOpenListFunction(self, func):
        """Receives the openList function from interface.window.MainWindow and
        set the function as a class variable.
        """
        self.openList = func

    def getOpenProjectNames(self) -> list:
        """Return a list that has the names of the projects currently open in
        the ProjectTree widget.
        """
        return self.projectIds.keys()

    def updateTree(self, projectName: str):
        """Checks if the project with projectName is in the ProjectTree and
        also if the project is not updated, if both question return true, the
        fuction searches on the database for the missing list names and add it 
        to the ProjectTree.
        """
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
            
    def isTreeUpdated(self, projectName: str) -> bool:
        """If any project is currently open in the ProjectTree, the function
        checks if those projects are update. If the project is updated the 
        function returns true.
        """
        if len(self.listsOpen) > 0:
            server = Server()
            dbList = server.getListsNameFromProject(self.projectIds[projectName])
            
            if len(self.listsOpen[projectName]) != len(dbList):
                return False
            else:
                return sorted(self.listsOpen[projectName]) == sorted(dbList)
        else:
            return True



