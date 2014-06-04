#!/bin/env python2.7
# encoding: utf-8
"""
run_case.py

Edited by Kristen Thyng, 2014-06-04.

Created by Rob Hetland on 2007-10-15.
Copyright (c) 2007 Texas A&M University. All rights reserved.
Release under MIT license.
"""

import matplotlib
matplotlib.use('Agg')
import os
from grd import make_grd
import make_uv
import test


def run_case(rootdir, nx, ndrifters):
    
    ## Make grid ##

    print 'Making grid for %s' % rootdir

    shp = (3, 29, nx)

    grdshp = (shp[1]+3, shp[2]+3)
    make_grd(rootdir, Hmin=100.0, alpha=0.0, f=0,
             dx=3e3, dy=3e3, shp=grdshp)


    ## Make synthetic velocity fields ##

    print 'Making model output...'

    make_uv.make(rootdir)


    ## Run TracPy ##

    print 'Running TracPy...'

    test.run(rootdir, ndrifters)



if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--rootdir', type=str, default='./tests/', 
                        help='Simulation root directory.')
    parser.add_argument('--nx', type=int, default=2, 
                        help='number of grid points in x-direction (default=2)')
    parser.add_argument('--ndrifters', type=int, default=2, 
                        help='number of drifters (default=2)')
    args = parser.parse_args()
    
    run_case(rootdir=args.rootdir, nx=args.nx, ndrifters=args.ndrifters)
