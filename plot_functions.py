import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare
from matplotlib.colors import LogNorm

import fit_functions
import utilities

#Disegna un istogramma e se attiva la flag ne fa il fit
def histogram(x, xlabel, ylabel, bins = None, range = None, f=True, density = False, title = None):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x)))
  if (range is None):
   range = (x.min(), x.max()) 

  plt.figure()
  n, bins, patches = plt.hist(x,  bins = bins, range = range, density = density)
  set_plot(xlabel, ylabel, title = title)
    
  if(f is True): 
    bin_centers = 0.5 * (bins[1:] + bins[:-1]) 
    p0 = [len(x), numpy.mean(x), 1.]
    mask = (n > 0.) 
    opt, pcov = curve_fit(fit_functions.gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0)    
    results = ''
    for v, dv in zip(opt, pcov.diagonal()):
        results += '%f +- %f\n' % (v, numpy.sqrt(dv))
    print('Parametri fit con una gaussiana:\n%s' % results)
    chi2 = (n[mask] - fit_functions.gauss(bin_centers[mask], *opt))**2 / n[mask]
    chi2 = chi2.sum()
    ndof = len(n[mask])-len(opt)
    print("Chi quadro/ndof: ", chi2, ndof)  
    bin_grid = numpy.linspace(*range, 1000)
    legend = ("norm: %f\nmean: %f\nsigma: %f" % tuple(opt))
    plt.plot(bin_grid, fit_functions.gauss(bin_grid, *opt), '-r', label = legend)        
    plt.legend() 
    return opt, pcov
  

#Disegna un istogramma e se attiva la flag ne fa il fit con due gaussiane 
def fit2gauss(x, xlabel, ylabel, bins = None, range = None, f=False, p0=None, bounds = None, title = None):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x)))
  if (range is None):
   range = (x.min(), x.max())   
  if (bounds is None):
     bounds = (-numpy.inf, -numpy.inf, -numpy.inf, -numpy.inf, -numpy.inf , -numpy.inf), (numpy.inf, numpy.inf, numpy.inf,numpy.inf, numpy.inf, numpy.inf )
  
  plt.figure()
  n, bins, patches = plt.hist(x,  bins = bins, range = range)

  if(f is True): 
    bin_centers = 0.5 * (bins[1:] + bins[:-1]) 
    mask = (n > 0.) 
    opt, pcov = curve_fit(fit_functions.two_gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0, bounds = bounds)

    chi2 = (n[mask] - fit_functions.two_gauss(bin_centers[mask], *opt))**2 / n[mask]
    chi2 = chi2.sum()
    ndof = len(n[mask]) - len(opt)
    param_names = ['fraction', 'norm', '$\mu_{1}$', '$\sigma_1$', '$\mu_{2}$', '$\sigma_2$']    
    param_units = ['', 'ns$^{-1}$', 'ns', 'ns', 'ns', 'ns']  
    param_errors = numpy.sqrt(pcov.diagonal())
    legend = fit_legend(opt, param_errors, param_names, param_units, chi2, ndof)
    bin_grid = numpy.linspace(*range, 1000)   
    plt.plot(bin_grid, fit_functions.two_gauss(bin_grid, *opt), '-r', label = legend)        
    set_plot(xlabel, ylabel, title = title)
    return opt, pcov
  
 
  
#Disegna due istogrammi in due subplot  
def multiple_histogram(var1, var2, xlabel1, xlabel2, bins = None, range_var1= None, range_var2 = None , density = False):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(var1)))
  if (range_var1 is None):
    range_var1 = (var1.min(), var1.max()) 
  if (range_var2 is None):
    range_var2 = (var2.min(), var2.max())   

  plt.figure()
  plt.subplot(1, 2, 1)
  n1, bins1, patches1 = plt.hist(var1,  bins = bins, range = range_var1, density = density)
  ylabel1 = 'dn'
  set_plot(xlabel1, ylabel1, title = None)
  
  plt.subplot(1, 2, 2)
  ylabel2 = 'dn'
  set_plot(xlabel2, ylabel2, title = None)
  n2, bins2, patches2 = plt.hist(var2,  bins = bins, range = range_var2, density = density)
  return   
  
#Disegna lo scatter plot di due variabili  
def scatter_plot(x, y, xlabel, ylabel):
  plt.figure()
  plt.plot(x, y, '.')
  plt.xlim(x.min(), x.max())
  plt.ylim(y.min(), y.max())  
  
  set_plot(xlabel, ylabel, title=None)
  
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
  plt.hist2d(x, y,  bins=bins , range = (range_x, range_y), norm=LogNorm())  
  set_plot(xlabel, ylabel, title=None)
  plt.colorbar()
  return   

  
#fa plot in log  
def hist_log(x, xlabel, ylabel, bins = None, range = None):
  if (range is None):
   range = (x.min(), x.max())   
  
  if (bins is None): 
    bins = numpy.logspace( numpy.log(x.min()), numpy.log(x.max()), 101)
  plt.hist(x, bins = bins)
  plt.gca().set_xscale('log') 
  set_plot(xlabel, ylabel, title=None) 
  return   
  

#
def line_fit(x, y, dy, xlabel, ylabel, title = ''):
    p0 = [1., 1. ]
    opt, pcov = curve_fit(fit_functions.line, x, y, sigma = dy)    
    param_errors = numpy.sqrt(pcov.diagonal())  
    res = y-fit_functions.line(x, *opt)
    chi2 = (res**2)/(dy**2)
    chi2 = chi2.sum()
    ndof = len(x) - len(opt)
  
    plt.figure()
    plt.subplot(2, 1, 1) 
    plt.errorbar(x, y, yerr = dy, xerr = None, fmt = '.')

  
    param_names = ['m', 'q' ]
    param_units = ['ns/cm', 'ns']
    legend = fit_legend(opt, param_errors, param_names, param_units, chi2, ndof)
    x_new = numpy.linspace(0., 300., 1000)
    plt.plot(x_new, fit_functions.line(x_new, *opt), 'r', label = legend)
    set_plot(xlabel, ylabel, title = title)  
    
    plt.subplot(2, 1, 2)
    plt.errorbar(x, res, yerr = dy, fmt = '.')
  
    set_plot(xlabel, "residui", title = '')
    print(legend)
    return opt, pcov
  
  
def set_plot(xlabel, ylabel, title = ''):

  plt.title(title, fontsize=12)
  plt.xlabel(xlabel, fontsize=14)
  plt.ylabel(ylabel, fontsize=14)
  plt.yticks(fontsize=14, rotation=0)
  plt.xticks(fontsize=14, rotation=0) 
  plt.subplots_adjust(bottom = 0.13, left = 0.15)  
  plt.legend() 
  return 
  
def fit_legend(param_values, param_errors, param_names, param_units, chi2, ndof):   
  legend = ''
  for (name, value, error, unit) in zip(param_names, param_values, param_errors, param_units):
      legend += ("%s: %s %s\n" % (name, utilities.format_value_error(value, error), unit))
  legend += ("$\chi^2$/d.o.f.=%.2f/%d "% (chi2, ndof))
  return legend
  
  
  
def set_double_axes(xlabel, ylabel1, ylabel2, title = ''):

  fig, ax = plt.subplots()

  plt.title(title, fontsize=12)
  #fig, ax = plt.subplots(constrained_layout = True)
  ax.set_xlabel(xlabel, fontsize=14)
  
  ax.set_ylabel(ylabel1, fontsize=14, color='g')
  secax = ax.secondary_yaxis('right')
  secax.set_ylabel(ylabel2, fontsize=14, color = 'b')
  plt.yticks(fontsize=14, rotation=0)
  plt.xticks(fontsize=14, rotation=0) 
  plt.subplots_adjust(bottom = 0.13, left = 0.15, right = 0.15)  
  
  return 


