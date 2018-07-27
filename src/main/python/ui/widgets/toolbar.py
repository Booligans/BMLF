from PyQt5 import QtCore, QtGui, QtWidgets
from ..assets import assets

class ToolBar(QtWidgets.QFrame):
    def __init__(self, *args):
        QtWidgets.QFrame.__init__(self, *args)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color: rgb(239,246,253);")
        self.setMinimumSize(QtCore.QSize(0, 70))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        
        # Tab widget, for multiple toolbars
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setObjectName("toolbar_tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, -1, -1)
        
        # Tab 1, project toolbar
        self.tab = ProjectToolbar()
        self.tabWidget.addTab(self.tab, "")
        
        # Tab 2, ML toolbar
        self.tab_2 = MLToolbar()
        self.tabWidget.addTab(self.tab_2, "")

        # Tab 3, plots toolbar
        self.tab_3 = PlotToolbar()
        self.tabWidget.addTab(self.tab_3, "")

    def retranslateUi(self, _translate):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Project"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "ML"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Plot"))
        self.tab.retranslateUi(_translate)
        self.tab_2.retranslateUi(_translate)
        self.tab_3.retranslateUi(_translate)
        
     
class SingleToolbar(QtWidgets.QWidget):
    def __init__(self, name, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(name)
        self.labels = []
        self.buttons = []

    def addRegion(self, labelText, row, col, rowSpan, colSpan, *buttons):
        # Each region has a label, some buttons and is bordered by lines
        # buttons is an array of tuples (btn, row, col, rowSpan, colSpan)
        # where btn is a widget and the rest are grid parameters
        self.labels.append(QtWidgets.QLabel(self))
        self.labels[-1].setAlignment(QtCore.Qt.AlignCenter)
        self.labels[-1].setObjectName(self.objectName() + labelText)
        self.labels[-1].setText(labelText)
        self.labels[-1].setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.gridLayout.addWidget(self.labels[-1], 0, col, 1, colSpan)

        for button in buttons:
            self.gridLayout.addWidget(*button)
            self.buttons.append(button[0])
            
        line = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(line.sizePolicy().hasHeightForWidth())
        line.setSizePolicy(sizePolicy)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(line, 0, col+colSpan, rowSpan, 1)

    def retranslateUi(self, _translate):
        for widget in self.labels+self.buttons:
            widget.setText(_translate("MainWindow", widget.text()))
        

class ProjectToolbar(SingleToolbar):
    def __init__(self, *args, **kwargs):
        SingleToolbar.__init__(self, "proj_toolbar", *args, **kwargs)
        self.addRegion("File", 0, 0, 2, 2)

class MLToolbar(SingleToolbar):
    def __init__(self, *args, **kwargs):
        SingleToolbar.__init__(self, "ml_toolbar", *args, **kwargs)

        # Data region
        sel_data_button = ToolPushButton(QtGui.QIcon(":/images/select_data.png"), "Select data", self.select_data)
        data_buttons = [(sel_data_button, 1, 0, 1, 1)]
        self.addRegion("Data", 0, 0, 2, 1, *data_buttons)
        
        self.addRegion("Regression", 0, 2, 2, 1)
        self.addRegion("Classification", 0, 4, 2, 1)
        self.addRegion("Reduction", 0, 6, 2, 1)
        self.addRegion("Clustering", 0, 8, 2, 1)

    def select_data(self):
        #self.data = tableWidget.load_data()
        pass
        
        
class PlotToolbar(SingleToolbar):
    def __init__(self, *args, **kwargs):
        SingleToolbar.__init__(self, "plot_toolbar", *args, **kwargs)

        self.data = None

        # Data region (selection, treatment?)
        sel_data_button = ToolPushButton(QtGui.QIcon(":/images/select_data.png"), "Select data", self.select_data)
        data_buttons = [(sel_data_button, 1, 0, 1, 1)]
        self.addRegion("Data", 0, 0, 2, 1, *data_buttons)

        # Visual region (e.g. modify grid/colors?)
        self.addRegion("Visual", 0, 2, 2, 1)
        
        # Basic plots region
        pie_plot_button = ToolPushButton(QtGui.QIcon(":/images/pie_plot.jpg"), "Pie plot", self.pie_plot)
        basic_plots_buttons = [(pie_plot_button, 1, 4, 1, 1)]
        bar_plot_button = ToolPushButton(QtGui.QIcon(":/images/bar_plot.png"), "Bar plot", self.bar_plot)
        basic_plots_buttons.append((bar_plot_button, 1, 5, 1, 1))
        
        self.addRegion("Basic plots", 0, 4, 2, 2, *basic_plots_buttons)
        self.addRegion("Statistical plots", 0, 7, 2, 1)

    def pie_plot(self):
        #PlottingService.build_plot("", 'Pie', 'Pie plot', self.data).plot(axes[0][1])
        pass

    def bar_plot(self):
        pass

    def select_data(self):
        #self.data = tableWidget.load_data()
        pass

    
    
        
class ToolPushButton(QtWidgets.QPushButton):
    # A class to facilitate making of pushbuttons with adequate size for the toolbar,
    # no text, an icon and a tooltip
    def __init__(self, icon, text, function, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, icon, "", *args, **kwargs)
        self.setToolTip(text)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)
        self.clicked.connect(function)

    def sizeHint(self):
        return QtCore.QSize(30,30)
