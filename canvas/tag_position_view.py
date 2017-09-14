# mutex
from threading import Lock

# numpy
import numpy as np

# reference frame
from canvas.reference_frame import ReferenceFrame

class TagPositionAttitudeView:
    """
    Represents the tag position and attitude as a Matplotlib plotter object
    """
    def __init__(self, axes, color):

        # save axes
        self.axes = axes
        
        #instantiate the reference frame
        self.offset_rotation = rot_z(np.pi / 2) * rot_y(np.pi) 
        self.reference_frame = ReferenceFrame(self.offset_rotation, length = 0.1)
        self.reference_frame.draw(self.axes)

        self.position = [0, 0, 0]
        self.attitude = [0, 0, 0]

    def rot_x(self, theta):
        """
        Rotation matrix Rx(theta)
        """
        
        matrix = np.matrix([[1, 0, 0],
                            [0, np.cos(rot_angle), -np.sin(rot_angle)],
                            [0, np.sin(rot_angle), np.cos(rot_angle)]])

        return matrix


        
    def rot_y(self, rot_angle):
        """
        Rotation matrix Ry(theta)
        """
        
        matrix = np.matrix([[np.cos(rot_angle), 0, np.sin(rot_angle)],
                            [0, 1, 0],
                            [-np.sin(rot_angle), 0, np.cos(rot_angle)]])

        return matrix
        
    def rot_z(self, theta):
        """
        Rotation matrix Rz(theta)
        """
        
        matrix = np.matrix([[np.cos(rot_angle), -np.sin(rot_angle), 0],
                            [np.sin(rot_angle), np.cos(rot_angle), 0],
                            [0, 0, 1]])

        return matrix

        
    def rotation_matrix(self):
        """
        Return the rotation matrix
        """
        roll = self.roll
        pitch = self.pitch
        yaw = self.yaw

        # evaluate the RPY matrix
        matrix_rpy = rot_z(yaw) * rot_y(pitch) * rot_x(roll)

        matrix = self.offset_rotation * matrix_rpy
        return matrix

    def new_position(self, x, y, z, roll, pitch, yaw):
        """
        Add a new tag pose (cartesian position and attitude) 
        """
        self.position = [x, y, z]
        self.attitude = [roll, pitch, yaw]
    
    def update_view(self):
        """
        Update the reference frame with current data.
        """
        self.reference_frame.translation = self.position
        self.reference_frame.rotation = self.rotation_matrix()
        self.reference_frame.update()
        
class TagPositionView:
    """
    Represents the tag position as a Matplotlib scatter object
    """

    def __init__(self, axes, buffer_size, color):

        # instantiate a scatter with no data
        self.scatter = axes.scatter(np.zeros(0),\
                                    np.zeros(0),\
                                    np.zeros(0),\
                                    depthshade = 0)

        # instantiate a TagPositionsBuffer
        self._buffer = TagPositionsBuffer(buffer_size)

        self.color = color
        
        
    @property
    def buffer(self):
        return self._buffer

    def new_position(self, x, y, z):
        """
        Add a new tag position to the underlying tag positions buffer.
        """
        self.buffer.add_position(x, y, z)

    def update_view(self):
        """
        Update the scatter with current data.
        """

        # extract new data
        x, y, z = self.buffer.get_positions()

        # extract the number of elements in the buffer
        number_of_elements = self.buffer.get_number_of_elements()

        color_shade = self.color.get_color_shade(number_of_elements)

        # set new data
        self.scatter._offsets3d = (x, y, z)
        self.scatter._edgecolor3d = color_shade
        self.scatter._facecolor3d = color_shade
        
class TagPositionsBuffer:
    """
    Storage for a fixed number of tag cartesian positions.
    """

    def __init__(self, size):

        self.size = size
        
        # instantiate an empty numpy array for each cartesian axis
        self.data_x = np.zeros(0)
        self.data_y = np.zeros(0)
        self.data_z = np.zeros(0)

        # data mutex
        self.data_lock = Lock()

    def get_positions(self):
        """
        Return the tag positions stored in the buffer.
        """
        
        self.data_lock.acquire()

        data_x_copy = np.copy(self.data_x)
        data_y_copy = np.copy(self.data_y)
        data_z_copy = np.copy(self.data_z)

        self.data_lock.release()

        return data_x_copy, data_y_copy, data_z_copy

    def get_number_of_elements(self):
        """
        Return the number of elements in the buffer
        """
        self.data_lock.acquire()

        number_of_elements = self.data_x.size

        self.data_lock.release()

        return number_of_elements
    
    def add_position(self, x, y, z):
        """
        Add a new tag position to the buffer.
        
        If the buffer is not filled yet the new position is appended.
        Otherwise the buffer is left-shifted and the new position 
        is inserted in the last field.
        """

        self.data_lock.acquire()

        # append if not filled yet
        if self.data_x.size < self.size:
            self.data_x = np.append(self.data_x, x)
            self.data_y = np.append(self.data_y, y)
            self.data_z = np.append(self.data_z, z)
        else:
            # left shift
            for i in range(self.size-1):
                self.data_x[i] = self.data_x[i+1]
                self.data_y[i] = self.data_y[i+1]
                self.data_z[i] = self.data_z[i+1]

            # insert in the last field
            self.data_x[self.size-1] = x
            self.data_y[self.size-1] = y
            self.data_z[self.size-1] = z

        self.data_lock.release()
