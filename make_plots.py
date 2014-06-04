'''
Make summarizing plots for TracPy performance tests.
'''

import matplotlib.pyplot as plt
from glob import glob
import os
import numpy as np
import pdb

def read_data():
    '''
    Read in timing data from log files
    '''

    # Use all available test cases
    testdirs = glob(os.path.join('tests', '*'))
    times = np.empty((len(testdirs), 5))
    for i, testdir in enumerate(testdirs):

        logfile = open(os.path.join(testdir, 'log.txt'), 'r')
        log = logfile.read()
        logfile.close()
        pdb.set_trace()
        # read in times for different parts of simulation
        times[i,0] = log.expandtabs().splitlines()[-6][48:54] # 1: Preparing for simulation
        times[i,1] = log.expandtabs().splitlines()[-5][48:54] # 2: Preparing for model step
        times[i,2] = log.expandtabs().splitlines()[-4][48:54] # 3: Stepping, using TRACMASS
        times[i,3] = log.expandtabs().splitlines()[-3][48:54] # 4: Processing after model step
        times[i,4] = log.expandtabs().splitlines()[-2][48:54] # 5: Processing after simulation

    pdb.set_trace()
    return times


def plot(times):
    '''
    Make plots.
    '''

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times[0])

times = read_data()
plot(times)