""" Funzioni utili per fare plot, in particolare istogrammi e scatter plot """
import numpy
import matplotlib.pyplot as plt

#Disegna un istogramma e se attiva la flag ne fa il fit
def histogram(x, xlabel, bins = None, range = None, f=False):
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x)))
  if (range is None):
   range = (x.min(), x.max()) 
   
  plt.figure()
  plt.xlabel(xlabel)
  n, bins, patches = plt.hist(x,  bins = bins, range = range)


  if(f is True): 
    bin_centers = 0.5 * (bins[1:] + bins[:-1]) 
    p0 = [len(x), numpy.mean(x, 1.]
    mask = (n > 0.) 
    opt, pcov = curve_fit(gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0)    
    print("Parametri del fit (norm, mean, sigma): %s +-%s" % (opt, numpy.sqrt(numpy.diagonal(pcov))))
    print("Matrice di covarianza:\n%s" % pcov) 
    print("Chi quadro: ")
  
    bin_grid = numpy.linspace(*range, 1000)
    legend = ("norm: %f\nmean: %f\nsigma: %f" % tuple(opt))
    plt.plot(bin_grid, gauss(bin_grid, *opt), '-r', label = legend)        
    plt.legend() 
  return 
  
#Disegna due istogrammi in due subplot  
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
def hist2d(x, y, xlabel, ylabel, bins=None, ):
  plt.figure()
  if(bins is None ): 
    bins = int(numpy.sqrt(len(x))) 
  plt.hist2d(x, y,  bins=bins )  
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.colorbar()
  return   
