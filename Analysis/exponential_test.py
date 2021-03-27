import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import plot_functions
import fit_functions
import utilities

"""Da terminale si da in input il file di acquisizione"""
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File di acquisizione')


if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file = options['input_file']

    t, T23,  T13  = numpy.loadtxt(input_file, unpack = True)
    t_run = utilities.acquisition_duration(t)
    
    Delta_t = numpy.ediff1d(t)
    mask = Delta_t > 0.
    Delta_t = Delta_t[mask]
    print("Delta t max: ", Delta_t.max())

    range = (0., 60.)
    n_bins = 20
    
    n, bins = numpy.histogram(Delta_t,  bins = n_bins, range = range)
    errors = numpy.sqrt(n)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    
    mask = (n > 0.)
    x = bin_centers[mask]
    y = n[mask]
    dy = errors[mask]
    
    plt.figure("Time distribution")  
    plt.errorbar(x, y, yerr=dy, fmt='o')
    p0 = (10., 0.1)
    opt, pcov = curve_fit(fit_functions.exponential, x, y, sigma = dy, p0=p0)
    param_errors = numpy.sqrt(pcov.diagonal())  

    residuals = y - fit_functions.exponential(x, *opt)
    chi2 = numpy.sum((residuals/dy)**2)
    ndof = len(y)-len(opt)
    
    param_names = ['amplitude', 'rate']
    param_units = ['', 'Hz']
    legend = plot_functions.fit_legend(opt, param_errors, param_names, param_units, chi2, ndof)
    title = '%d eventi %d secondi, 24/03/21' % (len(t), t_run)
    bin_grid = numpy.linspace(*range, 1000)
    plt.plot(bin_grid, fit_functions.exponential(bin_grid, *opt), '-r', label = legend)   
    plot_functions.set_plot("$\Delta t [s]$", "entries/bin", title = title)

    plt.ion()
    plt.show()
