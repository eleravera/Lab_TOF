" Il programma prende in ingresso un file con i seguenti parametri (per colonna): "
"  x (posizione sulla sbarra, cioè la posizione dello scintillatore piccolo) "
"  T_12 medio () "
"  T_12 larghezza  "

"  T_12 medio e T_12 larghezza sono i valori ottenuti dai fit gaussiani sugli spettri acquisiti con l'ADC  "
import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.optimize import curve_fit

def line(x, m , q):
  return m * x +q

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File dei tempi tra PM1 e PM2')

options = vars(options_parser.parse_args())  
input_file = options['input_file']


x, T12_norm, T12_mean, T12_sigma  = numpy.loadtxt(input_file, unpack = True)

"La risoluzione si definisce come FWHM della distribuzione in t / valor medio dello spettro "
T12_resolution = T12_sigma 
print(x, T12_mean, T12_resolution)

p0 = [1., 1. ]
opt, pcov = curve_fit(line, x, T12_mean, sigma = T12_sigma/numpy.sqrt(800), p0 = p0)    
print("Parametri del fit : %s" % opt)
print("Matrice di covarianza:\n%s" % pcov) 


"Risoluzione della misura del tempo in funzione di x "
plt.figure("Calibrazione")
plt.xlabel("x [cm]")
plt.ylabel("T12 [ns]")
plt.errorbar(x, T12_mean, yerr=T12_sigma/numpy.sqrt(800), xerr=None, fmt='.')
plt.plot(numpy.linspace(0.,300, 1000), line(numpy.linspace(0.,300, 1000), *opt), 'r' )


plt.figure("Risoluzione")
plt.xlabel("T12_mean [ns]")
plt.ylabel("Resolution")
plt.errorbar(T12_mean, T12_resolution, xerr=None, fmt='.')

plt.ion()
plt.show()
