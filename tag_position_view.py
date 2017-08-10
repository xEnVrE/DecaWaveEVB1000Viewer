# mutex
from threading import Lock

# numpy
import numpy as np

class TagPositionView:
    """
    Represents the tag position as a Matplotlib scatter object
    """

    def __init__(self, axes, buffer_size):#, color):

        # instantiate a scatter with no data
        self.scatter = axes.scatter(np.zeros(0),\
                                    np.zeros(0),\
                                    np.zeros(0))

        # instantiate a TagPositionsBuffer
        self._buffer = TagPositionsBuffer(buffer_size)

        #TODO: handle scatter colors

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

        # set new data
        self.scatter._offsets3d = (x, y, z)

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
