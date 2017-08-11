# sys
import sys

# GUI
from gui import EVB1000ViewerMainWindow
from PyQt5.QtWidgets import QApplication

# DeviceManager
from device_manager import DeviceManager

if __name__ == '__main__':

    # instantiate device_manager
    dev_man = DeviceManager(target_vid = '0403', target_pid = '6001')
    dev_man.start()

    # instantiate a QApplication
    app = QApplication(sys.argv)

    # instantiate the main window
    gui = EVB1000ViewerMainWindow(dev_man)

    # show the main window
    gui.show()
    
    sys.exit(app.exec_())


    
