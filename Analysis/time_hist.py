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
"Regolazione scala "
T12 = T12 * 80 #ns
T13 = T13 * 80 

t_run = t.max() -t.min()
print("\n%d events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )


"""Istogramma"""
n_bins = 45 #int(numpy.sqrt(len(T12))) 

plt.figure(1)
plt.xlabel("T_12 [ns]")
plt.ylabel("dN/dT_12")
n, bins, patches = plt.hist(T12,  bins = n_bins, range = (0., 50.))

bin_centers = 0.5 * (bins[1:] + bins[:-1])
p0 = [200, 42., 2.]
opt_12, pcov_12 = curve_fit(gauss, bin_centers, n, p0 = p0)    

print("Parametri del fit T12 (norm, mean, sigma): %s" % opt_12)
print("Matrice di covarianza:\n%s" % pcov_12) 
plt.plot(bin_centers, gauss(bin_centers, *opt_12), '-r')    



plt.figure(2)
plt.xlabel("T_13 [ns] ")
plt.ylabel("dN/dT_13")
n, bins, patches = plt.hist(T13,  bins = n_bins, range = (20., 45.))
bin_centers = 0.5 * (bins[1:] + bins[:-1])
p0 = [200, 33., 2.]
opt_13, pcov_13 = curve_fit(gauss, bin_centers, n,  p0 = p0)    
print("Parametri del fit T13 (norm, mean, sigma): %s" % opt_13)
print("Matrice di covarianza:\n%s" % pcov_13) 
plt.plot(bin_centers, gauss(bin_centers, *opt_13), '-r')  


plt.ion() 
plt.show()


