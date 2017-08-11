# QtDesigner generated classes
from tag_item_ui import Ui_tagItem

# PyQt
from PyQt5.QtWidgets import QFrame

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
        
        # set Tag ID label
        self.tag_id = "-"
        # set Port label
        self.tag_port = port
        # set Rate label
        self.tag_msg_rate = "-"

        #
        

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

    @position.setter
    def position(self, pos):
                
    @property
    def tag_id(self):
        """
        Return Tag ID.
        """
        tag_id_str = self.ui.tagIdLabelValue.text()

        # split string to recover the numeric ID
        str_split = tag_id_str.split(' ')
        tag_ID = int(str_split[1])
        
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
        Set Tag ID label color. (TODO)
        """
        
        r = color[0]
        g = color[1]
        b = color[2]
        pass
    
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
        
        return self.ui.rateLabelValue.text()

    @tag_msg_rate.setter
    def tag_msg_rate(self, rate):
        """
        Set Tag msg rate
        """

        self.ui.rateLabelValue.setText(rate)

    def remove_from_layout(self):
        """
        Remove widget from layout.
        """
        
        # remove widget and its child from the layout 
        self.parent.connectedTagsScrollAreaWidgetLayout.removeWidget(self)
        sip.delete(self)
