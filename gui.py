#PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
import sys

# QtDesigner generated classes
from evb1000viewer import Ui_EVB1000ViewerMainWindow

# TagItem widget class
from tag_item import TagItem

# ColorPalette
import color_palette

# Matplotlib class
from matplotlib_viewer_canvas import MatplotlibViewerCanvas

# for logging
from time import localtime, strftime

class EVB1000ViewerMainWindow(QtWidgets.QMainWindow):
    """
    Main window class of EVB1000 Viewer
    """
    def __init__(self, device_manager = None):
        # call QMainWindow constructor
        super().__init__()

        # set up the user interface
        self.ui = Ui_EVB1000ViewerMainWindow()
        self.ui.setupUi(self)

        # connect action buttons
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionQuit.triggered.connect(self.quit)

        # instantiate the Logger
        self.logger = Logger(self.ui.logLabel, self.ui.logScrollArea)

        # store the Device Manager 
        self.dev_man = device_manager
        # register new_devices_connected slot
        if self.dev_man != None:
            self.dev_man.register_new_devices_connected_slot(self.new_devices_connected)
            self.dev_man.register_devices_removed_slot(self.devices_removed)
        
        # empty dictionary of tags widgets
        self.tags_widgets = dict()

        # empty matplotlib canvas
        self.mpl_canvas = None

        # instantiate the color palette
        self.palette = color_palette.ColorPalette()

        # remeber if the anchors position were already set 
        self.anc_positions_set = False
        
    @pyqtSlot()
    def new_devices_connected(self):
        """
        Handle new devices connected.
        """
        # get new devices
        devs = self.dev_man.new_devices

        for dev in devs:
            
            # log event
            self.logger.ev_tag_connected(str(dev))

            # register new_data_available slot
            dev.register_new_data_available_slot(self.new_data_available)

            # add tag widget to the layout
            # device id is used as key
            self.tags_widgets[dev.id] = TagItem(self.ui, str(dev))

    @pyqtSlot()
    def devices_removed(self):
        """
        Handle devices removed.
        """
        # get removed devices
        devs = self.dev_man.removed_devices

        for dev in devs:

            # recover tag widget from dictionary
            widget = self.tags_widgets.pop(dev.id)
            
            # log event
            self.logger.ev_tag_removed(widget.tag_id)

            # remove widget from layout
            widget.remove_from_layout()
            
            # remove refeernce to widget
            widget = None


    @pyqtSlot(str)
    def new_data_available(self, device_id):
        
        # retrieve device from device manager
        try:
            device = self.dev_man.device(device_id)
        except KeyError:
            # this could happen if a device has been removed
            # by the Device Manager but the associated thread
            # hasn't stopped yet
            return

        # get last data
        data = device.last_data

        # handle according to message type
        if data['msg_type'] == 'tpr':
            self.handle_tag_report_rcvd(device_id, data)
        elif data['msg_type'] == 'apr':
            self.handle_anch_report_rcvd(data)

    def handle_tag_report_rcvd(self, device_id, data):
        """        
        Handle the reception of a Tag Position Report message
        """
        
        # get the Tag widget 
        widget = self.tags_widgets[device_id]

        # get Tag ID
        tag_id = data['tag_id']

        # data from tags are plotted only if the anchors position are already set
        # and the matplotlib canvas is configured to show them
        if self.anc_positions_set:

            # in case the Tag device with ID <tag_id> was never connected
            # it is initialized inside mpl_canvas
            if not self.mpl_canvas.is_tag_view(tag_id):

                # pick a new color
                c = self.palette.get_new_color()
                
                # initialize tag in Matplotlib canvas
                self.mpl_canvas.set_new_tag(tag_id, c)

            # these actions are performed when the *first message*
            # arrives from *both* a newly connected tag or a tag
            # that was connected in the past
            if not widget.is_tag_id_set:
                
                # set widget Tag ID
                widget.tag_id = tag_id

                # take the color used for the tag
                c = self.mpl_canvas.get_tag_color(tag_id)
                
                # set widget label color
                widget.tag_id_color = c.color_255
                
            # get Tag position
            x = data['x']
            y = data['y']
            z = data['z']
                
            # update canvas with new position
            self.mpl_canvas.set_tag_position(tag_id, x, y, z)
                
            # update widget with new position
            widget.position = (x, y, z)

    def handle_anch_report_rcvd(self, data):
        """
        Handle the reception of a Anchor Position Report message    
        """

        # extract Anchors position
        a0 = [data['a0_x'], data['a0_y'], data['a0_z']]
        a1 = [data['a1_x'], data['a1_y'], data['a1_z']]
        a2 = [data['a2_x'], data['a2_y'], data['a2_z']]
        a3 = [data['a3_x'], data['a3_y'], data['a3_z']]
        
        # instantiate MatplotlibViewerCanvas
        frame_rate = 25.0
        tag_positions_buffer_size = 10
        self.mpl_canvas = MatplotlibViewerCanvas(self.ui.matPlotGroupBox,\
                                                 frame_rate,\
                                                 tag_positions_buffer_size)

        # evaluate basis change according to the z coordinate
        # of the fourth anchor
        anchor_3_height_z = a3[2]
        self.mpl_canvas.eval_basis_change(anchor_3_height_z)

        #TODO add in Gui
        self.mpl_canvas.anchors_plane_height = 1

        # set anchor positions (test)
        self.mpl_canvas.set_anchor_position([a0, a1, a2, a3])
        
        # eval and set figure limits
        self.mpl_canvas.eval_figure_limits()
        self.mpl_canvas.set_axes_limits()

        # draw anchors, plane and reference frame of anchor 0
        self.mpl_canvas.draw_static_objects()

        # add canvas to the main window
        self.ui.matPlotGroupBoxLayout.addWidget(self.mpl_canvas)

        self.anc_positions_set = True
        
    def about(self):
        """
        About method.

        Method called when actionAbout is triggered.
        """
        QtWidgets.QMessageBox.about(self, "About",
                                    """ TODO """)

    def quit(self):
        """
        Quit method.

        Method called when actionQuit is triggered.
        """
        self.close()

class Logger:
    """
    Logger class shows events during the execution of the viewer.
    """
    
    def __init__(self, log_widget, scroll_area):

        # set log widget from main window
        self.log_widget = log_widget

        # set scroll area form main window
        self.scroll_area = scroll_area

        # print welcome message
        txt = "EVB1000 Viewer started."
        self.write_to_log(txt)
        
    def ev_tag_id_recognized(self, tag_id):
        """
        Log a "tag id recognized" event.
        """
        
        txt = "Tag " + str(tag_id) + " is sending data."
        self.write_to_log(txt)

    def ev_tag_connected(self, device_port):
        """
        Log a "new tag connected" event.
        """
                
        txt = "New tag connected at " + device_port  + "."
        self.write_to_log(txt)

    def ev_tag_removed(self, tag_id):
        """
        Log a "removed tag" event.
        """
        
        txt = "Tag " + str(tag_id) + " removed."
        self.write_to_log(txt)

    def write_to_log(self, text):
        """
        Log the text "text" with a timestamp.
        """

        # extract current text from the log widget
        current_text = self.log_widget.text()

        # compose new text
        # convert local time to string
        time_str = strftime(" [%H:%M:%S] ", localtime())
        # 
        new_text = current_text + time_str + text + "\n"

        # log into the widget
        self.log_widget.setText(new_text)

        # scroll down text
        self.scroll_down()

    def scroll_down(self):
        """
        Scroll down the slider of the scroll area
        linked to this logger
        """
        # extract scroll bar from the scroll area
        scroll_bar = self.scroll_area.verticalScrollBar()

        # set maximum value of the slider, 1000 is enough
        scroll_bar.setMaximum(1000)
        scroll_bar.setValue(scroll_bar.maximum())
            
if __name__ == '__main__':
        
    # construct a QApplication
    app = QtWidgets.QApplication(sys.argv)

    # instantiate the main window and add the Matplotlib canvas
    gui = EVB1000ViewerMainWindow()

    # logger testing
    gui.logger.ev_tag_connected("/dev/ttyUSB0")
    gui.logger.ev_tag_id_recognized("0")
    gui.logger.ev_tag_removed("0")

    # show the main window
    gui.show()
    
    sys.exit(app.exec_())
