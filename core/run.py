import sys
from PyQt5.QtWidgets import QApplication
from gui.gui import Main_Gui


def run_application():

    #Start application
    new_application = QApplication(sys.argv)
    window = Main_Gui()
    # Logic

    window.show()

    # End application
    sys.exit(new_application.exec_())