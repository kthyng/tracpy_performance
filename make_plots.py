'''
Make summarizing plots for TracPy performance tests.
'''

import matplotlib.pyplot as plt
from glob import glob
import os
import numpy as np
import pdb
import matplotlib

def read_data():
    '''
    Read in timing data from log files
    '''

    # Use all available test cases
    testdirs = glob(os.path.join('tests', 'test_*'))
    ntests = len(testdirs)
    times = np.empty((ntests, 6))
    nx = np.empty(ntests)
    ndrifters = np.empty_like(nx)
    for i, testdir in enumerate(testdirs):

        logfile = open(os.path.join(testdir, 'log.txt'), 'r')
        log = logfile.read()
        logfile.close()
 
        # read in times for different parts of simulation
        times[i,0] = log.split(':')[1][:6] # Time for initialization
        times[i,1] = log.split('1: Preparing for simulation    \t\t')[1][:6]
        times[i,2] = log.split('2: Preparing for model step    \t\t')[1][:6]
        times[i,3] = log.split('3: Stepping, using TRACMASS    \t\t')[1][:6]
        times[i,4] = log.split('4: Processing after model step \t\t')[1][:6]
        times[i,5] = log.split('5: Processing after simulation \t\t')[1][:6]
        # times[i,1] = log.expandtabs().splitlines()[-6][48:54] # 1: Preparing for simulation
        # times[i,2] = log.expandtabs().splitlines()[-5][48:54] # 2: Preparing for model step
        # times[i,3] = log.expandtabs().splitlines()[-4][48:54] # 3: Stepping, using TRACMASS
        # times[i,4] = log.expandtabs().splitlines()[-3][48:54] # 4: Processing after model step
        # times[i,5] = log.expandtabs().splitlines()[-2][48:54] # 5: Processing after simulation

        # save order of simulation properties
        nx[i] = int(testdir.split('nx')[1].split('_')[1])
        ndrifters[i] = int(testdir.split('ndrifters')[1].split('_')[1])

    # pdb.set_trace()
    return times, nx, ndrifters


def plot(times, nx, ndrifters):
    '''
    Make plots.
    '''

    ## Plot simulations for which ndrifters==2 and grid resolution changes

    matplotlib.rcParams.update({'font.size': 16})#,'font.weight': 'bold'})

    total = times.sum(axis=1)

    ind = ndrifters==2
    isort = np.argsort(nx[ind]) # indices that sort in order

    fig = plt.figure(figsize=(18,6))
    ax = fig.add_subplot(1,2,1)
    ax.stackplot(nx[ind][isort]*29, times[ind,0][isort]/total[ind][isort], 
                times[ind,1][isort]/total[ind][isort],
                times[ind,2][isort]/total[ind][isort], 
                times[ind,3][isort]/total[ind][isort], 
                times[ind,4][isort]/total[ind][isort], 
                times[ind,5][isort]/total[ind][isort], 
                colors=['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
    ax.set_xlabel('Number of grid cells')
    ax.set_title('Effect of changing number of grid cells')
    ax.autoscale(axis='x', tight=True)
    ax.set_ylabel('Time [s]')
    ylims = ax.get_ylim()

    ## Plot simulations for which nx==10 and number of drifters changes

    ind = nx==10
    isort = np.argsort(ndrifters[ind]) # indices that sort in order

    ax = fig.add_subplot(1,2,2)
    ax.stackplot(ndrifters[ind][isort], times[ind,0][isort]/total[ind][isort], 
                times[ind,1][isort]/total[ind][isort],
                times[ind,2][isort]/total[ind][isort], 
                times[ind,3][isort]/total[ind][isort], 
                times[ind,4][isort]/total[ind][isort], 
                times[ind,5][isort]/total[ind][isort], 
                colors=['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
    ax.set_xlabel('Number of drifters')
    ax.set_title('Effect of changing number of drifters')
    ax.autoscale(axis='x', tight=True)
    ax.set_ylim(ylims)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.subplots_adjust(left=0.05, bottom=0.11, right=0.97, 
                        top=0.94, wspace=0.04, hspace=0.2)


    ## Overlay legend
    ax.text(0.05, 0.95, 'Initialization', color='r', transform=ax.transAxes)
    ax.text(0.05, 0.90, 'Preparing for run', color='orange', transform=ax.transAxes)
    ax.text(0.05, 0.85, 'Preparing for step', color='y', transform=ax.transAxes)
    ax.text(0.05, 0.80, 'Stepping', color='green', transform=ax.transAxes)
    ax.text(0.05, 0.75, 'After step', color='b', transform=ax.transAxes)
    ax.text(0.05, 0.70, 'After run', color='purple', transform=ax.transAxes)

    fig.savefig('figures/comparison_relative.pdf')


    ind = ndrifters==2
    isort = np.argsort(nx[ind]) # indices that sort in order

    fig = plt.figure(figsize=(18,6))
    ax = fig.add_subplot(1,2,1)
    ax.stackplot(nx[ind][isort]*29, times[ind,0][isort], 
                times[ind,1][isort],
                times[ind,2][isort], 
                times[ind,3][isort], 
                times[ind,4][isort], 
                times[ind,5][isort], 
                colors=['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
    ax.set_xlabel('Number of grid cells')
    ax.set_title('Effect of changing number of grid cells')
    ax.autoscale(axis='x', tight=True)
    ax.set_ylabel('Time [s]')
    ylims = ax.get_ylim()

    ## Plot simulations for which nx==10 and number of drifters changes

    ind = nx==10
    isort = np.argsort(ndrifters[ind]) # indices that sort in order

    ax = fig.add_subplot(1,2,2)
    ax.stackplot(ndrifters[ind][isort], times[ind,0][isort], 
                times[ind,1][isort],
                times[ind,2][isort], 
                times[ind,3][isort], 
                times[ind,4][isort], 
                times[ind,5][isort], 
                colors=['red', 'orange', 'yellow', 'green', 'blue', 'purple'])
    ax.set_xlabel('Number of drifters')
    ax.set_title('Effect of changing number of drifters')
    ax.autoscale(axis='x', tight=True)
    # ax.set_ylim(ylims)
    # plt.setp(ax.get_yticklabels(), visible=False)
    plt.subplots_adjust(left=0.05, bottom=0.11, right=0.97, 
                        top=0.94, wspace=0.06, hspace=0.2)


    ## Overlay legend
    ax.text(0.05, 0.95, 'Initialization', color='r', transform=ax.transAxes)
    ax.text(0.05, 0.90, 'Preparing for run', color='orange', transform=ax.transAxes)
    ax.text(0.05, 0.85, 'Preparing for step', color='y', transform=ax.transAxes)
    ax.text(0.05, 0.80, 'Stepping', color='green', transform=ax.transAxes)
    ax.text(0.05, 0.75, 'After step', color='b', transform=ax.transAxes)
    ax.text(0.05, 0.70, 'After run', color='purple', transform=ax.transAxes)

    fig.savefig('figures/comparison_absolute.pdf')


times, nx, ndrifters = read_data()
plot(times, nx, ndrifters)