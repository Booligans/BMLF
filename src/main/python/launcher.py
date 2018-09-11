import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.gui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen_res = app.desktop().screenGeometry()
    window = MainWindow(screen_res)
    if (window.ui.file != ""):
        window.show()
        app.exec_()        
        
