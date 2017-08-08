import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# neded for static canvas (example)
from numpy import arange, sin, pi

from PyQt5 import QtWidgets

from evb1000viewer import Ui_MainWindow
from tag_item_ui import Ui_tagItem

class MplCanvas(FigureCanvas):
    """Menage MatPlotLib figure in PyQt canvas"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # instantiate Figure object
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_figure()
        FigureCanvas.__init__(self, fig)

        #add parent
        self.setParent(parent)

        # set size
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    #def compute_figure(self):
    #   pass


class StaticMplCanvas(MplCanvas):
    """Simple canvas with a sine plot."""

    def compute_figure(self):
        """
        Plot a sine function
        """
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        
class MainWindow(QtWidgets.QMainWindow):
    """ MainWindow class """
    def __init__(self):
        super().__init__()

        # Set up the user interface from MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect action buttons
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionQuit.triggered.connect(self.quit)

        # dictionary of the widgets that reppresent each Tag
        self.tags_widgets = dict()

    def add_canvas(self):
        """Simple example""" 
        sc = StaticMplCanvas(self.ui.matPlotGroupBox, width=5, height=4, dpi=100)
        self.ui.matPlotGroupBoxLayout.addWidget(sc)

    def add_widget_tag(self, key, tag_id, port):
        """
        add widget to the layout

        allow to add information about a Tag (tag_id and serial port).
        """
        # set default value to the widget
        tag_item = tagItem()
        tag_item.ui.tagIdLabelValue.setText(tag_id)
        tag_item.ui.portLabelValue.setText(port)
        tag_item.ui.frequencyLabelValue.setText('-')

        # add the widget to the dictionary
        self.tags_widgets[key] = tag_item

        # add the widget to the layout
        self.ui.connectedTagsScrollAreaWidgetLayout.insertWidget(0, tag_item)

    def remove_widget_tag(self, key):
        """
        remove Tag widget from the layout
        
        allow to remove a widget. Key of the widget, the same used in add_widget_tag method,
        id needed.
        """
        import sip
        widget = self.tags_widgets[key]

        # remove widget from layout 
        self.ui.connectedTagsScrollAreaWidgetLayout.removeWidget(widget)
        sip.delete(widget)

        # remove elements from dictionary
        del self.tags_widgets[key]
        widget = None
        
    def about(self):
        """
        About method

        Method called when actionAbout is triggered
        """
        QtWidgets.QMessageBox.about(self, "About",
                                    """ TODO """)

    def quit(self):
        """
        Quit method

        Method called when actionQuit is triggered
        """
        self.close()

class tagItem(QtWidgets.QWidget):
    """ tagItem class """
    def __init__(self, parent = None):
        super().__init__(parent)

        # Set up the user interface for tagItem
        self.ui = Ui_tagItem()
        self.ui.setupUi(self)

        
# construct a QApplication
app = QtWidgets.QApplication(sys.argv)

# instantiate the main window and add canvas 
gui = MainWindow()
gui.add_canvas()

# add two tags (only for example)
gui.add_widget_tag("TAG0", "Tag 0", "COM3")
gui.add_widget_tag("TAG1", "Tag 1", "COM2")

# show the main window
gui.show()

sys.exit(app.exec_())
