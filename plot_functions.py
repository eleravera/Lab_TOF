""" Funzioni utili per fare plot"""

import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare

def gauss(x, norm, mean, sigma): 
  return (norm) * numpy.exp(-0.5 * ((x - mean)/sigma )**2)
  
def line(x, m , q):
  return m * x +q

def two_gauss(x, a, norm, mean1, sigma1, mean2, sigma2):
  return a * gauss(x, norm, mean1, sigma1) + (1-a) * gauss(x, norm, mean2, sigma2)


#Disegna un istogramma e se attiva la flag ne fa il fit
def histogram(x, xlabel, ylabel, bins = None, range = None, f=False):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x)))
  if (range is None):
   range = (x.min(), x.max()) 
  plt.figure()
  plt.xlabel(xlabel)
  n, bins, patches = plt.hist(x,  bins = bins, range = range)
  if(f is True): 
    bin_centers = 0.5 * (bins[1:] + bins[:-1]) 
    p0 = [len(x), numpy.mean(x), 1.]
    mask = (n > 0.) 
    opt, pcov = curve_fit(gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0)    
    print("\n\nFIT CON UNA GAUSSIANA\n")
    print("Parametri del fit (norm, mean, sigma): %s +-%s" % (opt, numpy.sqrt(numpy.diagonal(pcov))))
    print("Matrice di covarianza:\n%s" % pcov) 
    chi2, p = chisquare(n[mask], gauss(bin_centers[mask], *opt) )
    print("Chi quadro/ndof: ", chi2, len(n[mask]))  
    bin_grid = numpy.linspace(*range, 1000)
    legend = ("norm: %f\nmean: %f\nsigma: %f" % tuple(opt))
    plt.plot(bin_grid, gauss(bin_grid, *opt), '-r', label = legend)        
    plt.legend() 
  return 

#Disegna un istogramma e se attiva la flag ne fa il fit con due gaussiane 
def fit2gauss(x, xlabel, ylabel, bins = None, range = None, f=False):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x)))
  if (range is None):
   range = (x.min(), x.max())   
  plt.figure()
  plt.xlabel(xlabel)
  n, bins, patches = plt.hist(x,  bins = bins, range = range)
  if(f is True): 
    bin_centers = 0.5 * (bins[1:] + bins[:-1]) 
    p0 = [0.1, len(x), 15., 3., 17.5, 0.4]
    mask = (n > 0.) 
    opt, pcov = curve_fit(two_gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0)    
    print("\n\nFIT CON DUE GAUSSIANE\n")
    print("Parametri del fit (norm, mean, sigma): %s +-%s" % (opt, numpy.sqrt(numpy.diagonal(pcov))))
    print("Matrice di covarianza:\n%s" % pcov) 
    chi2, p = chisquare(n[mask], two_gauss(bin_centers[mask], *opt) )
    print("Chi quadro/ndof: ", chi2, len(n[mask]))  
    bin_grid = numpy.linspace(*range, 1000)
    #legend = ("OPT" % tuple(opt))
    plt.plot(bin_grid, two_gauss(bin_grid, *opt), '-r', label = None)        
    #plt.legend() 
  return 

  
#Disegna due istogrammi in due subplot  
def multiple_histogram(var1, var2, xlabel1, xlabel2, bins = None, range_var1= None, range_var2 = None ):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(var1)))
  if (range_var1 is None):
    range_var1 = (var1.min(), var1.max()) 
  if (range_var2 is None):
    range_var2 = (var2.min(), var2.max())   

  plt.figure()
  plt.subplot(2, 1, 1)
  plt.xlabel(xlabel1)
  n1, bins1, patches1 = plt.hist(var1,  bins = bins, range = range_var1)
  plt.subplot(2, 1, 2)
  plt.xlabel(xlabel2)
  n2, bins2, patches2 = plt.hist(var2,  bins = bins, range = range_var2)
  return   
  
#Disegna lo scatter plot di due variabili  
def scatter_plot(x, y, xlabel, ylabel):
  plt.figure()
  plt.plot(x, y, '.')
  plt.xlabel(xlabel)
  plt.xlim(x.min(), x.max())
  plt.ylabel(ylabel)
  plt.ylim(y.min(), y.max())  
  plt.grid(True)
  return   

#Disegna l'istogramma 2D di due variabili  
def hist2d(x, y, xlabel, ylabel, bins=None, range_x = None, range_y = None):
  plt.figure()
  if (range_x is None):
    range_x = (x.min(), x.max()) 
  if (range_y is None):
    range_y = (y.min(), y.max())   
   
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x))) 
  plt.hist2d(x, y,  bins=bins )  
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.colorbar()
  return   
  plt.ylabel(ylabel)
  plt.colorbar()
  return   
  
#fa plot in log  
def hist_log(x, xlabel, ylabel, bins = None, range = None):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x)))
  if (range is None):
   range = (x.min(), x.max())   
  bins = numpy.logspace( x.min(), x.max(), 101)
  plt.hist(x, bins = bins)
  plt.gca().set_xscale('log') 
  plt.xlabel() 
  return   
  

#
def line_fit(x, y, dy, xlabel, ylabel):
  p0 = [1., 1. ]
  opt, pcov = curve_fit(line, x, y, sigma = dy)    
  print("Parametri del fit : %s" % opt)
  print("Matrice di covarianza: %s\n" % pcov)
  chi2, p = chisquare(y, line(x, *opt) )
  print("chi square/ndof: ", chi2, len(x))
  plt.figure()
  plt.subplot(2, 1, 1)
  plt.ylabel(ylabel)
  plt.errorbar(x, y, yerr=dy, xerr=None, fmt='.')
  legend = ("m: %f ns/cm\nq: %f ns" % tuple(opt))
  plt.plot(numpy.linspace(x.min(), x.max, 1000), plot_functions.line(numpy.linspace(x.min(), x.max, 1000), *opt), 'r', label = legend)
  plt.legend() 
  plt.subplot(2, 1, 2)
  plt.errorbar(x, y-plot_functions.line(x, *opt), yerr=dy, fmt='.')
  plt.ylabel("residui")
  plt.xlabel(xlabel)
  return opt, pcov
  
