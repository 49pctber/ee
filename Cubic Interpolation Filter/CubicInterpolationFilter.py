""" CubicInterpolationFilter.py

A cubic interpolation filter.
Based on block diagram from "Digital Communications: A Discrete-Time Approach"
See section 8.4 Discrete-Time Techniques for M-ary PAM (p. 440 of my edition)

Interpolation with mu = 0. will return the third most recently entered sample value.
Interpolation with mu = 1. will return the second most recently entered sample value.
Interpolation with a fractional mu will return the interpolation value between those two samples.

Author: redd
"""

class CubicInterpolationFilter:

    epsilon = 0.0001 # for floating point rounding errors

    def __init__(self):
        self.__s = [0.0, 0.0, 0.0, 0.0] # samples
        self.__fc = [0.0, 0.0, 0.0, 0.0] # filter coefficients

    def describe(self):
        """
        Describe current state of the filter
        """
        for key, val in self.__dict__.items():
            print(key, val)

    def addSample(self, x):
        """
        Add a sampled value.
        """
        # add new sample
        self.__s.insert(0, x)
        self.__s.pop(len(self.__s)-1)
        # update filter coefficients
        self.__fc[3] = self.__s[0] / 6 + self.__s[1] /-2 + self.__s[2] / 2 + self.__s[3] /-6
        self.__fc[2] =                   self.__s[1] / 2 + self.__s[2] /-1 + self.__s[3] / 2
        self.__fc[1] = self.__s[0] /-6 + self.__s[1]     + self.__s[2] /-2 + self.__s[3] /-3 
        self.__fc[0] =                                     self.__s[2]

    def interpolate(self, mu):
        """
        Calculates the interpolated value at a fraction mu between the third- and second-most recently added samples.
        """
        return (( self.__fc[3] * mu + self.__fc[2] ) * mu + self.__fc[1] ) * mu + self.__fc[0] 

    def __findExtrema(self):
        """
        Returns the type of interpolation being used (sometimes the cubic simplifies to parabolic or linear)
        followed by the locations of the min and max, if applicable.
        """
        if abs(self.__fc[3]) < self.epsilon and abs(self.__fc[2]) < self.epsilon: # no local extrema for linear interpolation
            return ['none', -1.0, -1.0]
        elif abs(self.__fc[3]) < self.epsilon: # parabolic interpolation has one extremum
            val = -self.__fc[1] / 2 / self.__fc[2]
            if self.__fc[2] > 0:
                ret = ['min', val, -1.0]
            else:
                ret = ['max', -1.0, val]
            return ret 
        else: # cubic interpolation has both extrema
            p = (-self.__fc[2] + (self.__fc[2]**2 - 3*self.__fc[3]*self.__fc[1])**0.5) / 3/self.__fc[3]
            m = (-self.__fc[2] - (self.__fc[2]**2 - 3*self.__fc[3]*self.__fc[1])**0.5) / 3/self.__fc[3]
            if self.__fc[0] > 0:
                max = m
                min = p
            else:
                max = p
                min = m
            return ['both', min, max]

    def findExtremum(self):
        """
        Returns whether a local max or min appears in interval from 0 to 1.
        If so, returns the value of mu that produces the max or min.
        """
        x = self.__findExtrema()
        
        extremum_type = 'none'
        mu = 0.0

        if x[0] != 'none':
            if x[1] >= 0.0 and x[1] < 1.0:
                extremum_type = 'min'
                mu = x[1]
            elif x[2] >= 0.0 and x[2] < 1.0:
                extremum_type = 'max'
                mu = x[2]
            else:
                pass  
            
        return [extremum_type, mu]


# Example Usage
if __name__ == "__main__":

    # packages required for plotting
    from matplotlib import pyplot as plt
    import numpy as np

    # instantiate filter
    f = CubicInterpolationFilter()

    # load samples into filter
    inputs = [3.0, 2.0, 2.2, 0.0]
    for i in range(0,len(inputs)):
        f.addSample(inputs[i])

    # calculate interpolated values
    x = np.array(np.linspace(-1.0, 2.0, num=100))
    y = f.interpolate(x)

    # find local extremum, if applicable
    [etype, mu] = f.findExtremum()

    # plot
    plt.plot(x, y, 'g--')
    plt.stem([-1, 0, 1, 2], inputs)
    if etype == 'none':
        plt.title("Cubic Interpolation Filter\nNo local extremum between 0.0, 1.0")
    elif etype == 'max':
        plt.stem([mu], [f.interpolate(mu)], 'r', markerfmt='ro')
        plt.title("Cubic Interpolation Filter\nLocal maximum in [0.0, 1.0) at "+str(mu))
    elif etype == 'min':
        plt.stem([mu], [f.interpolate(mu)], 'r', markerfmt='ro')
        plt.title("Cubic Interpolation Filter\nLocal minimum in [0.0, 1.0) at "+str(mu))
    plt.show()