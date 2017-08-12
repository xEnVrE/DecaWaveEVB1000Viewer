# QtDesigner generated classes
from plane_height_setter_ui import Ui_planeHeightSetter

# PyQt
from PyQt5.QtWidgets import QWidget, QMessageBox

def is_float(string):
    """
    Return true if the string s can be interpreted as a float.
    """
    
    try:
        float(string)
        return True
    except ValueError:
        return False


class PlaneHeightSetterItem(QWidget):
    """
    Qt Widget wrapping the UI of a PlaneHeightSetter.
    """
    
    def __init__(self, parent, mpl_canvas):
        super().__init__(None)

        # set up the user interface for planeHeightSetterItem
        self.ui = Ui_planeHeightSetter()
        self.ui.setupUi(self)

        # connect button
        self.ui.planeHeightSetButton.clicked.connect(self.planeHeightSetButton_on_click)
        
        # store canvas
        self.mpl_canvas = mpl_canvas

        # add widget to layout
        parent.planeHeightGroupBoxLayout.insertWidget(0, self)
        
    def error_msg_box(self, text):
        """
        Show an error message box with a desired text.
        """

        # instantiate message box
        msg = QMessageBox()

        # set icon of the message box
        msg.setIcon(QMessageBox.Critical)

        # set text of the message 
        msg.setWindowTitle("Error")
        msg.setText(text)

        # show message box
        msg.exec_()

    def disable(self):
        """
        Disable set button and text edit widget.
        """

        # disable the set button
        self.ui.planeHeightSetButton.setDisabled(True)

        # disable the text edit widget
        self.ui.planeHeightTextEdit.setDisabled(True)
        
    def planeHeightSetButton_on_click(self):
        """
        Set the height of the anchors plane.
        """

        # get the value from the text edit widget
        height = self.ui.planeHeightTextEdit.toPlainText()

        # check if the value is a valid float number
        if is_float(height):
            h = float(height)
            if h >= 0:
                self.mpl_canvas.anchors_plane_height = h
                return

        # print the error message
        self.error_msg_box("Plane height must be a positive number.")
