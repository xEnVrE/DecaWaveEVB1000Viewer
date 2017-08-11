# sine and cosine
import math

class Circle:
    def __init__(self, radius, size, time_step, freq, z):
        self.radius = radius
        self.size = size
        self.time_step = time_step
        self.freq = freq
        self.z = z
        self.time = -time_step

    def tick(self):
        """
        Advance time by one time step.
        """
        self.time = self.time + self.time_step

    def eval_point(self):
        """
        Evaluate evaluate trajectory at current time.

        Return the coordinates of the trajectory as a tuple.
        """
        argument = 2 * math.pi * self.freq * self.time
        x = self.radius * math.cos(argument)
        y = self.radius * math.sin(argument)
        z = self.z

        return x,y,z

    def step(self):
        """
        Perform a step in the trajectory generation.

        Return the coordinates of the new point.
        """
        self.tick()
        x,y,z = self.eval_point()

        return x,y,z
