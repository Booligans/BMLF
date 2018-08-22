from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(273, 278)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 210, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(20, 70, 111, 21))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 130, 121, 21))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 100, 121, 21))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_4.setGeometry(QtCore.QRect(20, 160, 101, 21))
        self.checkBox_4.setObjectName("checkBox_4")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 251, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox.setText(_translate("Dialog", "Machine Learning"))
        self.checkBox_2.setText(_translate("Dialog", "Plotting"))
        self.checkBox_3.setText(_translate("Dialog", "Statistical Analysis"))
        self.checkBox_4.setText(_translate("Dialog", "Data Analysis"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Select the modules you want to add</span></p></body></html>"))

class InputDialog(QtWidgets.QDialog):

    def __init__(self, title, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)

        self.setWindowTitle(title)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setSpacing(5)

        self.centralWidget = QtWidgets.QWidget()
        self.verticalLayout.addWidget(self.centralWidget)
        
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.widgets = {}
        self.results = {}

        self.bottomWidget = QtWidgets.QWidget()
        self.verticalLayout.addWidget(self.bottomWidget)

        self.horLayout = QtWidgets.QHBoxLayout(self.bottomWidget)
        self.horLayout.setContentsMargins(0,0,0,0)
        self.horLayout.setSpacing(5)
        
        self.accept_ = QtWidgets.QPushButton("Accept")
        self.horLayout.addWidget(self.accept_)
        self.accept_.clicked.connect(self.accept)

        self.reject_ = QtWidgets.QPushButton("Cancel")
        self.horLayout.addWidget(self.reject_)
        self.reject_.clicked.connect(self.reject)

    def addWidget(self, _type, name, row, col, rowSpan, colSpan, *args, text='', icon=None, items=[], group=None, _range=None, **kwargs):
        """
        Types: check_box, radio_btn, btn_group, text_input, label, combo_box, spin_box
        The row, col, rowSpan and colSpan paramenters control the position and size
        of each widget. The text, icon and items parameters can be used with related types
        (items with combo_box, text with every one, icon with buttons, group with radio buttons,
        range with spin_box)
        """
        if _type == 'label':
            widget = QtWidgets.QLabel(text)
        elif _type == 'radio_btn':
            parent = self.centralWidget if group is None else self.widgets[group]
            widget = QtWidgets.QRadioButton(text, parent)
            widget.toggled.connect(lambda x: self.state_changed(name,x))
            self.widgets[name] = widget
            widget = None
        elif _type == 'btn_group':
            widget = QtWidgets.QButtonGroup(self.centralWidget)
        elif _type == 'check_box':
            widget = QtWidgets.QCheckBox(text, self.centralWidget)
            widget.stateChanged.connect(lambda x: self.state_changed(name, x))
            widget.stateChanged.emit(False)
        elif _type == 'text_input':
            widget = QtWidgets.QPlainTextEdit(text, self.centralWidget)
            widget.textChanged.connect(lambda: self.text_changed(name))
            self.results[name] = ''
        elif _type == 'combo_box':
            widget = QtWidgets.QComboBox(self.centralWidget)
            widget.addItems(items)
            widget.currentIndexChanged[str].connect(lambda x: self.state_changed(name, x))
            widget.currentIndexChanged[str].emit(items[0])
        elif _type == 'spin_box':
            widget = QtWidgets.QSpinBox(self.centralWidget)
            widget.setRange(*_range)
            widget.valueChanged[int].connect(lambda x: self.state_changed(name, x))
            widget.valueChanged[int].emit(1)
        else:
            raise ValueError("Type {} not recognized".format(_type))
        

        if widget is not None:
            self.widgets[name] = widget
            self.gridLayout.addWidget(widget, row, col, rowSpan, colSpan)

            
    def getResults(self):
        return self.results

    def state_changed(self, name, state):
        self.results[name] = state

    def text_changed(self, name):
        self.results[name] = self.widgets[name].toPlainText()
