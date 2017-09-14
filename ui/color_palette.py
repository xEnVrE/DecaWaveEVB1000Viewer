import numpy as np

class ColorPalette:
    """
    Color palette class.
    """
    
    def __init__(self, palette_name = "Matlab"):
        
        # define the Palette
        if palette_name == "Matlab":
            palette = [[0, 113.9850, 188.9550],
                       [216.7500, 82.8750, 24.9900],
                       [236.8950, 176.9700, 31.8750],
                       [125.9700, 46.9200, 141.7800],
                       [118.8300, 171.8700, 47.9400],
                       [76.7550, 189.9750, 237.9150],
                       [161.9250, 19.8900, 46.9200]]

        elif palette_name == "Google":
            palette = [[2,112,62],
                       [1,116,196],
                       [85,164,218],
                       [236,68,34],
                       [240,151,66]]

        self.palette = [[channel / 256  for channel in color] for color in palette]
        
        self.index = 0

    def get_new_color(self):
        """
        Return a new color
        """
        rgb = self.palette[self.index]
        color = Color(*rgb)

        # update the index
        self.index += 1
        self.index %= len(self.palette)

        return color

class Color:
    """
    Color class.
    """
    
    def __init__(self, r, g, b):
        
        # Set RGB value of the color
        self._color = [r, g, b]

    @property
    def color(self):
        return self._color

    @property
    def color_255(self):
        """
        Return the color with channels bewteen 0 and 255.
        """
        c = [channel * 255 for channel in self._color]
        return c

    def get_color_shade(self, resolution = 1):
        """
        Return a list of colors sorted by ascending alpha channel.
        """
        if resolution == 1:
            alpha_channels = [1]
        else:
            alpha_channels =  np.linspace(0, 1, resolution)

        # generate the shade of the color
        color_shade = [self.color + [alpha] for alpha in alpha_channels]
        
        return color_shade
