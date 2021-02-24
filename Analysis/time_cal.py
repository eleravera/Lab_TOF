" Il programma prende in ingresso un file con i seguenti parametri (per colonna): "
"  x (posizione sulla sbarra, cioè la posizione dello scintillatore piccolo) "
"  T_12 medio () "
"  T_12 larghezza  "

"  T_12 medio e T_12 larghezza sono i valori ottenuti dai fit gaussiani sugli spettri acquisiti con l'ADC  "

import numpy
import matplotlib.pyplot as plt
import argparse 

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File dei tempi tra PM1 e PM2')

options = vars(options_parser.parse_args())  
input_file = options['input_file']


#x, T12_mean, T12_sigma  = numpy.loadtxt(input_file, unpack = True)

"La risoluzione si definisce come FWHM della distribuzione in t / valor medio dello spettro "
T12_resolution = 2.35 * T12_sigma / T12_mean
print(x, T12_mean, T12_resolution)


"Risoluzione della misura del tempo in funzione di x "
plt.figure(1)
plt.xlabel("x [m]")
plt.ylabel("T12 [ns]")
plt.errorbar(x, T12_resolution, yerr=None, xerr=None, fmt='.')#xerr? yerr=?



plt.ion()
plt.show()
