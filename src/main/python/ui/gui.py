from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setStyleSheet( "QListWidget{background: rgb(216,233,250);}")
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 251, 631))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 959, 21))
        self.menubar.setStyleSheet( "QMenuBar{background: rgb(239,246,253);}")
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet( "QStatusBar{background: rgb(239,246,253); border-top:1px solid white;}")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.toolbar = ToolBar(MainWindow)
        MainWindow.addToolBar( QtCore.Qt.TopToolBarArea , self.toolbar )

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
    def resizeEvent(self, event):
        MainWindow.resize(self.width(), self.height())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BMLF"))
        self.tableWidget.setSortingEnabled(False)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Visualization"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Analysis"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
			
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

