# numpy
import numpy as np

# PyQt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# matplotilb
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# representation of tag position as a scatter
from tag_position_view import TagPositionView

# circle buffer
from circle import Circle

# lock
from threading import Lock

class MatplotlibViewerCanvas(FigureCanvas):
    """
    Main view containing anchors, reference frame of anchor 0
    and the estimated position of the tag(s).

    Inherits from FigureCanvasQTAgg in order to integrate with PyQt.
    """
    def __init__(self, parent, frame_rate, tag_buffer_size):
        
        # create a new figure
        fig = Figure(dpi = 100)
        fig.subplots_adjust(left=-0.1, right=1.1, bottom=-0.2, top=1.3)
        
        # call FigureCanvas constructor
        FigureCanvas.__init__(self, fig)

        # set the parent of this FigureCanvas
        self.setParent(parent)

        # empty list of anchors positions
        self.anchors = []

        # empty list of anchors colors
        self.anchor_colors = []

        # empty dictionary of TagPositionView scatters
        self.tags_position_view = dict()

        # common height of anchors 0, 1 and 2
        self._anchors_plane_height = 0
        self.anchors_plane_height_lock = Lock()
        
        # save requested frame rate for animation
        self.frame_rate = frame_rate

        # save requested size of TagPositionsBuffer buffers
        self.tag_buffer_size = tag_buffer_size

        # setup the plot
        self.setup_plot(fig)

        # Circle class producing fake data for testing
        self.circle = Circle(radius = 1,\
                             size = 50,\
                             time_step = 1.0 / self.frame_rate,\
                             freq = 1,\
                             z = 0.5)

    @property
    def anchors_plane_height(self):

        # get the anchors plane height 
        self.anchors_plane_height_lock.acquire()

        height = self._anchors_plane_height

        self.anchors_plane_height_lock.release()
        
        return height 

    @anchors_plane_height.setter
    def anchors_plane_height(self, height):

        self.anchors_plane_height_lock.acquire()

        self._anchors_plane_height = height

        self.anchors_plane_height_lock.release()
        
    def setup_plot(self, figure):
        """
        Setup the main plot of the figure.
        """

        # add plot to the figure
        self.axes = figure.add_subplot(111, projection = '3d')
        
        # set labels
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")
        self.axes.set_zlabel("Z")

        # disable drawing of grid
        self.axes.axis('off')

        # start tags position animation
        time_step = 1.0 / self.frame_rate * 1000
        self.anim = animation.FuncAnimation(figure, self.update_tags_position_view, interval = time_step)

    def update_tags_position_view(self, frame_number):
        """
        Update each tag position view in self.tags_position_view
        """
        # update each tag position view in self.tags_position_view
        for view_name in self.tags_position_view:
            self.tags_position_view[view_name].update_view()

    def set_axes_limits(self):
        """
        Set axes limits.
        """
        self.axes.set_xlim(self.x_y_min_value, self.x_y_max_value)
        self.axes.set_ylim(self.x_y_min_value, self.x_y_max_value)
        self.axes.set_zlim(self.z_min_value, self.z_max_value)

    def eval_figure_limits(self):
        """
        Evaluate figure limits using the position of the anchors.
        """

        # put all the x and y coordinates of anchors in a list
        x_y_list = [anch.item(i) for anch in self.anchors for i in range(2)]

        # eval max and min for x and y axes and add some tolerance
        tolerance_x_y = 0.5
        self.x_y_min_value = min(x_y_list) - tolerance_x_y
        self.x_y_max_value = max(x_y_list) + tolerance_x_y

        # set minimum z value to z with some negative tolerance
        # because some estimate of the tag z position may be negative
        tolerance_z = 1
        self.z_min_value = 0 - tolerance_z / 2.0 
        # set maximum z value to the z coordinate of the fourth anchor
        # which is known to be the taller
        self.z_max_value = self.anchors[3].item(2) + tolerance_z * 3.0 / 4.0

    def set_anchor_position(self, anchors_position):
        """
        Save position of each anchor as an array of numpy column vector.


        Anchors_position are expressed in "data" frame and are saved
        in self.anchors after an homogeneous transformation
        (see vector_hom_transformation()).
        """
        
        for anchor_position in anchors_position:
            # create numpy column vector
            np_anchor = np.transpose(np.array([anchor_position]))

            # perform homogeneous transformation
            np_anchor_transformed = self.vector_hom_transformation(np_anchor)

            # append to list
            self.anchors.append(np_anchor_transformed)


            
    def set_new_tag(self, tag_ID, tag_color):
        """
        Register a new tag given its ID and its representing color
        """
        
        # instantiate a new TagPositionView
        self.tags_position_view[tag_ID] = TagPositionView(self.axes,\
                                                          self.tag_buffer_size,\
                                                          tag_color)        
    def is_tag_view(self, tag_ID):
        """
        Return True if the a TagPositionView for tag <tag_ID> already exists.
        Return False otherwise.
        """

        return tag_ID in self.tags_position_view
        
    def get_tag_color(self, tag_ID):
        """
        Return the color used in the plot for a specific Tag
        """

        return self.tags_position_view[tag_ID].color

    def set_anchor_colors(self, colors):
        """
        Save the color of each anchor as a list.
        """
        
        anchor_colors = colors

    
    def set_tag_position(self, tag_ID, x, y, z):
        """
        Inform the tag position view of the tag <tag_ID> that a new position [x, y, z]
        is available.
        """

        # perform homogeneous transformation on data
        position_data_frame = np.array([[x,y,z]]).T
        position_mpl_frame = self.vector_hom_transformation(position_data_frame)

        # extract coordinates
        x = position_mpl_frame.item(0)
        y = position_mpl_frame.item(1)
        z = position_mpl_frame.item(2)

        # set new position
        self.tags_position_view[tag_ID].new_position(x, y, z)

    def eval_basis_change(self, a3_z):
        """
        Evaluate change of basis between the "data" frame, in which
        data coming from the tag are expressed, and the frame
        used in the Matplotlib view.

        Depending upon the position of the anchors, data coming from the tag
        may be expressed in a "data" frame that is obtained with a rotation of -180
        degrees about a common y-axis with respect to the frame used in the
        Matplotlib view. In order to understand whether the rotation is required
        or not the sign of the z coordinate of the fourth anchor (a3), expressed
        in "data" frame, must be checked.
        """
        
        rot_angle = 0

        if a3_z  < 0:
            rot_angle = -np.pi
        
        self.basis_change = np.matrix([[np.cos(rot_angle), 0, np.sin(rot_angle)],
                                       [0, 1, 0],
                                       [-np.sin(rot_angle), 0, np.cos(rot_angle)]])

    def vector_hom_transformation(self, vector):
        """
        Perform an homogeneous transformation on a numpy column vector expressed
        in the "data" frame.

        The change of basis of the transformation is given by self.basis_change.
        The shift of the transformation is given by [0, 0, self.anchors_plane_height]'.
        This way a vector expressed in "data" frame is expressed in Matplotlib frame
        and with respect to a new origin placed on the ground plane.

        Return the components of the new vector as a np vector.
        """

        # perform transformation
        shift = np.transpose(np.array([[0, 0, self.anchors_plane_height]]))
        vector = self.basis_change * vector + shift

        return vector

    def draw_static_objects(self):               
        """ 
        Draw static objects in the Matplotlib view.

        Static objects are:
        - a cylinder for each anchor
        - three axes representing the "data" reference frame
        - ground plane
        """
        self.draw_anchors()
        self.draw_data_frame_axes()
        self.draw_ground()

        # TODO: remove me!
        #        plt.show()
            
    def draw_data_frame_axes(self):
        """ 
        Draw three axes representing the "data" reference frame.
        """
        # here self.basis_change is seen as a Rotation instead of
        # a basis
        #
        # ReferenceFrame(rotation) representes three axes corresponding to
        # the axes of the Matplotlib view rotated by an amount described by 'rotation'
        reference_frame = ReferenceFrame(self.basis_change)

        # draw axes
        reference_frame.draw(self.axes)

    def draw_anchors(self):
        """
        Draw each anchor as a cylinder.
        """
        for i in range(4):

            # instantiate Anchor
            x = self.anchors[i].item(0)
            y = self.anchors[i].item(1)
            z = self.anchors[i].item(2)

            color = anchor_colors[i]
            
            cylinder_radius = 0.05
            anchor_plot = Anchor(x, y, z, cylinder_radius, color)

            # draw the cylinder represeting the anchor
            anchor_plot.draw(self.axes)
                
    def draw_ground(self):
        """ 
        Draw the ground plane
        """

        # ground plane is created taking into account
        # the limits of the figure
        plane = Plane(self.x_y_min_value, self.x_y_max_value)

        # draw ground plane
        plane.draw(self.axes)
        
class Anchor:
    """
    Represents an anchor as a cylinder.
    """
    def __init__(self, center_x, center_y, height, radius, color):

        # sample along diameter of the cylinder
        x_linspace = np.linspace(-radius, radius, 100)

        # sample along the axis of the cylinder
        z_linspace = np.linspace(0, height, 100)

        # perform a cartesian product between samples
        self.x, self.z = np.meshgrid(x_linspace, z_linspace)

        # for each x coordinate eval the y coordinate
        # using the *function* of the semicircle
        # y = f(x) = sqrt(r^2 - x^2)
        y = np.sqrt(radius**2 - (self.x)**2)

        # shift points by (center_x, center_y)
        self.x = self.x + center_x
        self.y_pos = y + center_y
        # this take into account the other "half"
        # of the surface of the cylinder
        self.y_neg = -y + center_y

        # save color used in plot representation
        self.color = color

    def draw(self, axes):
        """
        Draw a cylinder on the given axes.
        """
        # sampling related stuff
        rstride = 20
        cstride = 10

        c = self.color.color
        
        # draw one half of the cylinder
        axes.plot_surface(self.x, self.y_pos, self.z, color = c,\
                          alpha=0.5, rstride=rstride, cstride=cstride)
        # draw the other half of the cylinder
        axes.plot_surface(self.x, self.y_neg, self.z, color = c,\
                          alpha=0.5, rstride=rstride, cstride=cstride)
        
class ReferenceFrame:
    """
    Represents a reference frame obtained from the Matplotlib view frame
    rotated by an amount described by a rotation matrix
    """
    
    def __init__(self, rotation):

        # store the rotation matrix
        self.rotation = rotation
        
    def draw(self, axes):
        """
        Draw the reference frame with three coloured axes.
        """
        # x axis (direction [1, 0, 0] expressed in Matplotlib frame)
        self.draw_axis( axes, 'x', 0.7, 1)
        
        # y axis (direction [0, 1, 0] expressed in Matplotlib frame)
        self.draw_axis( axes, 'y', 0.7, 1)
        
        # z axis (direction [0, 0, 1] expressed in Matplotlib frame)
        self.draw_axis( axes, 'z', 0.7, 1)

    def draw_axis(self, axes, axis_name, alpha, linewidth):
        """
        Draw an axis in axes given its name, alpha channel and linewidth.

        Colour is decided depending on the axis name using the standard convention:
        -x axis: red
        -y axis: green
        -z axis: blue
        """
        # resolution along axis
        resolution = 100

        # sample along axis
        segment = np.linspace(0, 1, resolution)

        # generate points along axis_name axis
        if axis_name == 'x':
            axis = np.array([segment, np.zeros(resolution), np.zeros(resolution)])
            color = 'r'
        elif axis_name == 'y':
            axis = np.array([np.zeros(resolution), segment, np.zeros(resolution)])
            color = 'g'
        elif axis_name == 'z':
            axis = np.array([np.zeros(resolution), np.zeros(resolution), segment])
            color = 'b'

        # rotate axis
        axis = self.rotation * axis

        # draw axis
        axes.plot(axis[0].A1, axis[1].A1, axis[2].A1,\
                  color = color, alpha=alpha, linewidth = linewidth)
        
class Plane:
    """
    Represents a square plane were the anchor are fixed. 
    """
    def __init__(self, limit_min, limit_max):

        # sample along a grid
        ls = np.linspace(limit_min, limit_max, 100)
        self.x, self.y = np.meshgrid(ls, ls)

        # indeed it is a *ground* plane
        self.z = 0 * self.x
                
    def draw(self, axes):
        """
        Draw the plane in axes.
        """

        # sampling related stuff
        rstride = 20
        cstride = 10

        # draw the plane
        axes.plot_surface(self.x, self.y, self.z,\
                          color = '#19781E',  alpha=0.2, rstride=rstride, cstride=cstride)
if __name__ == '__main__':
    # do some testing
    vc = ViewerCanvas()
    vc.eval_basis_change(1)
    vc.anchors_plane_height = 1
    vc.set_anchor_position([[0,0,0],[0,1,0],[2, -1, 0],[1, 2, 1]])
    vc.draw_static_objects()
