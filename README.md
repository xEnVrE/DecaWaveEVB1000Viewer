# DecaWaveEVB1000Viewer
DecaWaveEVB1000 Viewer is a 3D viewer with logging capabilities for the DecaWave EVB1000 system.

Usage
------------
Python 3.x is required.

Libraries required are
 * Matplotlib
 * PySerial
 * PyQt5

- **On Linux:**
```
    $ git clone https://github.com/xEnVrE/DecaWaveEVB1000Viewer.git
    $ cd DecaWaveEVB1000Viewer.git
    $ python app.py
```
> You may need to add your user to the group that owns serial port device files  (e.g. /dev/ttyACM0) to 
     execute the application succesfully. However you can always run the script as a super user like
     ```
     sudo python app.py
     ```

The application works also on Windows.
  
Configuration
-------------
The only thing you need to run the application is a configuration file `config.ini` containing the VIDs and PIDs of
USB serial ports you would like to use with the application.  
The structure of the file is quite simple
```
CONFIG_VID_PID
VID PID
<vid_1> <pid_1>
...
<vid_N> <pid_N>
```
