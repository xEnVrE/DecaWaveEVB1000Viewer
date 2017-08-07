# pyserial
from serial.tools import list_ports

class EVB1000Discovery:
    """
    Manage EVB1000 Tag devices connected through a serial port.
    """
    
    def __init__(self, target_vid, target_pid):

        # list of empty devices
        self.connected_devices = []

        # store pid and vid for the target device of interest
        self.target_vid = target_vid
        self.target_pid = target_pid

    def update_devices(self):
        """
        Update list of serial ports connected.

        New ports are added to connected_devices if the underlying
        usb device match the target VID and PID.
        Missing ports are remove from connected_devices.

        Return a list containing new devices.
        Return a list containing removed devices.
        """
        
        # fetch only those ports having
        # VID:PID == target_vid:target_pid
        vid_pid = self.target_vid + ':' + self.target_pid
        ports = [p for p in list_ports.grep(vid_pid_re)]
        
        # add new ports to connected_devices
        # and update new_ports
        new_ports = []
        for p in ports:
            if not p in self.connected_devices:
                self.connected_devices.append(p)
                new_ports.append(p)

        # remove missing ports from devices_found
        # and update removed_ports
        removed_ports = []
        for p in self.connected_devices:
            if not p in ports:
                self.connected_devices.remove(p)
                removed_ports.append(p)

        return new_ports, removed_ports

if __name__ == '__main__':
    discover = EVB1000Discovery(target_vid = '0403', target_pid = '6001')

    while (1):
        new_ports, removed_ports = discover.update_devices()
        if new_ports:
            print('New ports:')
            print(new_ports)
            for p in new_ports:
                print(p)
                print(p.hwid)
        if removed_ports:
            print('Removed ports:')
            print(removed_ports)
    
