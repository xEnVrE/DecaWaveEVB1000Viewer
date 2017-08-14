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

# EVB1000 decoder
from decoder import DataFromEVB1000

# CSV loffer
from csv_logger import CSVLogger

# serial reading testing
from struct import pack
from trilateration_data_csv import TrilaterationData

anchor_positions_sent = False
fake_data = TrilaterationData('trilat_data.csv')

def float_to_hex_string(value):
    """
    Transform float to a string
    containing its hexadecimal representation
    """
    hex_string = ''
    
    # pack as a float
    packed_value = pack('>f', value)
        
    for byte in packed_value:
        # extract string of
        # hexadecimal representation of byte
        hex_str = str(hex(byte))
        
        # remove the heading '0x'
        hex_str = hex_str[2:]

        # str removes padding zero
        # it is required to insert it again
        if len(hex_str) == 1:
            hex_str = '0' + hex_str

        # append to hex_string
        hex_string += hex_str

    return hex_string

def fake_serial_readline(self):
    """
    Fake serial readline() method for testing purposes
    """

    global anchor_positions_sent
    global fake_data

    # empty line
    line = ''

    if not anchor_positions_sent:

        # anchor positions are now "sent"
        anchor_positions_sent = True
        
        # set anchor position report message type
        line += 'apr'
        line += ' '
        
        # set tag id
        line += '00'
        line += ' '

        # set anchor 0 cartesian positions
        line += float_to_hex_string(0)
        line += ' '
        line += float_to_hex_string(0)
        line += ' '
        line += float_to_hex_string(0)
        line += ' '

        # set anchor 1 cartesian positions
        line += float_to_hex_string(0)
        line += ' '
        line += float_to_hex_string(17.7758)
        line += ' '
        line += float_to_hex_string(0)
        line += ' '

        # set anchor 2 cartesian positions
        line += float_to_hex_string(10.7935)
        line += ' '
        line += float_to_hex_string(4.8023)
        line += ' '
        line += float_to_hex_string(0)
        line += ' '

        # set anchor 3 cartesian positions
        line += float_to_hex_string(4.3826)
        line += ' '
        line += float_to_hex_string(7.7982)
        line += ' '
        line += float_to_hex_string(1.4259)

        # close line
        line += '\r\n'

    else:
        # set anchor position report message type
        line += 'tpr'
        line += ' '
        
        # set tag id
        line += '00'
        line += ' '

        # get new position from fake_data
        pos = fake_data.get_new_value()

        x = pos[0]
        y = pos[1]
        z = pos[2]

        # set position
        line += float_to_hex_string(x)
        line += ' '
        line += float_to_hex_string(y)
        line += ' '
        line += float_to_hex_string(z)
        
        # close line
        line += '\r\n'

    return line

serial.Serial.readline = fake_serial_readline

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

        # instantiate a new csv logger
        self._logger = CSVLogger()

    def __str__(self):
        return self.port.device

    @property
    def logger(self):
        return self._logger

    @property
    def last_data(self):
        self.data_lock.acquire()

        data = self._last_data
        
        self.data_lock.release()

        return data

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

        # gracefully stop thread if the connection is not working
        # TODO: signal the GUI that an I/O error occured
        if not self.connect():
            return
        
        while self.state == 'running':
            try:
                # attempt reception of a new line
                line = self.serial.readline()
                
                # process only non null data
                if len(line) > 0:

                    # store new line received
                    # access to last_data here may happen *before*
                    # the GUI has requested the data related to the last
                    # signal emission. In this case the old line is overwritten
                    # by the new one.
                    #
                    # TODO: consider a buffered approach
                    #
                    
                    # decode last line received
                    evb1000_data = DataFromEVB1000(line)

                    # continue only if message type was decoded successfully
                    if evb1000_data.msg_type_decoded:
                        # store data
                        self.last_data = evb1000_data.decoded

                        # signal the GUI that new data is available
                        self.new_data_available.emit(self.id)

                        # log to file
                        self.logger.log_data(evb1000_data)

            except SerialException:
                pass

            # test a framerate of 100Hz
            sleep(1.0 / 100.0)

        if self.state == 'stopped':
            # close csv file
            self.logger.close()
            
            # stop thread
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

        # in Windows even if the device is detected it
        # may be not ready to be opened yet
        while not self.serial.is_open:
            try:
                self.serial.open()
            except SerialException:
                pass
            
        return True

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
    new_dev_connected_sig = pyqtSignal()
    dev_removed_sig = pyqtSignal()
    
    def __init__(self, target_vid, target_pid):


        # call Thread constructor
        QThread.__init__(self)

        # empty list of ports
        self.connected_ports = []

        # empty dictionary of devices
        self.configured_devices = dict()

        # empty list of *newly* configured devices
        self._new_devices = []
        # empty list of *just* removed  devices
        self._removed_devices = []

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

    @property
    def removed_devices(self):

        # copy new devices
        devs = self._removed_devices

        # clean _new_devices
        self._removed_devices = []
        
        return devs

    @removed_devices.setter
    def removed_devices(self, devs):
        self._removed_devices = devs

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
                self.new_dev_connected_sig.emit()

            # in case of removed ports
            if removed_ports:
                # removed devices that were disconnected
                self.removed_devices = self.remove_devices(removed_ports)

                # signal GUI that some devices were removed
                self.dev_removed_sig.emit()

            # wait some time
            sleep(1)

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

        Return a list containing the removed devices.
        """

        removed_devices = []

        # for each port change the state of the underlying thread
        # from 'running' to 'stopped' using stop_device()
        for p in ports:
            # device id is defined as str(port.__hash__())
            device_id = str(hash(p))
            self.configured_devices[device_id].stop_device()
            
            # clean configured_devices dict
            removed_device = self.configured_devices.pop(device_id)
            removed_devices.append(removed_device)

        return removed_devices

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
        self.new_dev_connected_sig.connect(slot)

    def register_devices_removed_slot(self, slot):
        self.dev_removed_sig.connect(slot)
        
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
