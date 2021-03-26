import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import fit_functions

"""Da terminale si da in input il file di acquisizione"""
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File di acquisizione')


if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file = options['input_file']

    t, T23,  T13  = numpy.loadtxt(input_file, unpack = True)

    Delta_t = numpy.ediff1d(t)

    mask_restart = Delta_t < 0.
    t_run = t[len(t)-1] - t[0] +  numpy.sum(mask_restart) * 6553.6
    print("\n%d events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )   
    

    mask = Delta_t > 0.
    Delta_t = Delta_t[mask]
    print("Delta t max: ", Delta_t.max())

    range = (0., 40.)
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
    print("fit parameters (amplitude, rate): %s" % opt)

    residuals = y - fit_functions.exponential(x, *opt)
    chi2 = numpy.sum((residuals/dy)**2)
    #plt.text(0.7, 0.7, ), transform=plt.gca().transAxes)
    param_names = ['Amplitude', 'Rate']
    legend = ''
    for (name, value, error) in zip(param_names, opt, param_errors):
        legend += ("%s: %.3f $\pm$ %.3f\n" % (name, value, error))
    legend += ("$\chi^2$/d.o.f.=%.2f/%d "% (chi2, len(x) - len(opt)))
    bin_grid = numpy.linspace(*range, 1000)
    plt.plot(bin_grid, fit_functions.exponential(bin_grid, *opt), '-r', label = legend)   
    plt.legend() 

    plt.ion()
    plt.show()
