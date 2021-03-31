import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import numpy
import matplotlib.pyplot as plt

import plot_functions
import fit_functions
import plot_functions
import geometry


def TOF(T13, T23, costant , save_fig = False, figlabel = ''): 
  TOF = ( T13 + T23 ) * 0.5 - costant
  range_TOF = (-5., 40.)
  plot_functions.histogram(TOF, "TOF[ns]", "dN/dT", bins = 100, f = False, title = 'TOF')
  if save_fig is True:
    plt.savefig('plot_distribution/TOF%s.pdf' % figlabel, format = 'pdf')    
  return TOF


def T12(T13, T23, costant, save_fig = False, figlabel = ''): 
  T12 = T13 - T23 - costant
  
  plot_functions.histogram(T12, "T12[ns]", "dN/dT", bins = 100, f = False, title = 'T12')
  if save_fig is True:
    plt.savefig('plot_distribution/T12%s.pdf' % figlabel, format = 'pdf')      
  return T12
  
  
def x(T12, m,  save_fig = False, figlabel = ''): 
  x = (geometry.X1 * 100 - T12/m ) * 0.5
  plot_functions.histogram(x, "x [cm]", "dN/dx", bins=None , range = (-20., 300.), f = False, title = 'x')
  if save_fig is True:
    plt.savefig('plot_distribution/x%s.pdf' % figlabel, format = 'pdf')   
  return x

def l(x, h, p3):
  l = numpy.sqrt(( x - p3 )**2 + h**2 )
  return l 

def beta(l,  h13, TOF , save_fig = False, figlabel = ''): 
  c = geometry.c * 10**(-7) #cm/s
  beta = l / (TOF * c) 
  plot_functions.histogram(beta, "$Beta [cm/ns]$", "dN/dbeta", bins= None , range = (0., 3.), f = False, title = 'beta')
  if save_fig is True:
    plt.savefig('plot_distribution/beta%s.pdf' % figlabel, format = 'pdf')   
  return beta 




def l_vs_TOF(l, TOF, lmin, lmax, n_bins):
  l_bins = numpy.linspace(lmin , lmax, n_bins)
  mean_tof = []
  sigma_tof = []
  for i in range(len(l_bins)-1): 
    mask_l = (l > l_bins[i] ) * ( l < l_bins[i+1])
    #opt, pcov = plot_functions.histogram(TOF[mask_l], "tof", "dn/dtof", bins = 80, f=True, density = False)
    #mean_tof.append(opt[1])
    #sigma_tof.append( numpy.sqrt(pcov.diagonal())[1] )
    mean_tof.append(numpy.mean(TOF[mask_l]))
    sigma_tof.append(numpy.std(TOF[mask_l]) / numpy.sqrt(len(TOF[mask_l])))
  mean_tof = numpy.array(mean_tof)
  sigma_tof = numpy.array(sigma_tof)
  l_bins_center = 0.5 * (l_bins[1:] + l_bins[:-1])
  
  mask_l = numpy.full(l_bins_center.size, True) 
  opt, pcov = plot_functions.proportional_fit( l_bins_center[mask_l], mean_tof[mask_l],  sigma_tof[mask_l], "l", "tof")
  v = 1/ opt[0]
  dv = numpy.sqrt(pcov.diagonal())[0]/(opt[0])**2
  print("v+- dv", v, dv)
  
  return 


  
  
