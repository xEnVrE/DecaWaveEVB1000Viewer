import numpy as np

class ColorPalette:
    """
    Color Palette class
    """
    def __init__(self):
        # define the Palette
        self.palette = [[1,116,196],
                        [85,164,218],
                        [2,112,62],
                        [236,68,34],
                        [240,151,66]]
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
    Color class 
    """
    def __init__(self, r, g, b):
        # Set RGB value of the color
        self._color = [r, g, b]

    @property
    def color(self):
        return self._color

    def get_color_shade(self, resolution = 1):
        """
        Return a list of colors sortered by 
        ascending order of the alpha channel  
        """
        if resolution == 1:
            alpha_channels = [1]
        else:
            alpha_channels =  np.linspace(0, 1, resolution)

        # generate the shade of the color
        color_shade = [self.color + [alpha] for alpha in alpha_channels]
        return color_shade
