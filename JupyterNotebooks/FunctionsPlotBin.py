#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:09:05 2022

@author: andreacamilarianoescandon using plot file seisflows-legacy
"""

#!/usr/bin/env python

import sys
from os.path import exists

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
import numpy as np
import pylab
import scipy.interpolate
from mpl_toolkits.axes_grid1 import make_axes_locatable

import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib.path import Path


def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v/256 for v in value]

def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list. 
        
        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        
        Returns
        ----------
        colour map'''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))
        
    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = matplotlib.colors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp

def read_fortran(filename):
    """ Reads Fortran style binary data and returns a numpy array.
    """
    with open(filename, 'rb') as f:
        # read size of record
        f.seek(0)
        n = np.fromfile(f, dtype='int32', count=1)[0]

        # read contents of record
        f.seek(4)
        v = np.fromfile(f, dtype='float32')

    return v[:-1]

def mesh2grid(v, x, z):
    """ Interpolates from an unstructured coordinates (mesh) to a structured 
        coordinates (grid)
    """
    lx = x.max() - x.min()
    lz = z.max() - z.min()
    nn = v.size
    mesh = _stack(x, z)

    nx = np.around(np.sqrt(nn*lx/lz))
    nz = np.around(np.sqrt(nn*lz/lx))
    dx = lx/nx
    dz = lz/nz

    # construct structured grid
    x = np.linspace(x.min(), x.max(), int(nx))
    z = np.linspace(z.min(), z.max(), int(nz))
    X, Z = np.meshgrid(x, z)
    grid = _stack(X.flatten(), Z.flatten())

    # interpolate to structured grid
    V = scipy.interpolate.griddata(mesh, v, grid, 'linear')

    # workaround edge issues
    if np.any(np.isnan(V)):
        W = scipy.interpolate.griddata(mesh, v, grid, 'nearest')
        for i in np.where(np.isnan(V)):
            V[i] = W[i]

    return np.reshape(V, (nz, nx))
    
def _stack(*args):
    return np.column_stack(args)

def plotbin(x_coords_file,z_coords_file,database_file,figname,figlabel):
    # check filenames conform to SPECFEM2D naming convention
    assert 'proc000000_x.bin' in x_coords_file
    assert 'proc000000_z.bin' in z_coords_file
    assert 'proc000000_' in database_file

    # check that files actually exist
    assert exists(x_coords_file)
    assert exists(z_coords_file)
    assert exists(database_file)

    # read mesh coordinates
    #try:
    if True:
        x = read_fortran(x_coords_file)
        z = read_fortran(z_coords_file)
    #except:
    #    raise Exception('Error reading mesh coordinates.')

    # read database file
    try:
        v = read_fortran(database_file)
    except:
        raise Exception('Error reading database file: %s' % database_file)

    # check mesh dimensions
    assert x.shape == z.shape == v.shape, 'Inconsistent mesh dimensions.'
        
    #color map 
    hex_list = ['#e44c2e','#e68f3e','#efef5c','#eefeff','#75fbfe','#53b7f9','#050df5']

    #re-organizing x vector 
    vmin=np.min(v)-.1*np.max(v)
    vmax=np.max(v)+.1*np.max(v)
    fig, ax = plt.subplots(figsize=(3,3),dpi=250)
    #fig.set_size_inches(4,4)
    plt.rcParams.update({'font.size': 4})
    cmap=get_continuous_cmap(hex_list) #cm.RdYlBu
    cmapr=cmap
    cs = plt.tricontourf(x,z, v, cmap =cmapr, vmin=vmin, vmax=vmax, levels=np.linspace(vmin, vmax,25),extend='both')
    ax.axis('equal')
    plt.gca().set_adjustable("box")
    ax.set_xlabel('x-coord, m', fontsize=4)
    ax.set_ylabel('z-coord, m', fontsize=4)
    ax.tick_params(axis='both',which='major',labelsize=4)
    cbar=plt.colorbar(orientation = 'horizontal',fraction=0.05)
    cbar.set_label(figlabel, rotation=0)
    plt.show()
    fig.savefig(figname+".pdf",bbox_inches = 'tight')
