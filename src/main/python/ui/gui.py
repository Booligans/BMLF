from PyQt5 import QtCore, QtGui, QtWidgets
from dialog import *
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 531)
        p = MainWindow.palette()
        p.setColor(MainWindow.backgroundRole(), QtGui.QColor(253,238,241))
        MainWindow.setPalette(p)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(270, 10, 1091, 641))
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = TableWidget(self.tab)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 801, 551))
        self.graphicsView.setObjectName("graphicsView")
        self.tabWidget.addTab(self.tab_2, "")
        file = str(QtWidgets.QFileDialog.getExistingDirectory(MainWindow, "Select your workspace"))
        self.projectTreeWidget = projectTree(self.centralwidget, file)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = MenuBar(MainWindow, self)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet( "QStatusBar{background: rgb(239,246,253); border-top:1px solid white;}")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar = ToolBar(MainWindow)
        MainWindow.addToolBar( QtCore.Qt.TopToolBarArea , self.toolbar )

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BMLF"))
        self.tableWidget.setSortingEnabled(False)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Visualization"))
			
class ToolButton(QtWidgets.QToolButton):
    def __init__(self, *args):
        QtWidgets.QToolButton.__init__(self, *args)
        self.setCheckable(True)
        self.setStyleSheet( "QToolButton{border:1px solid white;}")
			
class ToolBar(QtWidgets.QToolBar):
    def __init__(self, *args):
        QtWidgets.QToolBar.__init__(self, *args)
        self.setStyleSheet( "QToolBar{background: rgb(239,246,253);}")
        self.setObjectName("toolbar")
        toolButton1 = ToolButton(self)
        self.addWidget(toolButton1)
        toolButton2 = ToolButton(self)
        self.addWidget(toolButton2)
		
class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args):
        stylesheet_1 = "::section{Background-color:rgb(216,233,250);}"
        stylesheet_2 = (
        "QHeaderView::section{""border-right:1px solid #D8D8D8;""border-bottom: 1px solid #D8D8D8;}"
        "QTableCornerButton::section{border-right:1px solid #D8D8D8;border-bottom: 1px solid #D8D8D8;background-color:#d8e9fa;}")
        QtWidgets.QTableWidget.__init__(self, *args)
        self.setGeometry(QtCore.QRect(0, 0, 1081, 611))
        self.setAutoFillBackground(False)
        self.setShowGrid(True)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setWordWrap(True)
        self.setRowCount(10000)
        self.setColumnCount(1000)
        self.setObjectName("tableWidget")
        self.setStyleSheet(stylesheet_1)
        self.horizontalHeader().setStyleSheet(stylesheet_2)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setCascadingSectionResizes(False)
        self.verticalHeader().setStyleSheet(stylesheet_2)
        self.verticalHeader().setVisible(True)
        self.verticalHeader().setCascadingSectionResizes(False)
        self.verticalHeader().setHighlightSections(True)
        self.verticalHeader().setSortIndicatorShown(False)
        self.verticalHeader().setStretchLastSection(False)

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, *args):
        QtWidgets.QMenuBar.__init__(self, args[0])
        self.setGeometry(QtCore.QRect(0, 0, 959, 21))
        self.setStyleSheet( "QMenuBar{background: rgb(239,246,253);}")
        self.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self)
        self.menuEdit.setObjectName("menuEdit")
        actionOpen = Action(self, "actionOpen", lambda: self.opened(), "Open")
        self.menuNew = QtWidgets.QMenu(self)
        self.menuNew.setObjectName("menuNew")
        actionMLModule = Action(self, "actionMLModule", lambda: self.newML(args[1], "ML"), "ML Module")
        actionAModule = Action(self, "actionAModule", lambda: self.newML(args[1], "Analysis"), "Analysis")
        actionMLModule = Action(self, "actionMLModule", lambda: self.newML(args[1], "ML"), "ML Module")
        actionSwWorkspace = Action(self, "actionSwWorkspace", lambda: self.sw_workspace(args[1]), "Switch Workspace")
        self.menuPreferences = QtWidgets.QMenu(self)
        self.menuPreferences.setObjectName("menuPreferences")
        self.setPreferencesAction = Action(self, "setPreferencesAction", lambda: self.dialog(args[1]), "Preferences")
        self.menuPreferences.addAction(self.setPreferencesAction)
        self.addAction(self.menuPreferences.menuAction())
        actionUndo = Action(self, "actionUndo", lambda: self.undo(), "Undo")
        actionRedo = Action(self, "actionRedo", lambda: self.redo(), "Redo")
        self.menuNew.addAction(actionMLModule)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(actionOpen)
        self.menuFile.addAction(actionSwWorkspace)
        self.menuEdit.addAction(actionUndo)
        self.menuEdit.addAction(actionRedo)
        self.menuEdit.addSeparator()
        self.addAction(self.menuFile.menuAction())
        self.addAction(self.menuEdit.menuAction())
		
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuNew.setTitle(_translate("MainWindow", "New"))
        self.menuPreferences.setTitle(_translate("MainWindow", "Preferences"))

    def opened(self):
        QtWidgets.QFileDialog.getOpenFileName()
	
    def sw_workspace(self, Ui_MainWindow):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select your workspace"))
        Ui_MainWindow.projectTreeWidget.reset()
        Ui_MainWindow.projectTreeWidget.load_project(file, Ui_MainWindow.projectTreeWidget)
	
    def undo(self):
        print("undo")

    def redo(self):
        print("redo")

    def newModule(self, Ui_MainWindow, MName):
        self.tab_new = QtWidgets.QWidget()
        self.tab_new.setObjectName(MName)
        Ui_MainWindow.tabWidget.addTab(self.tab_new, MName)
	
    def dialog(self, Ui_MainWindow):
        dialog = PreferencesDialog(Ui_MainWindow)

class projectTree(QtWidgets.QTreeWidget):
    def __init__(self, *args):
        QtWidgets.QTreeWidget.__init__(self, args[0])
        self.setGeometry(QtCore.QRect(10, 10, 251, 531))
        self.setObjectName("projectTreeWidget")
        self.setHeaderLabel("Projects")
        self.setStyleSheet( "QTreeWidget{background: rgb(216,233,250);}")
        self.load_project(args[1], self)

    def reset(self):
        iterator = QtWidgets.QTreeWidgetItemIterator(self, QtWidgets.QTreeWidgetItemIterator.All)
        while iterator.value():
            iterator.value().takeChildren()
            iterator +=1
        i = self.topLevelItemCount()
        while i > -1:
            self.takeTopLevelItem(i)
            i -= 1

    def load_project(self, startpath, tree):
        """
        Load Project structure tree
        :param startpath: 
        :param tree: 
        :return: 
        """
        for element in os.listdir(startpath):
            path_info = startpath + "/" + element
            parent_itm = QtWidgets.QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                self.load_project(path_info, parent_itm)
                parent_itm.setIcon(0, QtGui.QIcon('assets/folder.png'))
            else:
                parent_itm.setIcon(0, QtGui.QIcon('assets/file.png'))

class Action(QtWidgets.QAction):
    def __init__(self, *args):
        QtWidgets.QAction.__init__(self, args[0])
        self.setObjectName(args[1])
        self.triggered.connect(args[2])
        self.setText(QtCore.QCoreApplication.translate("MainWindow", args[3]))

class PreferencesDialog(QtWidgets.QDialog):
    def __init__(self, *args):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui.checkBox.stateChanged.connect(lambda: self.state_changed(self.ui.checkBox, args[0], "ML Module"))
        self.ui.checkBox_2.stateChanged.connect(lambda: self.state_changed(self.ui.checkBox_2, args[0], "Plotting"))
        self.ui.checkBox_3.stateChanged.connect(lambda: self.state_changed(self.ui.checkBox_3, args[0], "Stat Analysis"))
        self.ui.checkBox_4.stateChanged.connect(lambda: self.state_changed(self.ui.checkBox_4, args[0], "Data Analysis"))
        self.exec_()

    def state_changed(self, CheckBox, Ui_MainWindow, MName):
        tab = Ui_MainWindow.tabWidget
        if CheckBox.isChecked():
            tab.removeTab(tab.indexOf(tab.findChild(QtWidgets.QWidget, MName)))
            Ui_MainWindow.menubar.newModule(Ui_MainWindow, MName)
        else:
            tab.removeTab(tab.indexOf(tab.findChild(QtWidgets.QWidget, MName)))

