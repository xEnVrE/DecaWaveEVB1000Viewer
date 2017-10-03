# sys
import sys

# GUI
from ui.gui import EVB1000ViewerMainWindow
from PyQt5.QtWidgets import QApplication

# DeviceManager
from device.device_manager import DeviceManager
from device.device_manager import DeviceVIDPIDList

if __name__ == '__main__':

    # load VIDs and PIDs from config.ini
    vid_pid_list = DeviceVIDPIDList('config.ini')

    # instantiate device_manager
    dev_man = DeviceManager(vid_pid_list)

    # instantiate a QApplication
    app = QApplication(sys.argv)

    # instantiate the main window
    gui = EVB1000ViewerMainWindow(dev_man)

    # show the main window
    gui.show()

    # start the device manager
    dev_man.start()
    
    sys.exit(app.exec_())


    
