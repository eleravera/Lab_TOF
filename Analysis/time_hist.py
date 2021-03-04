""" 
    Questo script serve per visualizzare e fittare (con una gaussiana) le distribuzioni della differenza dei tempi tra l'arrivo del segnale
    nel PM1 e il PM2 e tra PM1 e PM3. 
    Per lanciare il programma scrivere su terminale 'python3 -i time_hist.py -f <nome_file.dat>'
"""
import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def gauss(x, norm, mean, sigma): 
  return (norm) * numpy.exp(-0.5 * ((x - mean)/sigma )**2)


"""Da terminale si da in input il file di acquisizione"""
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File di acquisizione')

options = vars(options_parser.parse_args())  
input_file = options['input_file']


t, T12,  T13  = numpy.loadtxt(input_file, unpack = True)
t_run = t.max() -t.min()
print("\n%d events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )


"""Istogramma"""
n_bins = 45 #int(numpy.sqrt(len(T12))) 
T12 = T12 * 80 #ns
T13 = T13 * 80 

range_T12 = (37., 60.)
range_T13 = (20., 37.)


def T_hist_plot(t , xlabel, ylabel, range_t):
  n_bins = 45 #int(numpy.sqrt(len(T12))) 
  plt.figure()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  n, bins, patches = plt.hist(t,  bins = n_bins, range = range_t)
  bin_centers = 0.5 * (bins[1:] + bins[:-1])

  p0 = [len(t), numpy.mean(t), 2.]
  mask = (n > 0.)
  opt, pcov = curve_fit(gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0)    
  print("Parametri del fit (norm, mean, sigma): %s" % opt)
  print("Matrice di covarianza:\n%s" % pcov) 

  bin_grid = numpy.linspace(*range_t, 1000)
  plt.plot(bin_grid, gauss(bin_grid, *opt), '-r')    
 
  return 


T_hist_plot(T12, "T_12 [ns]", "dN/dT_12", range_T12)
T_hist_plot(T13, "T_13 [ns]", "dN/dT_13", range_T13)

plt.ion() 
plt.show()


