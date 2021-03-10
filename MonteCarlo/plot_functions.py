import numpy
import matplotlib.pyplot as plt


def histogram(var, xlabel, bin_var = None, range_var = None, f=False):

  if(bin_var is None ): 
    bin_var = int(numpy.sqrt(len(var)))
  if (range_var is None):
   range_var = (var.min(), var.max()) 
 
  plt.figure()
  plt.xlabel(xlabel)
  n, bins, patches = plt.hist(var,  bins = bin_var, range = range_var)
  bin_centers = 0.5 * (bins[1:] + bins[:-1])
  
  if(f is True): 
    p0 = [len(t), numpy.mean(t), 1.]
    mask = (n > 0.) 
    opt, pcov = curve_fit(gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0)    
    print("Parametri del fit (norm, mean, sigma): %s +-%s" % (opt, numpy.sqrt(numpy.diagonal(pcov))))
    print("Matrice di covarianza:\n%s" % pcov) 
    print("Chi quadro: ")
  
    bin_grid = numpy.linspace(*range_t, 1000)
    legend = ("norm: %f\nmean: %f\nsigma: %f" % tuple(opt))
    plt.plot(bin_grid, gauss(bin_grid, *opt), '-r', label = legend)        
    plt.legend() 
  
  return 
  
  
def multiple_histogram(var1, var2, xlabel1, xlabel2, bin_var = None, range_var1= None, range_var2 = None ):

  if(bin_var is None ): 
    bin_var = int(numpy.sqrt(len(var1)))
  if (range_var1 is None):
   range_var1 = (var1.min(), var1.max()) 
  if (range_var2 is None):
    range_var2 = (var2.min(), var2.max())   

  plt.figure()
  plt.subplot(2, 1, 1)
  plt.xlabel(xlabel1)
  n, bins, patches = plt.hist(var1,  bins = bin_var, range = range_var1)
  plt.subplot(2, 1, 2)
  plt.xlabel(xlabel2)
  n, bins, patches = plt.hist(var2,  bins = bin_var, range = range_var2)
  return   
