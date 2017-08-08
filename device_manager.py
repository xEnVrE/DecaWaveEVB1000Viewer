# pyserial
import serial
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo
from serial.serialutil import SerialException

# make ListPortInfo hashable
def hash_fun(self):
    return hash(str(self))
ListPortInfo.__hash__ = hash_fun

# multi-threading
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from threading import Lock

# sleep
from time import sleep

# sys
import sys

# QtWidgets contains QApplication
from PyQt5 import QtWidgets

class Device(QThread):
    """
    Represents an EVB1000 Tag connected through a serial port.

    Inherits from QThread to handle serial i/o operations
    in background.
    """

    #pyqt signals are class attributes
    new_data_available = pyqtSignal(str)

    def __init__(self, port):
        # call Thread constructor
        QThread.__init__(self)
        
        # save port
        self.port = port

        # configure device
        self.configure()

        # set device state
        self._state = 'running'
        self.state_lock = Lock()

        # set device id
        self.id = str(hash(self.port))

        # data
        self._last_data = None
        self.data_lock = Lock()

    @property
    def last_data(self):
        self.data_lock.acquire()
        value = self._last_data
        self.data_lock.release()

        return value

    @last_data.setter
    def last_data(self, data):
        self.data_lock.acquire()
        self._last_data = data
        self.data_lock.release()
        
    @property
    def state(self):
        self.state_lock.acquire()
        value = self._state
        self.state_lock.release()
        
        return self._state

    @state.setter
    def state(self, new_state):
        self.state_lock.acquire()
        self._state = new_state
        self.state_lock.release()

    def stop_device(self):
        """
        Change the state of the device from 'running' to 'stopped'.
        """

        self.state = 'stopped'

    def run(self):
        """
        Thread main method.
        """

        if not self.connect():
            return
        
        while self.state == 'running':
            try:
                self.last_data = self.serial.readline()

                # signal the GUI that new data is available
                self.new_data_available.emit(self.id)

            except SerialException:
                pass

        if self.state == 'stopped':
            self.close()

    def configure(self):
        """
        Get a serial.Serial instance and configure it.
        """

        # instantiate Serial
        self.serial = serial.Serial()

        # set port_path, e.g. '/dev/ttyUSBx' or 'COMx'
        self.serial.port = self.port.device

        # set baudrate
        self.serial.baudrate = 115200

    def connect(self):
        """
        Open the serial port.

        return Serial.is_open
        """

        self.serial.open()

        return self.serial.is_open

    def close(self):
        """
        Close the serial port.

        return Serial.is_open
        """

        self.serial.close()

    def register_new_data_available_slot(self, slot):
        self.new_data_available.connect(slot)


class DeviceManager(QThread):
    """
    Manage EVB1000 Tag devices connected through a serial port.

    Inherits from QThread to handle devices connection/disconnection
    in background.
    """

    #pyqt signals are class attributes
    new_devices_connected = pyqtSignal()
    
    def __init__(self, target_vid, target_pid):


        # call Thread constructor
        QThread.__init__(self)

        # empty list of ports
        self.connected_ports = []

        # empty dictionary of devices
        self.configured_devices = dict()

        # empty list of *newly* configured devices
        self._new_devices = []

        # store pid and vid for the target device of interest
        self.target_vid = target_vid
        self.target_pid = target_pid

    @property
    def new_devices(self):

        # copy new devices
        devs = self._new_devices

        # clean _new_devices
        self._new_devices = []
        
        return devs

    @new_devices.setter
    def new_devices(self, devs):
        self._new_devices = devs

    def device(self, device_id):
        return self.configured_devices[device_id]
    
    def run(self):
        """
        Thread main method.
        """

        while True:
            # update new and removed ports
            new_ports, removed_ports = self.update_ports()
                
            # in case of new ports
            if new_ports:
                # configure devices connected to ports in new_ports
                self.new_devices = self.configure_devices(new_ports)

                # signal GUI that new devices are available
                self.new_devices_connected.emit()

            # in case of removed ports
            if removed_ports:
                # removed devices that were disconnected
                self.remove_devices(removed_ports)

    def configure_devices(self, ports):
        """
        Configure devices connected via serial ports in ports.

        Return a list containing the new devices.
        """

        new_devices = []
        
        # for each port create a new Device and start the underlying thread
        for p in ports:
            new_device = Device(p)
            self.configured_devices[new_device.id] = new_device
            new_devices.append(new_device)
            new_device.start()

        return new_devices

    def remove_devices(self, ports):
        """
        Remove devices whose ports were removed.
        """

        # for each port change the state of the underlying thread
        # from 'running' to 'stopped' using stop_device()
        for p in ports:
            # device id is defined as str(port.__hash__())
            device_id = str(hash(p))
            self.configured_devices[device_id].stop_device()

    def update_ports(self):
        """
        Update list of serial ports connected.

        New ports are added to connected_ports if the underlying
        usb device match the target VID and PID.
        Missing ports are remove from connected_ports.

        Return a list containing new ports.
        Return a list containing removed ports.
        """
        
        # fetch only those ports having
        # VID:PID == target_vid:target_pid
        vid_pid = self.target_vid + ':' + self.target_pid
        ports = [p for p in list_ports.grep(vid_pid)]
        #ports = list_ports.comports()
        
        # add new ports to connected_ports
        # and update new_ports
        new_ports = []
        for p in ports:
            if not p in self.connected_ports:
                self.connected_ports.append(p)
                new_ports.append(p)

        # remove missing ports from devices_found
        # and update removed_ports
        removed_ports = []
        for p in self.connected_ports:
            if not p in ports:
                self.connected_ports.remove(p)
                removed_ports.append(p)

        return new_ports, removed_ports

    def register_new_devices_connected_slot(self, slot):
        self.new_devices_connected.connect(slot)

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

    dev_man = DeviceManager(target_vid = '0403', target_pid = '6001')
    dev_man.start()

    gui = MockGUI(dev_man)
    gui.start()

    sys.exit(app.exec_())
