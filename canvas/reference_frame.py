# numpy
import numpy as np

# lock
from threading import Lock

class ReferenceFrame:
    """
    Represents a reference frame obtained from the Matplotlib view frame
    rotated by an amount described by a rotation matrix
    """
    
    def __init__(self, rotation, translation = [0, 0, 0], length = 1):

        # store the rotation matrix
        self._rotation = rotation

        # store translation vector
        self._translation = translation

        # resolution along axis
        resolution = 100

        # sample along axis
        segment = np.linspace(0, length, resolution)
        
        # save cononical base
        self.canonical_base = {'x': np.array([segment, np.zeros(resolution), np.zeros(resolution)]),
                               'y': np.array([np.zeros(resolution), segment, np.zeros(resolution)]),
                               'z': np.array([np.zeros(resolution), np.zeros(resolution), segment])}

        self.colors = {'x': 'r', 'y':'g', 'z':'b'}

        self.axes_plot = dict()

    @property
    def rotation(self):
        # get the rotation matrix
        rotation = self._rotation
        
        return rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation

    @property
    def translation(self):

        # get the translation vector
        translation = self._translation

        return translation 

    @translation.setter
    def translation(self, translation):
        self._translation = translation
        
    def draw(self, axes):
        """
        Draw the reference frame with three coloured axes.
        """
        # x axis (direction [1, 0, 0] expressed in Matplotlib frame)
        self.draw_axis(axes, 'x', 0.7, 1)
        
        # y axis (direction [0, 1, 0] expressed in Matplotlib frame)
        self.draw_axis(axes, 'y', 0.7, 1)
        
        # z axis (direction [0, 0, 1] expressed in Matplotlib frame)
        self.draw_axis(axes, 'z', 0.7, 1)

    def update(self):
        """
        Draw the reference frame with three coloured axes.
        """
        # x axis (direction [1, 0, 0] expressed in Matplotlib frame)
        self.update_axis('x')
        
        # y axis (direction [0, 1, 0] expressed in Matplotlib frame)
        self.update_axis('y')
        
        # z axis (direction [0, 0, 1] expressed in Matplotlib frame)
        self.update_axis('z')

        
    def homogeneus_transformation(self, axis_name):
        """
        Evaluate the homogeneus transformation
        """
        axis =  self.canonical_base[axis_name]        
        
        for i in range(3):
            axis[i] = axis[i] + self.translation[i]

        axis = self.rotation * self.canonical_base[axis_name]

        return axis
        
    def draw_axis(self, axes, axis_name, alpha, linewidth):
        """
        Draw an axis in axes given its name, alpha channel and linewidth.

        Colour is decided depending on the axis name using the standard convention:
        -x axis: red
        -y axis: green
        -z axis: blue
        """
        
        axis = self.homogeneus_transformation(axis_name)

        # draw axis
        self.axes_plot[axis_name] = axes.plot(axis[0].A1, axis[1].A1, axis[2].A1,\
                                              color = self.colors[axis_name], alpha=alpha,
                                              linewidth = linewidth)

    def update_axis(self, axis_name):
        """
        update the axis in axes given its name, alpha channel and linewidth.

        Colour is decided depending on the axis name using the standard convention:
        -x axis: red
        -y axis: green
        -z axis: blue
        """
        
        axis = self.homogeneus_transformation(axis_name)
        
        # draw axis
        self.axes_plot[axis_name].set_data(axis[0].A1, axis[1].A1)
        self.axes_plot[axis_name].set_3d_properties(axis[2].A1)

        # is draw needed?
