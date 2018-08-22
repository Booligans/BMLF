from PyQt5 import QtCore, QtGui, QtWidgets
from ..assets import assets
from ..dialog import InputDialog
from .abstractions import Clipboard, Data
from .tablewidget import TableWidget
from ml.regression.regression import LinearModel
from ml.classifier.classifier import MultiModelClassifier
from ml.clustering.clustering import ClusteringModel
from ml.reduction.pca_reductor import PCAReductor
import ast

SELECTION = 'selection'
TRANSFORMED = 'transformed'

class ToolBar(QtWidgets.QFrame):
    def __init__(self, data_medium, plotting_space, *args):
        """
        :param data_medium: Medium for data storage and retrieval
        :type data_medium: ui.widgets.abstractions.DataMedium
        """
        
        QtWidgets.QFrame.__init__(self, *args)
        Clipboard.__init__(self, data_medium)

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

        # The toolbar has a Clipboard because subbars need to access the selected data,
        # or save new generated data, and this must be done through the toolbar, which has
        # access to the table or other data medium
        self.clipboard = Clipboard(data_medium)
        
        # Tab 1, project toolbar
        self.tab = ProjectToolbar(self.clipboard)
        self.tabWidget.addTab(self.tab, "")
        
        # Tab 2, ML toolbar
        self.tab_2 = MLToolbar(self.clipboard)
        self.tabWidget.addTab(self.tab_2, "")

        # Tab 3, plots toolbar
        self.tab_3 = PlotToolbar(plotting_space, self.clipboard)
        self.tabWidget.addTab(self.tab_3, "")

    def retranslateUi(self, _translate):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Project"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "ML"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Plot"))
        self.tab.retranslateUi(_translate)
        self.tab_2.retranslateUi(_translate)
        self.tab_3.retranslateUi(_translate)

     
class SingleToolbar(QtWidgets.QWidget):
    def __init__(self, name, clipboard, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(name)
        self.labels = []
        self.buttons = []

        # Toolbars need to deal with data, which they get from and store in
        # a clipboard passed from the parent
        self.clipboard = clipboard
        
        
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
            self.gridLayout.addWidget(button[0], button[1]+row, button[2]+col, button[3], button[4])
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

        sel_data_button = ToolPushButton(
            QtGui.QIcon(":/images/select_data.png"), "Select data", self.select_data)
        show_sel_data_button = ToolPushButton(
            QtGui.QIcon(":/images/show_data.png"), "Show selected data", self.show_selected_data)
        paste_data_button = ToolPushButton(
            QtGui.QIcon(":/images/paste_data.png"), "Paste selected data into the table", self.paste_data)
        data_buttons = [(sel_data_button, 1, 0, 1, 1), (show_sel_data_button, 1, 1, 1, 1), (paste_data_button, 1, 2, 1, 1)]
        self.addRegion("Data", 0, 3, 2, 3, *data_buttons)
        
    def select_data(self):
        self.clipboard.load_from_medium(key=SELECTION)

    def show_selected_data(self):
        if len(self.clipboard.get_keys()) > 0:
            dialog = QtWidgets.QDialog()
            gridLayout = QtWidgets.QGridLayout(dialog)
            tabWidget = QtWidgets.QTabWidget()
            gridLayout.addWidget(tabWidget)
            for key in self.clipboard.get_keys():
                tab = QtWidgets.QWidget()
                table = TableWidget(tab)
                table.load_data(self.clipboard.get_data(key=key))
                tabWidget.addTab(tab, key)
                
            dialog.setWindowTitle("Selected data")
            dialog.setWindowModality(QtCore.Qt.ApplicationModal)
            dialog.exec_()
        else:
            raise ValueError("No data selected")

    def paste_data(self):
        dialog = InputDialog("Save data")
        dialog.addWidget("label", "label1", 0, 0, 1, 1,
                         text="Save the new data\nstarting in column:")
        dialog.addWidget("spin_box", "spbox", 0, 1, 1, 1, _range=(1,100))
        dialog.addWidget("label", "label2", 1, 0, 1, 1, text="Select which data to save")
        dialog.addWidget("combo_box", "cbbox", 1, 1, 1, 1, items=list(self.clipboard.get_keys()))
        if dialog.exec_():
            col_offset = dialog.getResults()["spbox"]-1
            key = dialog.getResults()["cbbox"]
            self.clipboard.save_to_medium(key=key, colOffset=col_offset)
        
        
        
class MLToolbar(SingleToolbar):
    def __init__(self, *args, **kwargs):
        SingleToolbar.__init__(self, "ml_toolbar", *args, **kwargs)

        
        model_selection = ToolComboBox(
            ["auto"]+list(LinearModel._supported_models.keys()), "Select model")
        fit = ToolPushButton(
            QtGui.QIcon(":/images/fit_model.png"), "Fit model", self.fit_regression_model)
        regression_buttons = [(model_selection, 1, 0, 1, 1), (fit, 1, 1, 1, 1)]    
        self.addRegion("Regression", 0, 2, 2, 2, *regression_buttons)

        
        model_selection = ToolComboBox(
            ["auto"]+list(MultiModelClassifier._supported_models.keys()), "Select model")
        fit = ToolPushButton(
            QtGui.QIcon(":/images/fit_model.png"), "Fit model", self.fit_regression_model)
        classification_buttons = [(model_selection, 1, 0, 1, 1), (fit, 1, 1, 1, 1)] 
        self.addRegion("Classification", 0, 5, 2, 2, *classification_buttons)

        self.pca_types = {}
        self.pca_types['auto'] = ToolPushButton(
            QtGui.QIcon(":/images/auto_pca.png"), "Automatic PCA", lambda : self.selectPCAType('auto'))
        self.pca_types['auto'].setCheckable(True)
        self.pca_types['incremental'] = ToolPushButton(
            QtGui.QIcon(":/images/inc_pca.png"), "Incremental PCA", lambda : self.selectPCAType('incremental'))
        self.pca_types['incremental'].setCheckable(True)
        self.pca_types['kernel'] = ToolPushButton(
            QtGui.QIcon(":/images/kernel_pca.png"), "Kernel PCA", lambda : self.selectPCAType('kernel'))
        self.pca_types['kernel'].setCheckable(True)
        fit_pca = ToolPushButton(
            QtGui.QIcon(":/images/fit_model.png"), "Fit PCA", self.fitPCA)
        trans_pca = ToolPushButton(
            QtGui.QIcon(":/images/trans_pca.png"), "Transform data", self.transPCA)
        reduction_buttons = [(self.pca_types['auto'], 1, 0, 1, 1),
                             (self.pca_types['incremental'], 1, 1, 1, 1),
                             (self.pca_types['kernel'], 1, 2, 1, 1),
                             (fit_pca, 1, 3, 1, 1), (trans_pca, 1, 4, 1, 1)]
        self.addRegion("Reduction", 0, 8, 2, 5, *reduction_buttons)

        
        model_selection = ToolComboBox(
            ["auto"]+list(ClusteringModel._supported_models.keys()), "Select model")
        fit = ToolPushButton(
            QtGui.QIcon(":/images/fit_model.png"), "Fit model", self.fit_regression_model)
        clustering_buttons = [(model_selection, 1, 0, 1, 1), (fit, 1, 1, 1, 1)] 
        self.addRegion("Clustering", 0, 16, 2, 2, *clustering_buttons)


    def fit_regression_model(self):
        pass

    def fit_classification_model(self):
        pass

    def fit_clustering_model(self):
        pass

    def selectPCAType(self, pca_type):
        for key, val in self.pca_types.items():
            if key == pca_type:
                val.setChecked(True)
            else:
                val.setChecked(False)

        dialog = InputDialog("PCA parameters")
        dialog.addWidget("label", "label1", 0, 0, 1, 1, text="Number of features:")
        dialog.addWidget("spin_box", "spbox", 0, 1, 1, 1, _range=(1,100))
        dialog.addWidget("label", "label2", 1, 0, 1, 1, text="Additional parameters\n(e.g. {'random_state':None}")
        dialog.addWidget("text_input", "txt", 2, 0, 1, 2)
        if dialog.exec_():
            n_features = dialog.getResults()["spbox"]
            try:
                params = ast.literal_eval(dialog.getResults()["txt"])
            except SyntaxError:
                params = {}
            self.pca_model = PCAReductor(pca_type, n_features, **params)
            self.pca_model.isfit = False
            
        
    def fitPCA(self):
        if self.pca_model is not None:
            try:
                data = self.clipboard.get_data(SELECTION)
                self.pca_model.fit(data.get_data())
                self.pca_model.isfit = True
            except KeyError:
                raise Exception("No data loaded")
        else:
            raise Exception("No model selected")
        

    def transPCA(self):
        if self.pca_model is not None and self.pca_model.isfit:
            try:
                data = self.clipboard.get_data(SELECTION)
                self.clipboard.store_data(Data(self.pca_model.transform(data.get_data())), TRANSFORMED)
            except KeyError:
                raise Exception("No data loaded")
        else:
            raise Exception("Please fit a PCA reductor first")
        
    def retranslateUi(self, _translate):
        for widget in self.labels+self.buttons:
            if isinstance(widget, ToolComboBox):
                widget.retranslateUi(_translate)
            else:
                widget.setText(_translate("MainWindow", widget.text()))


        
class PlotToolbar(SingleToolbar):
    def __init__(self, plotting_space, *args, **kwargs):
        SingleToolbar.__init__(self, "plot_toolbar", *args, **kwargs)

        self.plotting_space = plotting_space

        # Visual region (e.g. modify grid/colors?)
        self.addRegion("Visual", 0, 2, 2, 1)
        
        # Basic plots region
        pie_plot_button = ToolPushButton(QtGui.QIcon(":/images/pie_plot.jpg"), "Pie plot", self.pie_plot)
        basic_plots_buttons = [(pie_plot_button, 1, 0, 1, 1)]
        bar_plot_button = ToolPushButton(QtGui.QIcon(":/images/bar_plot.png"), "Bar plot", self.bar_plot)
        basic_plots_buttons.append((bar_plot_button, 1, 1, 1, 1))
        
        self.addRegion("Basic plots", 0, 4, 2, 2, *basic_plots_buttons)
        self.addRegion("Statistical plots", 0, 7, 2, 1)

    def pie_plot(self):
        #PlottingService.build_plot("", 'Pie', 'Pie plot', self.data).plot(axes[0][1])
        pass

    def bar_plot(self):
        pass
    
    
        
class ToolPushButton(QtWidgets.QPushButton):
    # A class to facilitate making of pushbuttons with adequate size for the toolbar,
    # no text, an icon and a tooltip
    def __init__(self, icon, text, function, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, icon, "", *args, **kwargs)
        self.setToolTip(text)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)
        self.pressed.connect(function)

    def sizeHint(self):
        return QtCore.QSize(30,30)


class ToolComboBox(QtWidgets.QComboBox):
    def __init__(self, items, tooltip, *args, **kwargs):
        QtWidgets.QComboBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("selection-color: rgb(0, 0, 0);selection-background-color: rgb(255, 255, 255);")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)
        self.setToolTip(tooltip)
        for item in items:
            self.addItem(item)

    def retranslateUi(self, _translate):
        for i in range(self.count()):
            self.setItemText(i, _translate("MainWindow", self.itemText(i)))
