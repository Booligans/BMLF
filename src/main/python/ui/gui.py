import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from .mainWindow import *

class MainWindow(QMainWindow):
    def __init__(self, screen_res, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow(screen_res)
        self.ui.setupUi(self)
