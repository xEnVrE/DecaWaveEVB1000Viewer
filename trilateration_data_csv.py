import csv
class TrilaterationData:
    """
    Get trilateration data from a csv file and return the set 
    of coordinates.
    """
    
    def __init__(self, file_name):
        # list of tags coordinates
        self.tag_positions = []

        # open the csv file
        with open(file_name, 'r') as csvfile:

            tag_coord = []

            # read the csv file
            file_ = csv.reader(csvfile, delimiter=',')
            for row in file_:
                for value in row:
                    # save each coordinate
                    tag_coord.append(float(value))

                # populate the Tag position list with the coordinates
                self.tag_positions.append(tag_coord)
                tag_coords = []

            # close the csv file
            csvfile.close()

        self.data_index = 0
        
    def get_new_value(self):
        """
        Get a new set of coordinates.
        
        Returns a list [x, y, z]
        """

        # take the coordinates
        coords = self.tag_positions[self.data_index]

        # update the index
        self.data_index += 1
        self.data_index % len(self.tag_positions)

        return coords
