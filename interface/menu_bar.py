from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence

from .shortcuts.project import OpenProjectAction
from .shortcuts.project import CreateProjectAction
from .shortcuts.project import CloseProjectAction
from .shortcuts.list import SaveAllListsAction
from .shortcuts.menu import OpenHelpDialogAction

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        super(MenuBar, self).__init__()
        arquivo = self.addMenu("Arquivo")
        ajuda = self.addMenu("Ajuda")
        
        addProject = CreateProjectAction(parent, "Novo projeto")
        openProject = OpenProjectAction(parent)
        saveProject = SaveAllListsAction(parent, parent.tabs.saveAllLists, "Salvar projeto")
        closeProject = CloseProjectAction(parent, parent.tree.getOpenProjectNames)
        
        addProject.setShortcut(QKeySequence('Ctrl+P'))
        openProject.setShortcut(QKeySequence('Ctrl+O'))
        saveProject.setShortcut(QKeySequence('Ctrl+Shift+S'))
        
        addProject.setIconVisibleInMenu(False)
        openProject.setIconVisibleInMenu(False)
        saveProject.setIconVisibleInMenu(False)
        closeProject.setIconVisibleInMenu(False)

        arquivo.addAction(addProject)
        arquivo.addAction(openProject)
        arquivo.addAction(saveProject)
        arquivo.addAction(closeProject)

        version = "versão: 1.0.0"
        creator = "Desenvolvido por: Bruno Martins"
        
        ajuda.addAction(OpenHelpDialogAction(parent, version, creator))