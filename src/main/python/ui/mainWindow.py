from PyQt5 import QtCore, QtGui, QtWidgets
from .dialog import *
from .assets import assets
from .widgets.treewidget import ProjectTree
import os

from plots.plotting_service import PlottingService

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 531)
        p = MainWindow.palette()
        p.setColor(MainWindow.backgroundRole(), QtGui.QColor(253,238,241))
        MainWindow.setPalette(p)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set main layout for automatic resizing
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        # Tab widget, contains the data, visualization... tabs
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)

        self.gridLayout.addWidget(self.tabWidget, 0, 2, 10, -1)

        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setObjectName("tabWidget")

        # Tab 1, will contain the data table
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = TableWidget(self.tab)
        self.tabWidget.addTab(self.tab, "")
        """
        # ----Sample data----

        data = np.array([[1,2,3],[4,5,6],[7,8,9]])
        tags = ['Foo', 'Bar', 'Target']
        self.tableWidget.load_data(data, tags)
        
        #--------------------
        """
        # Tab 2, will contain the visualizations
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        # Grid layout for the second tab, necessary for FigureCanvas automatic resizing
        self.gridLayout_tab_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_tab_2.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_tab_2.setSpacing(0)
        self.gridLayout_tab_2.setObjectName("gridLayout_tab_2")

        #FigureCanvas for displaying plots
        self.canvas = FigureCanvas(Figure())
        self.gridLayout_tab_2.addWidget(self.canvas, 0, 0, 1, 1)


        # ----Sample basic plots-----

        #data
        sp = np.linspace(0, 10, 501)
        pie = np.array([1,2,3,1])

        #We want a 2x2 grid of plots, with 0.5 vertical separation
        axes = self.canvas.figure.subplots(2,2, gridspec_kw={'hspace':0.5})

        #Call plotting module
        PlottingService.build_plot('Awesomest project', 'Bar', 'Bar plot', pie, 'X axis', 'Y axis').plot(axes[0][0])
        PlottingService.build_plot('Awesomest project', 'Pie', 'Pie plot', pie).plot(axes[0][1])
        PlottingService.build_plot('Awesomest project', 'Line', 'Line plot', [sp, np.cos(sp)]).plot(axes[1][0])

        #----------------------------

        self.tabWidget.addTab(self.tab_2, "")

        # Menu bar
        self.menubar = MenuBar(MainWindow, self)
        MainWindow.setMenuBar(self.menubar)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("QStatusBar{background: rgb(239,246,253); border-top:1px solid white;}")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Tool bar
        self.toolbar = ToolBar(MainWindow)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

        # Get workspace and setup project tree
        self.file = QtWidgets.QFileDialog.getExistingDirectory(MainWindow, "Select your workspace")
        if (self.file != ""):
            self.ProjectTreeWidget = ProjectTree(self.centralwidget, self.file, self.gridLayout)
            self.ProjectTreeWidget.opened_data.connect(self.tableWidget.load_data)
            
        MainWindow.setCentralWidget(self.centralwidget)
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

    DEFAULT_ROWS = 10000
    DEFAULT_COLS = 1000
    
    def __init__(self, *args):
        stylesheet_1 = "::section{Background-color:rgb(216,233,250);}"
        stylesheet_2 = (
        "QHeaderView::section{""border-right:1px solid #D8D8D8;""border-bottom: 1px solid #D8D8D8;}"
        "QTableCornerButton::section{border-right:1px solid #D8D8D8;border-bottom: 1px solid #D8D8D8;background-color:#d8e9fa;}")
        QtWidgets.QTableWidget.__init__(self, *args)

        self.gridLayout = QtWidgets.QGridLayout(args[0])
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout_tab_1")

        self.gridLayout.addWidget(self, 0, 0, 1, 1)
        
        self.setGeometry(QtCore.QRect(0, 0, -1, -1))
        self.setAutoFillBackground(False)
        self.setShowGrid(True)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setWordWrap(True)
        self.setRowCount(self.DEFAULT_ROWS)
        self.setColumnCount(self.DEFAULT_COLS)
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
        self.setItemPrototype(self.CustomTableWidgetItem())


    def load_data(self, data, columns = None):
        """
        Load data into the table
        :param data: The data to load
        :param columns: Names of columns
        :type data: ndarray, shape=(n_samples, n_features)
        :type columns: array-like, shape=(n_features)
        """
        for i, row in enumerate(data):
            for j, elem in enumerate(row):
                self.setItem(i, j, self.CustomTableWidgetItem(str(elem)))

        if columns is not None:
            self.setHorizontalHeaderLabels(columns)
        
        
        
    class CustomTableWidgetItem(QtWidgets.QTableWidgetItem):
        # Custom table item with specified alignment
        def __init__(self, *args, align=QtCore.Qt.AlignCenter,
                     type=QtWidgets.QTableWidgetItem.UserType, **kwargs):
            super().__init__(*args, type=type, **kwargs)
            self.setTextAlignment(align)
            

class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, *args):
        QtWidgets.QMenuBar.__init__(self, args[0])
        self.setGeometry(QtCore.QRect(0, 0, 959, 21))
        self.setStyleSheet( "QMenuBar{background: rgb(239,246,253);}")
        self.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self)
        self.menuNew.setObjectName("menuNew")
        actionNewProject = Action(self, "actionNewProject", lambda: self.newProject(), "Project")
        self.menuNew.addAction(actionNewProject)
        self.menuFile.addAction(self.menuNew.menuAction())
        actionOpen = Action(self, "actionOpen", lambda: self.opened(), "Open")
        self.menuFile.addAction(actionOpen)
        actionSwWorkspace = Action(self, "actionSwWorkspace", lambda: self.sw_workspace(args[1]), "Switch Workspace")
        self.menuFile.addAction(actionSwWorkspace)
        self.menuModules = QtWidgets.QMenu(self)
        self.menuModules.setObjectName("Modules")
        self.actionNewModule = Action(self, "actionNewModule", lambda: self.dialog(args[1]), "Add")
        self.menuModules.addAction(self.actionNewModule)
        self.menuFile.addAction(self.menuModules.menuAction())

        self.menuEdit = QtWidgets.QMenu(self)
        self.menuEdit.setObjectName("menuEdit")
        actionUndo = Action(self, "actionUndo", lambda: self.undo(), "Undo")
        self.menuEdit.addAction(actionUndo)
        actionRedo = Action(self, "actionRedo", lambda: self.redo(), "Redo")
        self.menuEdit.addAction(actionRedo)
        self.menuEdit.addSeparator()

        self.addAction(self.menuFile.menuAction())
        self.addAction(self.menuEdit.menuAction())
		
        _translate = QtCore.QCoreApplication.translate
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuNew.setTitle(_translate("MainWindow", "New"))
        self.menuModules.setTitle(_translate("MainWindow", "Modules"))

    def newProject(self):
        print("new Project")

    def opened(self):
        QtWidgets.QFileDialog.getOpenFileName()
	
    def sw_workspace(self, Ui_MainWindow):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select your workspace"))
        if (file != ""):
            Ui_MainWindow.ProjectTreeWidget.reset()
            Ui_MainWindow.ProjectTreeWidget.load_project(file, Ui_MainWindow.ProjectTreeWidget)
	
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

