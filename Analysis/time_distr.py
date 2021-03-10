import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def exponential(x, a, m): 
  return a * numpy.exp(-x * m)


"""Da terminale si da in input il file di acquisizione"""
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File di acquisizione')

options = vars(options_parser.parse_args())  
input_file = options['input_file']


t, T12,  T13  = numpy.loadtxt(input_file, unpack = True)
t_run = t.max() -t.min()
print("\n%d events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )

Delta_t = numpy.ediff1d(t)
print("Delta t max: ", Delta_t.max())

n_bins = 45
plt.figure("Time distribution")  
n, bins, patches = plt.hist(Delta_t,  bins = n_bins, range = (0., Delta_t.max()))
bin_centers = 0.5 * (bins[1:] + bins[:-1])
#p0 = [Delta, numpy.mean(t), 2.]
mask = (n > 0.)
opt, pcov = curve_fit(exponential, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]))    
print("fit parameters (amplitude, rate): %s" % opt)

bin_grid = numpy.linspace(0., Delta_t.max(), 1000)
legend = ("ampl: %f\nrate: %f" % tuple(opt))
plt.plot(bin_grid, exponential(bin_grid, *opt), '-r', label = legend)    
plt.legend() 

plt.ion()
plt.show()
