#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:09:05 2022

@author: andreacamilarianoescandon using plot file seisflows-legacy
"""

#!/usr/bin/env python

import os
import re
import glob
import shutil
import obspy
import numpy as np
import IPython.display as dp
import matplotlib.pyplot as plt

from scipy.integrate import simps
from PIL import Image

# Some utility functions (written by Ridvan Orsvuran)
def read_trace(filename):
    """Reads an ASCII file and returns a obspy Traces"""
    data = np.loadtxt(filename)
    # first column is time, second column is the data
    times = data[:, 0]
    disp = data[:, 1]
    # get station name from the filename
    net, sta, comp, *_ = filename.split("/")[-1].split(".")
    delta = times[1] - times[0]
    headers = {"station": sta, "network": net, "channel": comp, "delta": delta, "b": times[0]}
    return obspy.Trace(disp, headers)

def save_trace(tr, filename):
    """Writes out the traces as an ASCII file. Uses b value as the beginning."""
    data = np.zeros((len(tr.data), 2))
    data[:, 0] = tr.times()+tr.stats.b
    data[:, 1] = tr.data
    np.savetxt(filename, data)
       
def specfem_write_parameters(filename, parameters, output_file=None):
    """Write parameters to a specfem config file"""

    with open(filename) as f:
        pars = f.read()

    for varname, value in parameters.items():
        pat = re.compile(
            r"(^{varname}\s*=\s*)([^#$\s]+)".format(varname=varname),
            re.MULTILINE)
        pars = pat.sub(r"\g<1>{value}".format(value=value), pars)

    if output_file is None:
        output_file = filename

    with open(output_file, "w") as f:
        f.write(pars)     
        
def specfem2D_prep_save_forward(filename=None):
    if filename is None:
        filename = "./DATA/Par_file"
    params = {
        "SIMULATION_TYPE": 1,
        "SAVE_FORWARD": ".true.",
        "SAVE_MODEL": "binary",
        "NGNOD": 9
    }
    specfem_write_parameters(filename, params)
    
def specfem2D_prep_adjoint(filename=None):
    if filename is None:
        filename = "./DATA/Par_file"
    params = {
        "SIMULATION_TYPE": 3,
        "SAVE_FORWARD": ".false."
    }
    specfem_write_parameters(filename, params)
      
def grid(x, y, z, resX=100, resY=100):
    """
    Converts 3 column data to matplotlib grid
    """
    # Can be found in ./utils/Visualization/plot_kernel.py
    from scipy.interpolate import griddata

    xi = np.linspace(min(x), max(x), resX)
    yi = np.linspace(min(y), max(y), resY)

    # mlab version
    #Z = griddata(x, y, z, xi, yi, interp='linear')
    # scipy version
    Z = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

    X, Y = np.meshgrid(xi, yi)
    return X, Y, Z

# AR: function to replace line in text file ------------------------------------
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()