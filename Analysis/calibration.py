" Il programma prende in ingresso un file con i seguenti parametri (per colonna): "
"  x (posizione sulla sbarra, cioè la posizione dello scintillatore piccolo) "
"  T_12 medio () "
"  T_12 larghezza  "

"  T_12 medio e T_12 larghezza sono i valori ottenuti dai fit gaussiani sugli spettri acquisiti con l'ADC  "
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.optimize import curve_fit

import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File dei tempi tra PM1 e PM2')

options = vars(options_parser.parse_args())  
input_file = options['input_file']


x, n, T_norm, T_mean, T_sigma, dT_norm, dT_mean, dT_sigma  = numpy.loadtxt(input_file, unpack = True)

opt, pcov = plot_functions.line_fit(x, T_mean, T_sigma/numpy.sqrt(n),  "x [cm]", "T [ns]" )
print("Velocità misurata: %s +- %s\n" %(1/opt[0], numpy.sqrt(pcov[0][0])/opt[0]**2))


T_res = T_sigma * 2.35 
dT_res = (2.35) * dT_sigma #numpy.sqrt( (dT_sigma/T_mean)**2 + (T_sigma*dT_mean/T_mean**2)**2 )
opt, pcov = plot_functions.line_fit(x, T_res, dT_res, "x [cm]", "Risoluzione" )





plt.ion()
plt.show()
