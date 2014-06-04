'''
Script to run drifters in various test cases to assess TracPy performance.
'''

import matplotlib as mpl
mpl.use("Agg") # set matplotlib to use the backend that does not require a windowing system
import numpy as np
import tracpy
import init
from datetime import datetime, timedelta
from tracpy.tracpy_class import Tracpy
import os
import time

def init(rootdir, ndrifters):
    '''
    Initialize simulation.
    '''

    name = os.path.join(rootdir, 'tracks')

    # Where to find simulation information
    currents_filename = os.path.join(rootdir, 'ocean_his_0001.nc')
    grid_filename = os.path.join(rootdir, 'grid.nc')
    time_units = 'seconds since 1970-01-01'
    num_layers = 3

    nsteps = 5

    # Number of steps to divide model output for outputting drifter location
    N = 4

    # This is a forward-moving simulation
    ff = 1 

    # Time between outputs
    tseas = 4*3600. # 4 hours between outputs, in seconds 
    ah = 0.
    av = 0. # m^2/s

    # Number of days
    ndays = tseas*9./(3600.*24)

    # surface drifters
    z0 = 's'  
    zpar = num_layers-1 # top layer

    # for 3d flag, do3d=0 makes the run 2d and do3d=1 makes the run 3d
    do3d = 0
    doturb = 0

    # for periodic boundary conditions in the x direction
    doperiodic = 1

    # Flag for streamlines. All the extra steps right after this are for streamlines.
    dostream = 0

    # Initialize Tracpy class
    tp = Tracpy(currents_filename, grid_filename, name=name, tseas=tseas, ndays=ndays, nsteps=nsteps,
                N=N, ff=ff, ah=ah, av=av, doturb=doturb, do3d=do3d, z0=z0, zpar=zpar, time_units=time_units,
                savell=False, doperiodic=0)

    # one particle starting position times however many drifters
    x0 = np.ones(ndrifters)*12000.
    y0 = np.ones(ndrifters)*31000.

    return tp, x0, y0


def run(rootdir, ndrifters):

    # Start date in date time formatting
    date = datetime(2013, 12, 19, 0)

    # Simulation initialization
    itime = time.time()
    tp, x0, y0 = init(rootdir, ndrifters)

    print '\nAdditional time for initialization:%4.4f\n' % (time.time() - itime)

    xp, yp, zp, t, T0, U, V = tracpy.run.run(tp, date, x0, y0)


if __name__ == "__main__":
    run()    
