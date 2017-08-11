#PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
import sys

# QtDesigner generated classes
from evb1000viewer import Ui_EVB1000ViewerMainWindow
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
        
        # empty dictionary of tags widgets
        self.tags_widgets = dict()

        # empty matplotlib canvas
        self.mpl_canvas = None

        # instantiate the color palette
        self.palette = color_palette.ColorPalette()

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


    @pyqtSlot(str)
    def new_data_available(self, device_id):
        
        # retrieve device from device manager
        device = self.dev_man.device(device_id)

        # print new data
        print(str(device) + '_'  + device_id + ': ' + str(device.last_data))

    def add_matplotlib_canvas(self):
        """
        Add Matplotlib canvas to the main window.
        """
        
        # instantiate MatplotlibViewerCanvas
        frame_rate = 100.0
        tag_positions_buffer_size = 70
        self.mpl_canvas = MatplotlibViewerCanvas(self.ui.matPlotGroupBox,\
                                        frame_rate,\
                                        tag_positions_buffer_size)

        # evaluate basis change according to the z coordinate
        # of the fourth anchor
        anchor_3_height_z = 1
        self.mpl_canvas.eval_basis_change(anchor_3_height_z)

        #TODO add in Gui
        self.mpl_canvas.anchors_plane_height = 1

        # set anchor positions (test)
        self.mpl_canvas.set_anchor_position([[0,0,0],[0,1,0],[2, -1, 0],[1, 2, 1]])
        
        # eval and set figure limits
        self.mpl_canvas.eval_figure_limits()
        self.mpl_canvas.set_axes_limits()

        # draw anchors, plane and reference frame of anchor 0
        self.mpl_canvas.draw_static_objects()

        # add new tag
        color = self.palette.get_new_color()
        self.mpl_canvas.set_new_tag('tag0', color)

        # add canvas to the main window
        self.ui.matPlotGroupBoxLayout.addWidget(self.mpl_canvas)

    def add_tag_widget(self, key, tag_id, port):
        """
        Add a new tag widget to the layout.
        """
        
        # instantiate a new TagItem
        tag_item = TagItem()
        tag_item.ui.tagIdLabelValue.setText(tag_id)
        tag_item.ui.portLabelValue.setText(port)
        tag_item.ui.rateLabelValue.setText("-")

        # add the widget to the dictionary
        self.tags_widgets[key] = tag_item

        # add the widget to the layout
        self.ui.connectedTagsScrollAreaWidgetLayout.insertWidget(0, tag_item)

    def remove_tag_widget(self, key):
        """
        Remove a tag widget from the layout.
        """
        import sip
        # retrieve widget from the dictionary
        widget = self.tags_widgets[key]

        # remove widget and its child from the layout 
        self.ui.connectedTagsScrollAreaWidgetLayout.removeWidget(widget)
        sip.delete(widget)

        # remove element from the dictionary
        del self.tags_widgets[key]
        
        # remove refeernce to widget
        widget = None
        
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
        
        txt = "Tag " + tag_id + " is sending data."
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
        
        txt = "Tag " + tag_id + " removed."
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
    gui.add_matplotlib_canvas()

    # tag widgets testing
    gui.add_tag_widget("TAG0", "Tag 0", "COM3")
    gui.add_tag_widget("TAG1", "Tag 1", "COM2")

    # logger testing
    gui.logger.ev_tag_connected("/dev/ttyUSB0")
    gui.logger.ev_tag_id_recognized("0")
    gui.logger.ev_tag_removed("0")

    # show the main window
    gui.show()
    
    sys.exit(app.exec_())
