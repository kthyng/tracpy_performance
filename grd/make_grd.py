""" This script creates a grid and forcing file for an idealized near-field plume case
"""



import os
import cPickle

import numpy as np
import netCDF4

import octant
import octant.roms



def make_grd(rootdir = '../project/',
             Hmin = 5.0, alpha = 0.001, 
             f = 1e-4,
             dx = 1e3, dy = 1e3,
             shp = (131, 259)):
    
    if not os.path.exists(rootdir):
        print ' ### Making directory %s' % rootdir
        os.mkdir(rootdir)
    
    M, L = shp
    x = np.arange(L, dtype='d') * dx
    y = np.arange(M, dtype='d') * dy
    
    xvert, yvert = np.meshgrid(x, y)
    
    grd = octant.grid.CGrid(xvert, yvert)
    
    # custom set coreolis paremeter (otherwise determined from grd.lat)
    grd.f = f
    
    # create an exponential depth profile, with decay radius Rh, and a value
    # of Hmin and Hmax at the river and ocean ends, respectively.
    cff1 = (grd.y_rho - grd.y_rho[1])*alpha + Hmin
    cff1 += 0.01 * np.random.randn(*grd.y_rho.shape) * cff1
    cff1[0] = cff1[1]
    cff2 = Hmin
    grd.h = np.maximum(cff1, cff2)
    
    grd.proj = None  # define non-georeference grid
    print 'Writing netcdf GRD file..'
    octant.roms.write_grd(grd, os.path.join(rootdir, 'grid.nc'), verbose=True)
