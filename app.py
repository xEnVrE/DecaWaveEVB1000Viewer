# sys
import sys

# GUI
from ui.gui import EVB1000ViewerMainWindow
from PyQt5.QtWidgets import QApplication

# DeviceManager
from device.device_manager import DeviceManager

if __name__ == '__main__':

    # instantiate device_manager
    dev_man = DeviceManager(target_vid = '0483', target_pid = '5740')

    # instantiate a QApplication
    app = QApplication(sys.argv)

    # instantiate the main window
    gui = EVB1000ViewerMainWindow(dev_man)

    # show the main window
    gui.show()

    # start the device manager
    dev_man.start()
    
    sys.exit(app.exec_())


    
