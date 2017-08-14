# QtDesigner generated classes
from anchor_item_ui import Ui_anchItem

# PyQt
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtGui import QColor, QPalette

class AnchItem(QGroupBox):
    """
    Qt Widget wrapping the UI of a Anch item.
    """
    
    def __init__(self, parent, anchor_index, coordinates):
        super().__init__(None)

        # set up the user interface for anchItem
        self.ui = Ui_anchItem()
        self.ui.setupUi(self)

        # store parent
        self.parent = parent

        # add widget to layout
        self.parent.anchorsScrollAreaWidgetLayout.addWidget(self)

        # set GroupoBox title
        title = "Anchor " + str(anchor_index)
        self.setTitle(title)
        
        x, y, z = coordinates 

        # set the format of the coordiantes
        # of Anch position
        x_str = format(x, '.3f')
        y_str = format(y, '.3f')
        z_str = format(z, '.3f')

        # set labels
        self.ui.xLabelValue.setText(x_str)
        self.ui.yLabelValue.setText(y_str)
        self.ui.zLabelValue.setText(z_str)


    @property
    def color(self):
        """
        Return anch title color. (TODO)
        """
        
        pass

    @color.setter
    def color(self, color):
        """
        Set Anchor groupbox title color.
        """

        # get rgb channel
        r, g, b = color

        # set Title color
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(r, g, b))
        self.setPalette(palette)
        self.setStyleSheet('QGroupBox {color:rgb(r,g,b);}')
