from tag_item_ui import Ui_tagItem

from PyQt5.QtWidgets import QFrame

class TagItem(QFrame):
    """
    Qt Widget wrapping the UI of a Tag item.
    """
    
    def __init__(self, parent, port):
        super().__init__(None)

        # Set up the user interface for tagItem
        self.ui = Ui_tagItem()
        self.ui.setupUi(self)

        # add widget to layout
        parent.connectedTagsScrollAreaWidgetLayout.insertWidget(0, self)
        
        # set Tag ID label
        self.tag_id = "-"
        # set Port label
        self.tag_port = port
        # set Rate label
        self.tag_msg_rate = "-"
        
    @property
    def tag_id(self):
        """
        Return Tag ID.
        """
        
        return self.ui.tagIdLabelValue.text

    @tag_id.setter
    def tag_id(self, tag_id):
        """
        Set Tag ID.
        """
        
        self.ui.tagIdLabelValue.setText(tag_id)

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
        
        return self.ui.portLabelValue.text

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
        
        return self.ui.rateLabelValue.text

    @tag_msg_rate.setter
    def tag_msg_rate(self, rate):
        """
        Set Tag msg rate
        """

        self.ui.rateLabelValue.setText(rate)
