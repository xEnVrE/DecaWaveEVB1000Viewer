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

    Inherits from threading.Thread to handle serial i/o operations
    in background.
    """

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
        self.id = hash(self.port)

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
                line_byte = self.serial.readline()
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

class DeviceManager(QThread):
    """
    Manage EVB1000 Tag devices connected through a serial port.
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
                self._new_devices = self.configure_devices(new_ports)

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
            # device id is defined as port.__hash__()
            device_id = hash(p)
            self.configured_devices[device_id].stop_device()

    def update_ports(self):
        """
        Update list of serial ports connected.

        New ports are added to connected_ports if the underlying
        usb device match the target VID and PID.
        Missing ports are remove from connected_ports.

        Return a list containing new devices.
        Return a list containing removed devices.
        """
        
        # fetch only those ports having
        # VID:PID == target_vid:target_pid
        vid_pid = self.target_vid + ':' + self.target_pid
        ports = [p for p in list_ports.grep(vid_pid)]
        
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
    
    def __init__(self, DM):
        # call Thread constructor
        QThread.__init__(self)
        self.DM = DM
        self.DM.register_new_devices_connected_slot(self.new_devices_connected)

    @pyqtSlot()
    def new_devices_connected(self):
        devs = self.DM.new_devices
        for dev in devs:
            print(dev.port.device)

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
