import csv
import time

# EVB1000 decoder
from decoder import DataFromEVB1000

class CSVLogger:
    """
    Save data from the EVB1000 serial to a csv file.
    """

    def __init__(self):

        # uninitialized file descriptor
        self._file = None

        # uninitialized writer
        self.writer = None

        # set state to disabled
        self._enabled = False

    @property
    def enabled(self):
        return self._enabled

    @enable.property
    def enabled(self, state):
        self._enabled = state
        
    def log_data(self, evb1000_data):
        """
        Log new line from EVB1000 serial line.
        """

        # log only if the logger is enabled
        if not self.enabled:
            return

        # extract data
        data = evb1000_data.decoded

        # open file descriptor in case it is closed
        #
        # file is opened in append mode so that
        # a newly connected tag with the same id
        # logs in the same file
        if self._file == None:
            filename = "tag_" + str(data['tag_id']) + "_" +\
                       time.strftime("%d_%m_%Y")
            self._file = open(self.filename + '.csv', 'a')

            # write header
            self.writer = csv.DictWriter(self._file, evb1000_data.msg_fields)
            self.writer.writeheader()
        
        # write new data
        self.writer.writerow(evb1000_data.decoded)

    def close(self):
        """
        Close the file descriptor.
        """
        self._file.close()

