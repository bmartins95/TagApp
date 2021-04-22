from PyQt5.QtWidgets import QTabWidget

class Tab(QTabWidget):
    def __init__(self):
        super(Tab, self).__init__()
        self.setTabsClosable(True)
        self.defineStyle()
        self.tabBar().setMovable(True)
        self.openListIds = []

        self.tabCloseRequested.connect(self.closeTab)

    def defineStyle(self):
        style = """
            QTabBar::tab { 
                text-align: center;
                height: 25px; 
                width: 120px; 
            }
        """
        self.setStyleSheet(style)

    def closeTab(self, index):
        self.openListIds.pop(index)
        self.removeTab(index)

    def saveList(self):
        self.currentWidget().save()

    def saveAllLists(self):
        for index in range(0, self.count()):
            self.widget(index).save()