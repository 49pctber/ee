""" InterpolationFilter.py

A cubic interpolation filter.
Based on block diagram from "Digital Communications: A Discrete-Time Approach"
See section 8.4 Discrete-Time Techniques for M-ary PAM (p. 440 of my edition)

Interpolation with mu = 0. will return self.__s[2]
Interpolation with mu = 1. will return self.__s[1]
Interpolation with a fractional mu will return the interpolation value between those two samples.

Author: redd
"""

from matplotlib import pyplot as plt
import numpy as np

class InterpolationFilter:

    def __init__(self):
        self.__s = [0.0, 0.0, 0.0, 0.0] # samples
        self.__fc = [0.0, 0.0, 0.0, 0.0] # filter coefficients

    def describe(self):
        # describe current state of the filter
        for key, val in self.__dict__.items():
            print(key, val)

    def addInput(self, x):
        # add new sample
        self.__s.insert(0, x)
        self.__s.pop(len(self.__s)-1)
        # update filter coefficients
        self.__fc[3] = self.__s[0] / 6 + self.__s[1] /-2 + self.__s[2] / 2 + self.__s[3] /-6
        self.__fc[2] =                   self.__s[1] / 2 + self.__s[2] /-1 + self.__s[3] / 2
        self.__fc[1] = self.__s[0] /-6 + self.__s[1]     + self.__s[2] /-2 + self.__s[3] /-3 
        self.__fc[0] =                                     self.__s[2]

    def interpolate(self, mu):
        return (( self.__fc[3] * mu + self.__fc[2] ) * mu + self.__fc[1] ) * mu + self.__fc[0] 

# Example Usage
if __name__ == "__main__":
    
    f = InterpolationFilter()

    inputs = [1.5, 2.0, 1.5, 0.5]

    for i in range(0,len(inputs)):
        f.addInput(inputs[i])

    x = np.array(np.linspace(-1.0, 2.0, num=100))
    y = f.interpolate(x)

    plt.plot(x, y)
    plt.stem([-1, 0, 1, 2], inputs)
    plt.title("Cubic Interpolation Filter")
    plt.show()