""" SampleShifter.py

Example of how to use CubicInterpolationFilter to shift a sampled signal by a fractional sample.
mu controls how far to shift signal.
black dots indicate sampled points
cyan dots indicate interpolated points

Author: redd
"""

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from CubicInterpolationFilter import CubicInterpolationFilter

# Increase resolution of matplotlib plots
matplotlib.rcParams['figure.dpi'] = 150

# Samples, 10 per cycle, 2 cycles
x = np.array(np.linspace(0, 4*np.pi, num=21))

# Fraction to shift signal
mu = 0.3 # 0.3 of a sample

# generate sampled signal
n = 0.1 * np.random.rand(len(x)) # add noise, if desired.
y = np.sin(x) + n # sampled signal
plt.plot(x, y, 'k.') # plot signal

# filter
cif = CubicInterpolationFilter()
for i in range(0,len(y)):
    cif.addSample(y[i]) # add a sample to the filter
    out = cif.interpolate(mu) # interpolated value
    if i >= 3: # plot interpolated points once filter has enough data
        plt.plot(mu*x[i-1]+(1-mu)*x[i-2],out,'c.')

plt.title("Interpolation Demo\nBlack points are samples, cyan points are interpolated, mu="+str(mu))
plt.show()