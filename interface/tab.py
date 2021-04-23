from PyQt5.QtWidgets import QTabWidget


class Tab(QTabWidget):
    """Creates the widget that allows lists to be shown."""
    def __init__(self):
        super(Tab, self).__init__()
        self.setTabsClosable(True)
        self.defineStyle()
        self.tabBar().setMovable(True)
        
        self.openListIds = []
        self.tabCloseRequested.connect(self.closeTab)

    def defineStyle(self):
        """Defines tab sizes."""
        style = """
            QTabBar::tab { 
                height: 25px; 
                width: 120px; 
            }
        """
        self.setStyleSheet(style)

    def closeTab(self, index):
        """Removes listId from openListIds and removes the list widged from the
        Tab widget.
        """
        self.openListIds.pop(index)
        self.removeTab(index)

    def saveList(self):
        """Checks if a tab is opened in the Tab widget. If a tab is opened, the 
        functions saves any changed data on the TagTable widget currently 
        selected.
        """
        if self.currentWidget() is not None:
            self.currentWidget().save()

    def saveAllLists(self):
        """Saves changes for all the TagTable widgets currently opened in the
        Tab widget.
        """
        for index in range(0, self.count()):
            self.widget(index).save()

