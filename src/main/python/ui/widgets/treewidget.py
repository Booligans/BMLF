from PyQt5 import QtCore, QtGui, QtWidgets
from ..assets import assets
import os
import numpy as np

class ProjectTree(QtWidgets.QTreeWidget):

    opened_data = QtCore.pyqtSignal(np.ndarray, list)
    
    def __init__(self, *args):
        QtWidgets.QTreeWidget.__init__(self, args[0])
        args[2].addWidget(self, 0, 0, 6, 2)
        
        self.setObjectName("ProjectTreeWidget")
        self.setHeaderLabel("Projects")
        self.setStyleSheet( "QTreeWidget{background: rgb(216,233,250);}")
        self.startpath = args[1]
        self.search_projects()
        self.itemDoubleClicked.connect(self.open_item)

    def reset(self):
        iterator = QtWidgets.QTreeWidgetItemIterator(self, QtWidgets.QTreeWidgetItemIterator.All)
        while iterator.value():
            iterator.value().takeChildren()
            iterator +=1
        i = self.topLevelItemCount()
        while i > -1:
            self.takeTopLevelItem(i)
            i -= 1

    def open_item(self, item, col):
        """
        Open an item in the tree
        :param item:
        :type item: QTreeWidgetItem
        """
        path = self.get_abs_path(item)
        if self.is_project(path):
            if not item.isOpen():
                self.load_project(path, item)
                item.setOpen(True)
        elif os.path.isdir(path):
            if not item.isOpen():
                self.open_folder(path, item)
                item.setOpen(True)
        else:
            self.open_file(path)

    def open_file(self, path):
        """
        Open a file with data, tagged or not
        :param path: Path to the file
        :type path: str:
        """
        try:
            tagged = False
            tags = []
            with open(path, 'r') as f:
                tags = f.readline().split(' ')
                for tag in tags:
                    try:
                        complex(tag)
                    except ValueError:
                        #The string is not a number, so it must be a tag
                        tagged = True
                        break;

            #Remove end of line
            tags[-1] = tags[-1][:-1]
            
            skiprows = 0
            if tagged:
                skiprows = 1
            else:
                tags = []
                
            data = np.loadtxt(path, skiprows=skiprows)
            self.opened_data.emit(data, tags)
            
        except Exception as err:
            raise ValueError("Could not read data from " + path + ".\n", err)
            
    def open_folder(self, folder, tree):
        """
        Opens a folder in the tree
        :param folder: Folder to open
        :type folder: str
        """
        for element in os.listdir(folder):
            path_info = folder + "/" + element
            parent_itm = CustomTreeWidgetItem(tree, [element])
            if os.path.isdir(path_info):
                parent_itm.setIcon(0, QtGui.QIcon(':/images/folder.png'))
                self.open_folder(path_info, parent_itm)
                parent_itm.setExpanded(False)
                parent_itm.setOpen(True)
            else:
                parent_itm.setIcon(0, QtGui.QIcon(':/images/file.png'))
                
            
    def search_projects(self):
        """
        Search for projects in the workspace
        and load them into the tree structure
        :param tree: 
        :return: 
        """
        for element in os.listdir(self.startpath):
            path_info = self.startpath + "/" + element
            if self.is_project(path_info):
                parent_itm = CustomTreeWidgetItem(self, [element])
                parent_itm.setIcon(0, QtGui.QIcon(':/images/proj.png'))
                
                
    def load_project(self, proj_path, tree):
        """
        Load a single project into the tree
        :param tree: 
        :return: 
        """
        # THIS MUST BE REIMPLEMENTED WHEN PROJECT DATA IS AVAILABLE
        self.open_folder(proj_path, tree)

        
    def is_project(self, path_info):
        # THIS MUST BE REIMPLEMENTED WHEN PROJECT DATA IS AVAILABLE
        # For the moment, just look for a .prj file
        return os.path.isdir(path_info) and len(list(filter(lambda x : '.prj' in x, os.listdir(path_info)))) == 1

    def get_abs_path(self, item):
        if item is None:
            return self.startpath
        else:
            return self.get_abs_path(item.parent()) + '/' + item.text(0)

        
class CustomTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._isOpen = False
    
    def setOpen(self, isOpen):
        self._isOpen = isOpen

    def isOpen(self):
        return self._isOpen
