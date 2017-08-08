import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# neded for static canvas (example)
from numpy import arange, sin, pi

from PyQt5 import QtWidgets

from evb1000viewer import Ui_MainWindow

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
        
    def add_canvas(self):
        """Simple example""" 
        sc = StaticMplCanvas(self.ui.matPlotGroupBox, width=5, height=4, dpi=100)
        self.ui.matPlotGroupBoxLayout.addWidget(sc)

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

# construct a QApplication
app = QtWidgets.QApplication(sys.argv)

# instantiate the main window and add canvas 
gui = MainWindow()
gui.add_canvas()

# show the main window
gui.show()

sys.exit(app.exec_())
