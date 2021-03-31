import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import numpy
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from matplotlib.colors import LogNorm


import plot_functions
import fit_functions
import plot_functions
import geometry

def TOF(T13, T23, costant ): 
  TOF = ( T13 + T23 ) * 0.5 - costant
  return TOF

def T12(T13, T23, costant): 
  T12 = T13 - T23 - costant      
  return T12
  
def x(T12, m): 
  x = (geometry.X1 * 100 - T12/m ) * 0.5   
  return x

def l(x, h, p3):
  l = numpy.sqrt(( x - p3 )**2 + h**2 )
  return l 

def beta(l,  h13, TOF): 
  c = geometry.c * 10**(-7) #cm/s
  beta = l / (TOF * c) 
  return beta 


def Ti_histogram(T13, T23, bins=None, range_T13=None, range_T23=None, norm = None, legend = '', title = '', figlabel = '', save_fig = False):   
  plot_functions.histogram(T23, "$T_{23} [ns]$", "entries/bin", bins=bins, range=range_T23, f = False, title = title , legend = legend)
  if save_fig == True: 
      plt.savefig('plot/T23%s.pdf' % figlabel, format = 'pdf')        
  plot_functions.histogram(T13, "$T_{13} [ns]$", "entries/bin", bins = bins, range=range_T23, f = False, title = title, legend = legend)
  if save_fig == True:   
      plt.savefig('plot/T13%s.pdf' % figlabel, format = 'pdf')     
  plot_functions.hist2d(T23, T13, "$T_{23} [ns]$", "$T_{13} [ns]$", bins=bins, range_x = range_T23, range_y = range_T13, norm = norm, title = title , legend = legend )  
  if save_fig == True:   
      plt.savefig('plot/T13_T23%s.pdf' % figlabel, format = 'pdf')    
  r, p = pearsonr(T23, T13)
  print("r, p T23 and T13:", r, p)
  return 
  
  
def tof_beta_histogram(TOF, T12, x, beta, bins=None, range_TOF=(-5, 20.), range_T12=None, range_x = (-20., 300.), range_beta = (0., 3.), legend = '', title = '', figlabel = '', save_fig = False):       
  
  plot_functions.histogram(TOF, "TOF[ns]", "entries/bin", bins = bins, range = range_TOF, f = False, title = title, legend = legend)
  if save_fig is True:
    plt.savefig('plot/TOF%s.pdf' % figlabel, format = 'pdf') 
         
  plot_functions.histogram(T12, "T12[ns]", "entries/bin", bins = bins, range = range_T12, f = False, title = title, legend = legend)
  if save_fig is True:
    plt.savefig('plot/T12%s.pdf' % figlabel, format = 'pdf') 
     
  plot_functions.histogram(x, "x [cm]", "entries/bin", bins=bins , range = range_x, f = False, title = title, legend = legend)
  if save_fig is True:
    plt.savefig('plot/x%s.pdf' % figlabel, format = 'pdf')

  plot_functions.histogram(beta, "$beta [cm/ns]$", "entries/bin", bins= bins , range = range_beta, f = False, title = title, legend = legend)
  if save_fig is True:
    plt.savefig('plot/beta%s.pdf' % figlabel, format = 'pdf')   
  
  #plot_functions.hist2d(TOF, l,  "TOF [ns]", "l[cm]", bins=bins, range_x = range_TOF, range_y = (100., 300.), norm = LogNorm())   
  #if save_fig is True:
  #  plt.savefig('plot/tof_l_2dhist%s.pdf' % figlabel, format = 'pdf')   
  return 
  
 
def l_vs_TOF(l, TOF, lmin, lmax, n_bins):
  l_bins = numpy.linspace(lmin , lmax, n_bins)
  mean_tof = []
  sigma_tof = []
  for i in range(len(l_bins)-1): 
    mask_l = (l > l_bins[i] ) * ( l < l_bins[i+1])
    plt.figure()
    n, bins, _ = plt.hist(TOF[mask_l], bins = 80, density = False)
    #opt, pcov = plot_functions.histogram(TOF[mask_l], "tof", "dn/dtof", bins = 80, f=True, density = False)
    #mean_tof.append(opt[1])
    #sigma_tof.append( numpy.sqrt(pcov.diagonal())[1] )
    mean_tof.append(numpy.mean(TOF[mask_l]))
    sigma_tof.append(numpy.std(TOF[mask_l]) / numpy.sqrt(len(TOF[mask_l])))
  mean_tof = numpy.array(mean_tof)
  sigma_tof = numpy.array(sigma_tof)
  l_bins_center = 0.5 * (l_bins[1:] + l_bins[:-1])
  
  return l_bins_center, mean_tof, sigma_tof
 
