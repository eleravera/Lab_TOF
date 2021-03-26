import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import numpy
import matplotlib.pyplot as plt

import plot_functions
import fit_functions
import plot_functions
import geometry

def rate_and_saturation(t, ch0, ch1): 
#Calcola il rate degli eventi
  Delta_t = numpy.ediff1d(t)
  mask_t = Delta_t < 0
  t_run = t.max() -t.min() +  numpy.sum(mask_t) * 6553.6

  print("Il clock dell'FPGA è ripartito %d volte durante l'acquisizione:" % numpy.sum(mask_t) )
  print("\n%d Events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )

  #Cotrolla se ci sono eventi che hanno saturato l'FPGA
  saturation_ch0_mask = ch0 > 3.2
  saturation_ch1_mask = ch1 > 3.2

  print("Rate di eventi sopra soglia sul ch0:", numpy.sum(saturation_ch0_mask)/t_run)
  print("Rate di eventi sopra soglia sul ch1:", numpy.sum(saturation_ch1_mask)/t_run)
  print("Frazione di eventi sopra soglia: %f., %f.\n\n" % (numpy.sum(saturation_ch0_mask)/len(t), numpy.sum(saturation_ch1_mask)/len(t)))
  return 
  

def TOF(T13, T23, costant ): 
  TOF = ( T13 + T23 ) * 0.5 - costant
  range_TOF = (-5., 40.)
  plot_functions.histogram(TOF, "TOF[ns]", "dN/dT", bins = 20, range = range_TOF, f = False)
  return TOF
  
  
def x(T13, T23, m): 
  T12 = T13 - T23 
  
  x = (geometry.X1 * 100 - T12/m ) * 0.5
  plot_functions.histogram(x, "x [cm]", "dN/dx", bins=None , range = (-20., 300.), f = False)
  return x

def beta(l,  h13, TOF ): 
  beta = l / ((TOF)*30) 
  plot_functions.histogram(beta, "beta [cm]", "dN/dbeta", bins= None , range = (0., 3.), f = False)
  print(beta.min(), beta.max())
  return beta 

  
def l_vs_TOF(l, TOF):
  l_bins = numpy.linspace(l.min()-10, l.min() + 40, 5)
  mean_tof = []
  sigma_tof = []
  for i in range(len(l_bins)-1): 
    mask_l = (l > l_bins[i] ) * ( l < l_bins[i+1])
    opt, pcov = plot_functions.histogram(TOF[mask_l], "tof", "dn/dtof", bins = 20, range = (0., 40.), f=True, density = False)
    mean_tof.append(opt[1])
    sigma_tof.append( numpy.sqrt(pcov.diagonal())[1] )
  mean_tof = numpy.array(mean_tof)
  sigma_tof = numpy.array(sigma_tof)
  l_bins_center = 0.5 * (l_bins[1:] + l_bins[:-1])
  
  mask_l = numpy.full(l_bins_center.size, True) #l_bins_center<165.
  opt, pcov = plot_functions.line_fit( l_bins_center[mask_l], mean_tof[mask_l],  sigma_tof[mask_l], "l", "tof")
  v = 1/ opt[0]
  dv = numpy.sqrt(pcov.diagonal())[0]/(opt[0])**2
  print("v+- dv", v, dv)
  return 


  
  
