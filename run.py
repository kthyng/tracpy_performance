"""
Run performance tests for TracPy:
* Create grid and idealized velocity fields for each case
* Run TracPy with a varying number of drifters
* Track timing performance
* Plot results
"""

import matplotlib as mpl
mpl.use("Agg") # set matplotlib to use the backend that does not require a windowing system
import os

preamble = '''#!/bin/bash

'''

def get_suffix(**kwargs):
    keys = kwargs.keys()
    keys.sort()
    suffix='test'
    for key in keys:
        suffix += '_%s_%i' % (str(key), kwargs[key])
    
    return suffix

def write_shell(nx, ndrifters):
    '''
    Write shell script for the case that is to be run. It will call a
    Python script to do the rest.
    '''

    suffix = get_suffix(nx=nx, ndrifters=ndrifters)
    rootdir = './tests/%s' % suffix

    # Make sure necessary directories exist
    if not os.path.exists(rootdir):
        os.makedirs(rootdir, mode=0777)

    shfile = os.fdopen(os.open('%s/test.sh' % rootdir, os.O_WRONLY | os.O_CREAT, 0o777), 'w')
    shfile.writelines(preamble)
    shfile.write('python2.7 ./run_case.py --rootdir %s --nx %i --ndrifters %i  > %s/log.txt \n' % (rootdir, nx, ndrifters, rootdir))
    shfile.close()

    return rootdir


def case(nx, ndrifters):
    '''
    Take in desired parameters for different cases and run.
    '''

    # Make sure necessary directories exist
    if not os.path.exists('tests'):
        os.makedirs('tests', mode=0777)

    # Write shell script that controls running things
    rootdir = write_shell(nx, ndrifters)

    # Run the shell script
    os.system('%s/test.sh' % rootdir)



## Cases to run ##

# Change number of drifters for fixed grid
case(nx=3500, ndrifters=2) # basic case
case(nx=3500, ndrifters=10)
case(nx=3500, ndrifters=50)
case(nx=3500, ndrifters=100)
case(nx=3500, ndrifters=500)
case(nx=3500, ndrifters=1000)
case(nx=3500, ndrifters=5000)
case(nx=3500, ndrifters=10000)
case(nx=3500, ndrifters=50000)
case(nx=3500, ndrifters=100000)
case(nx=3500, ndrifters=500000)
# case(nx=3500, ndrifters=1000000)

# Change number of grid points in x direction for fixed number of drifters
case(nx=50, ndrifters=5000)
case(nx=100, ndrifters=5000)
case(nx=500, ndrifters=5000)
case(nx=1000, ndrifters=5000)
case(nx=1500, ndrifters=5000)
case(nx=2000, ndrifters=5000)
case(nx=2500, ndrifters=5000)
case(nx=3000, ndrifters=5000)
case(nx=3500, ndrifters=5000)
case(nx=4000, ndrifters=5000)
case(nx=4500, ndrifters=5000)
case(nx=5000, ndrifters=5000)
# case(nx=5500, ndrifters=5000)
# case(nx=6000, ndrifters=5000)
# case(nx=6500, ndrifters=5000)
# case(nx=7000, ndrifters=5000)
# case(nx=7500, ndrifters=2)
# case(nx=8000, ndrifters=2)
# case(nx=8500, ndrifters=2)
# case(nx=9000, ndrifters=2)
# case(nx=9500, ndrifters=2)
# case(nx=10000, ndrifters=2)
