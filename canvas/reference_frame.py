# numpy
import numpy as np

# lock
from threading import Lock

class ReferenceFrame:
    """
    Represents a reference frame obtained from the Matplotlib view frame
    rotated by an amount described by a rotation matrix and shifted by an 
    amount described by a translation vector.
    """
    
    def __init__(self, rotation, translation = [0, 0, 0], length = 1):
        """
        rotation: rotation matrix
        translation: tralnsation vector
        length: length of each axis of the reference frame, in meters
        """

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

        # set axes colors
        self.colors = {'x': 'r', 'y':'g', 'z':'b'}


        # empty dictionary of plots obtained returned by matplotlib
        self.axes_plot = dict()

    @property
    def rotation(self):
        # get the rotation matrix
        rotation = self._rotation
        
        return rotation

    @rotation.setter
    def rotation(self, rotation):
        # set the rotation matrixn
        self._rotation = rotation

    @property
    def translation(self):
        # get the translation vector
        translation = self._translation

        return translation 

    @translation.setter
    def translation(self, translation):
        # set the translation vector
        self._translation = translation

    def transform_axis(self, axis_name):
        """
        Perform rotrotranslation on an axis of the canonical base
        given the axis name.
        """

        # extract the axis depending on its name
        axis = [row[:] for row in self.canonical_base[axis_name]]
        
        # rotate the axis
        axis_rotated = self.rotation * axis

        # loop over the cartesian coordinates
        # and add the translation
        for i in range(3):
            axis_rotated[i] = axis_rotated[i] + self.translation[i]

        return axis_rotated
        
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

    def draw_axis(self, axes, axis_name, alpha, linewidth):
        """
        Draw an axis in axes given its name, alpha channel and linewidth.
        """
        # transform the axis using the current rotation and translation vector
        axis = self.transform_axis(axis_name)

        # draw axis
        line, = axes.plot(axis[0].A1, axis[1].A1, axis[2].A1,\
                                              color = self.colors[axis_name],\
                                              alpha=alpha,\
                                              linewidth = linewidth)

        self.axes_plot[axis_name] = line
        
    def update(self):
        """
        Update the reference frame.
        """

        # x axis (direction [1, 0, 0] expressed in Matplotlib frame)
        self.update_axis('x')
        
        # y axis (direction [0, 1, 0] expressed in Matplotlib frame)
        self.update_axis('y')
        
        # z axis (direction [0, 0, 1] expressed in Matplotlib frame)
        self.update_axis('z')

    def update_axis(self, axis_name):
        """
        Update the axis plot.
        """
        # transform the axis using the current rotation and translation vector
        axis = self.transform_axis(axis_name)
        
        # update internal matplolib representation
        self.axes_plot[axis_name].set_data(axis[0].A1, axis[1].A1)
        self.axes_plot[axis_name].set_3d_properties(axis[2].A1)

        # TODO:
        # is draw needed?
