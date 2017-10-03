# QtDesigner generated classes
from ui.tag_item_ui import Ui_tagItem

# PyQt
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QColor, QPalette

import sip

class TagItem(QFrame):
    """
    Qt Widget wrapping the UI of a Tag item.
    """
    
    def __init__(self, parent, port):
        super().__init__(None)

        # set up the user interface for tagItem
        self.ui = Ui_tagItem()
        self.ui.setupUi(self)

        # store parent
        self.parent = parent

        # add widget to layout
        self.parent.connectedTagsScrollAreaWidgetLayout.insertWidget(0, self)
        
        # hide the recording label
        self.ui.recordingLabel.setVisible(False)

        # set Tag ID label
        self.tag_id = "-"
        # set Port label
        self.tag_port = port
        # set Rate label
        self.tag_msg_rate = "-"

        # set coordinates
        self.ui.xLabelValue.setText("-")
        self.ui.yLabelValue.setText("-")
        self.ui.zLabelValue.setText("-")

        # set estimated coordinates
        self.ui.xEstLabelValue.setText("-")
        self.ui.yEstLabelValue.setText("-")
        self.ui.zEstLabelValue.setText("-")
        self.ui.rollEstLabelValue.setText("-")
        self.ui.pitchEstLabelValue.setText("-")
        self.ui.yawEstLabelValue.setText("-")
        
    @property
    def is_tag_id_set(self):
        """
        Return True if the tag id is already set.
        Return False otherwise.
        """
        if self.tag_id == "-":
            return False

        return True
        
    @property
    def position(self):
        """
        Get tag position.
        """

        x = float(self.ui.xLabelValue.text())
        y = float(self.ui.yLabelValue.text())
        z = float(self.ui.zLabelValue.text())
        
        return x, y, z

    @position.setter
    def position(self, pos):
        """
        Set tag position.
        """

        # extract from tuple
        x, y, z = pos
        
        # set the format of the coordiantes
        # of Tag position
        x_str = format(x, '.3f')
        y_str = format(y, '.3f')
        z_str = format(z, '.3f')

        # set labels
        self.ui.xLabelValue.setText(x_str)
        self.ui.yLabelValue.setText(y_str)
        self.ui.zLabelValue.setText(z_str)


    @property
    def estimated_pose(self):
        """
        Get tag estimated pose.
        """

        x = float(self.ui.xEstLabelValue.text())
        y = float(self.ui.yEstLabelValue.text())
        z = float(self.ui.LEstlabelValue.text())

        roll = float(self.ui.rollEstLabelValue.text())
        pitch = float(self.ui.pitchEstLabelValue.text())
        yaw = float(self.ui.yawEstLabelValue.text())

        return x, y, z, roll, pitch, yaw

    @estimated_pose.setter
    def estimated_pose(self, pos):
        """
        Set tag estimated pose.
        """

        # extract from tuple
        x, y, z, roll, pitch, yaw = pos
        
        # set the format of the coordiantes
        # of Tag estimated position
        x_str = format(x, '.3f')
        y_str = format(y, '.3f')
        z_str = format(z, '.3f')

        # set the format of the coordiantes
        # of Tag estimated attitude
        roll_str = format(roll, '.3f')
        pitch_str = format(pitch, '.3f')
        yaw_str = format(yaw, '.3f')
        
        # set labels
        self.ui.xEstLabelValue.setText(x_str)
        self.ui.yEstLabelValue.setText(y_str)
        self.ui.zEstLabelValue.setText(z_str)
        self.ui.rollEstLabelValue.setText(roll_str)
        self.ui.pitchEstLabelValue.setText(pitch_str)
        self.ui.yawEstLabelValue.setText(yaw_str)
        
    @property
    def tag_id(self):
        """
        Return Tag ID.
        """
        tag_id_str = self.ui.tagIdLabelValue.text()

        # split string to recover the numeric ID
        str_split = tag_id_str.split(' ')

        # in case the tag_ID was not already set
        try:
            tag_ID = int(str_split[1])
        except ValueError:
            tag_ID = str_split[1]
            
        return tag_ID

    @tag_id.setter
    def tag_id(self, tag_id):
        """
        Set Tag ID.
        """

        tag_id_str = "Tag " + str(tag_id)
        
        self.ui.tagIdLabelValue.setText(tag_id_str)

    @property
    def tag_id_color(self):
        """
        Return tag label id color. (TODO)
        """
        
        pass

    @tag_id_color.setter
    def tag_id_color(self, color):
        """
        Set Tag ID label color.
        """

        # get rgb channel
        r = color[0]
        g = color[1]
        b = color[2]

        # set label color
        label = self.ui.tagIdLabelValue
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(r, g, b))
        label.setPalette(palette)
    
    @property
    def tag_port(self):
        """
        Return tag port.
        """
        
        return self.ui.portLabelValue.text()

    @tag_port.setter
    def tag_port(self, port):
        """
        Set Tag port.
        """

        self.ui.portLabelValue.setText(port)

    @property
    def tag_msg_rate(self):
        """
        Return Tag msg rate
        """

        #return self.ui.rateLabelValue.text()
        pass
        
    @tag_msg_rate.setter
    def tag_msg_rate(self, rate):
        """
        Set Tag msg rate
        """

        #self.ui.rateLabelValue.setText(rate)
        pass
        
    @property
    def is_record_active(self):
        return self.ui.recordCheckbox.isChecked()
        
    def remove_from_layout(self):
        """
        Remove widget from layout.
        """
        
        # remove widget and its child from the layout 
        self.parent.connectedTagsScrollAreaWidgetLayout.removeWidget(self)
        sip.delete(self)

    def set_recording_status(self, status):
        self.ui.recordingLabel.setVisible(status)

        
