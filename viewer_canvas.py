import numpy as np

# TODO: remove me when using FigureCanvasQTAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ViewerCanvas:
    """
    Main view containing anchors, reference frame of anchor 0
    and the estimated position of the tag(s).

    Inherits from FigureCanvasQTAgg in order to integrate with PyQt.
    """
    def __init__(self):
        # TODO change with figure from inherited class FigureCanvas
        self.fig = plt.figure()

        # set main axes
        self.axes = self.fig.add_subplot(111, projection='3d')

        # set labels
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")
        self.axes.set_zlabel("Z")

        # empty list of anchors positions
        self.anchors = []

        # common height of anchors 0, 1 and 2
        self._anchors_plane_height = 0


    @property
    def anchors_plane_height(self):
        return self._anchors_plane_height

    @anchors_plane_height.setter
    def anchors_plane_height(self, height):
        self._anchors_plane_height = height

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
        plt.show()
            
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
        for anch in self.anchors:

            # instantiate Anchor
            x = anch.item(0)
            y = anch.item(1)
            z = anch.item(2)

            cylinder_radius = 0.05
            anchor_plot = Anchor(x, y, z, cylinder_radius)

            # draw the cylinder represeting the anchor
            anchor_plot.draw(self.axes)
                
    def draw_ground(self):
        """ 
        Draw the ground plane
        """

        # ground plane is evaluated taking into account
        # the position of the anchors
        plane = Plane(self.anchors)

        # draw ground plane
        plane.draw(self.axes)
        
class Anchor:
    """
    Represents an anchor as a cylinder.
    """
    def __init__(self, center_x, center_y, height, radius):

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

    def draw(self, axes):
        """
        Draw a cylinder on the given axes.
        """
        # sampling related stuff
        rstride = 20
        cstride = 10

        # draw one half of the cylinder
        axes.plot_surface(self.x, self.y_pos, self.z,color = '#42A9FF',\
                          alpha=0.5, rstride=rstride, cstride=cstride)
        # draw the other half of the cylinder
        axes.plot_surface(self.x, self.y_neg, self.z,color = '#42A9FF',\
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
    Represents the plane were the anchor are fixed. 
    """
    def __init__(self, anchors_position):

        # put all the x and y coordinates of anchors in a list
        list = [anch.item(i) for anch in anchors_position for i in range(2)]

        # eval max and min and add some tolerance
        max_value = max(list) + 0.5
        min_value = min(list) - 0.5

        # sample along a grid
        ls = np.linspace(min_value, max_value, 100)
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

boh = ViewerCanvas()
boh.eval_basis_change(1)
boh.anchors_plane_height = 1
boh.set_anchor_position([[0,0,0],[0,1,0],[2, -1, 0],[1, 2, 1]])
boh.draw_static_objects()
