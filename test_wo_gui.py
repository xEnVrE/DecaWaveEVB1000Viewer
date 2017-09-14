# sys
import sys

# QtWidgets contains QApplication
from PyQt5 import QtWidgets

# DeviceManager
from device.device_manager import DeviceManager
from device.device_manager import DeviceVIDPIDList

# multi-threading
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
        
class MockGUI(QThread):
    """
    Mock GUI class to test slot-signal connection
    """
    
    def __init__(self, dev_man):
        # call Thread constructor
        QThread.__init__(self)

        # save reference to instance of the device manager
        self.dev_man = dev_man
        self.dev_man.register_new_devices_connected_slot(self.new_devices_connected)

    @pyqtSlot()
    def new_devices_connected(self):
        # get new devices
        devs = self.dev_man.new_devices

        # connect new_data_available to slot of each device
        for dev in devs:
            print('New device connected: ' + dev.port.device)
            dev.register_new_data_available_slot(self.new_data_available)

    @pyqtSlot(str)
    def new_data_available(self, device_id):
        
        # retrieve device from device manager
        device = self.dev_man.device(device_id)

        # print new data
        print(device_id + ' ' + str(device.last_data))

    def run(self):
        while True:
              pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # load VIDs and PIDs from config.ini
    vid_pid_list = DeviceVIDPIDList('config.ini')

    dev_man = DeviceManager(vid_pid_list)
    dev_man.start()

    gui = MockGUI(dev_man)
    gui.start()

    sys.exit(app.exec_())
