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
        self.rotation = rotation
        self.rotation_lock = Lock()
        
        # store translation vector
        self.translation = translation
        self.translation_lock = Lock()

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
    def rotation(self, rotation):
        
        # get the rotation matrix
        self.rotation_lock.acquire()

        rotation = self.rotation

        self.rotation_lock.release()
        
        return rotation

    @rotation.setter
    def rotation(self, rotation):

        self.rotation_lock.acquire()

        self.rotation = rotation

        self.rotation_lock.release()

    @property
    def translation(self):

        # get the translation vector
        self.translation_lock.acquire()

        translation = self.translation

        self.translation_lock.release()
        
        return translation 

    @translation.setter
    def translation(self, translation):

        self.translation_lock.acquire()

        self.translation = translation

        self.translation_lock.release()

        
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
        axis =  self.axis[axis_name]        
        
        # translate the axis
        self.translation_lock.acquire()

        for i in range(3):
            axis[i] = axis[i] + self.translation[i]

        self.translation_lock.release()

        # rotate axis
        self.rotation_lock.acquire()

        axis = self.rotation * self.axis[axis_name]

        self.rotation_lock.release()

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
                                              color = self.color[axis_name], alpha=alpha,
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
