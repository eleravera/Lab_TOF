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
options_parser.add_argument('-fondo_scala', '-s', type=int, help='')

options = vars(options_parser.parse_args())  
input_file = options['input_file']
scale = options['fondo_scala']

t, T12,  T13  = numpy.loadtxt(input_file, unpack = True)
t_run = t.max() -t.min()

Delta_t = numpy.ediff1d(t)
mask_t = Delta_t < 0
print("quante volte il clock riparte:" , numpy.sum(mask_t))
t_run = t.max() -t.min() +  numpy.sum(mask_t) * 6514


print("\n%d events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )
print("T12 max:", T12.max())
print("T13 max:", T13.max())

""" Saturazione FPGA """
mask1 = T12 > 3.2
mask2 = T13 > 3.2

print("rate eventi t12 sopra soglia", numpy.sum(mask1)/t_run)
print("rate eventi t13 sopra soglia",numpy.sum(mask2)/t_run)

print("t1 sopra soglia", 20 * numpy.sum(mask1)/t_run)
print("t1 sopra soglia", 20 *numpy.sum(mask2)/t_run)


print("Frazione di eventi sopra soglia: %f., %f." % (numpy.sum(mask1)/len(t), numpy.sum(mask2)/len(t)))
"""Istogramma"""
n_bins = 45 #int(numpy.sqrt(len(T12))) 
T12 = T12 * scale/10 #ns
T13 = T13 * scale/10 
print("MASSIMI", T12.max(), T13.max())

maskera0 = T12 < 0.5
print("integrale eventi <0.5", numpy.sum(maskera0))



range_T12 = (3., 100.) # 35, 50.
range_T13 = (3., 100.)


def T_hist_plot(t , xlabel, ylabel, range_t):
  n_bins = 45 #int(numpy.sqrt(len(T12))) 
  plt.figure()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  n, bins, patches = plt.hist(t,  bins = n_bins, range = range_t)
  bin_centers = 0.5 * (bins[1:] + bins[:-1])

  p0 = [len(t), numpy.mean(t), 1.]
  mask = (n > 0.) * (n < 830)
  opt, pcov = curve_fit(gauss, bin_centers[mask], n[mask], sigma = numpy.sqrt(n[mask]), p0 = p0)    
  print("Parametri del fit (norm, mean, sigma): %s" % opt)
  print("Matrice di covarianza:\n%s" % pcov) 
  print("Incertezze:\n%s" % numpy.sqrt(numpy.diagonal(pcov))) 

  bin_grid = numpy.linspace(*range_t, 1000)
  legend = ("norm: %f\nmean: %f\nsigma: %f" % tuple(opt))
  plt.plot(bin_grid, gauss(bin_grid, *opt), '-r', label = legend)    
  plt.legend() 
  return 


T_hist_plot(T12, "T_12 [ns]", "dN/dT_12", range_T12)
T_hist_plot(T13, "T_13 [ns]", "dN/dT_13", range_T13)

plt.figure("t13t12")
plt.plot(T12, T13, '.')
plt.xlabel("T12 [ns]")
plt.ylabel("T13 [ns]")

plt.ion() 
plt.show()


