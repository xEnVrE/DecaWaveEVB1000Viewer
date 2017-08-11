import struct

def decode_unsigned_int(string):
    """
    Return the unsigned int coded in the hex string.
    """
    return int(string,16)

def decode_float(string):
    """
    Return the float coded in the hex string.
    """
    hex_code = bytes.fromhex(string)
    unpacked = struct.unpack('>f', hex_code)
    return unpacked[0]

def decode_string(string):
    """
    Return the string as is.
    """
    return string

def select_decoder(type_name):
    """
    Return a different decoder depending on type_name.
    """
    if type_name == 'u':
        return decode_unsigned_int
    elif type_name == 'f':
        return decode_float
    elif type_name == 's':
        return decode_string

class DataFromEVB1000:
    """
    Decodes a line coming from the EVB1000 serial.
    """

    def __init__(self, line):
        
        # remove trailing '\r\n' from the line
        self.line = line[:-2]

        # empty msg_type
        self.msg_type = ''

    def decode_msg_type(self):
        """
        Determine the type of the message.

        Types implemented are

        tag_position_report   := msg_type = 'tpr', range_number,  
                                 (string),         (unsigned),    

                                 pos_x,   pos_y,   pos_z
                                 (float), (float), (float)

        anch_positions_report := TODO

        If the type is valid the field names of the message 
        and its structure are stored and the function return True.

        Otherwise return False.
        """

        # msg_type is always 3 characters long
        if len(self.line) < 3:
            return False

        # get msg_type
        msg_type = self.line[0:3]

        # set field names and structure depending on the msg_type
        if msg_type == 'tpr':
            self.msg_fields = ['msg_type', 'tag_id', 'x', 'y', 'z']
            self.msg_structure = ['s'] + ['u'] + ['f'] * 3
        else:
            return False

        return True

    def decode(self):
        """
        Return a dictionary containing the fields
        decoded from the message line.
        """

        # make a list of items from the line string
        items = self.line.split(' ')

        # empty list of decoded values
        decoded = []
        
        for index, item in enumerate(items):
            # extract type for the current item
            item_type_name = self.msg_structure[index]

            # pick the right decoder
            decoder = select_decoder(item_type_name)
            decoded.append(decoder(item))

        # return a dictionary
        return dict(zip(self.msg_fields, decoded))

if __name__ == '__main__':
    # some testing
    # tag position report with tag_id = 2, x = y = z = 10.34
    example_line = 'tpr 02 412570a4 412570a4 412570a4\r\n'

    # instantiate obj
    d = DataFromEVB1000(example_line)

    if (d.decode_msg_type()):
        print(d.decode())
    
