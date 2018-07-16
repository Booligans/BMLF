import sys
from unittest import TestCase, skip
from PyQt5.QtWidgets import QApplication
from ui.gui import MainWindow

class TestUi(TestCase):

    @skip("UI test disabled")
    def test_init(self):
        # Test if UI is correctly started. Since this test requires user interaction
        # to continue, I have disabled it. Comment the annotation to run it.
        print('Launching app')
        app = QApplication(sys.argv)
        window = MainWindow()
        if (window.ui.file != ""):
            window.show()
            app.exec_()        
