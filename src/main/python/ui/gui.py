import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import mainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
if __name__ == '__main__':
    print('Launching app')
    app = QApplication(sys.argv)
    window = MainWindow()
    if (window.ui.file != ""):
        window.show()
        app.exec_()