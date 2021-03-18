""" 
    Questo script serve per visualizzare e fittare (con una gaussiana) le distribuzioni della differenza dei tempi tra l'arrivo del segnale
    nel PM1 e il PM2 e tra PM1 e PM3. 
    Per lanciare il programma scrivere su terminale 'python3 -i time_hist.py -f <nome_file.dat>'
"""
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

import fit_functions
import plot_functions
import geometry

#Opzioni da terminale: input file e fondo scala della tac
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, required = True, help='Input file')
options_parser.add_argument('-full_scale', '-s', default = 200, type=int, help='TAC s full scale')

options = vars(options_parser.parse_args())  
input_file = options['input_file']
scale = options['full_scale']

#Legge il file dati.
t, ch0,  ch1  = numpy.loadtxt(input_file, unpack = True)

#Calcola il rate degli eventi
Delta_t = numpy.ediff1d(t)
mask_t = Delta_t < 0
#t_switch = t[:-1][mask_t]
#print(t_switch)
t_run = t.max() -t.min() +  numpy.sum(mask_t) * 6553.6

print("Il clock dell'FPGA è ripartito %d volte durante l'acquisizione:" % numpy.sum(mask_t) )
print("\n%d Events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )

#Cotrolla se ci sono eventi che hanno saturato l'FPGA
saturation_ch0_mask = ch0 > 3.2
saturation_ch1_mask = ch1 > 3.2

print("Rate di eventi sopra soglia sul ch0:", numpy.sum(saturation_ch0_mask)/t_run)
print("Rate di eventi sopra soglia sul ch1:", numpy.sum(saturation_ch1_mask)/t_run)
print("Frazione di eventi sopra soglia: %f., %f.\n\n" % (numpy.sum(saturation_ch0_mask)/len(t), numpy.sum(saturation_ch1_mask)/len(t)))


#Analisi: ATTENZIONE BISOGNA ASSEGNARE I CANALI CORRETTAMENTE:
T23 = ch0 
T13 = ch1

t23 = T23 * scale/10 #[ns]
t13 = T13 * scale/10 #[ns]

mask_t13 = t13 > 3.
mask_t23 = t23 > 3.
mask = mask_t13 * mask_t23
T13 = t13[mask]
T23 = t23[mask]
print("Numero di eventi con Ti3 < 3ns:", numpy.sum(mask))

bins = 45 #int(numpy.sqrt(len(T23))) 
range_T23 = (0., 60.) # 35, 50.
range_T13 = (0., 60.)

plot_functions.histogram(T23, "T_23 [ns]", "dN/dT_23", bins , range = range_T23, f = False)
plot_functions.histogram(T13, "T_13 [ns]", "dN/dT_13", bins = bins, range = range_T13 , f = False)
plot_functions.hist2d(T23, T13, "T23 [ns]", "T13 [ns]", bins=None, range_x = (10., 40.), range_y = (10., 40.) )

r, p = pearsonr(T23, T13)
print("r, p T23 and T13:", r, p)


#Distribuzione TOF 
cost = 17.0 #ns
TOF = ( T13 + T23 ) * 0.5 - cost
range_TOF = (-10., 20.)
plot_functions.histogram(TOF, "TOF[ns]", "dN/dT", bins = bins, range = range_TOF, f = False)


#X
T12 = T13 - T23 
m_23 = 0.06421 #ns/cm
x = (geometry.X1 * 100 - T12/m_23 ) * 0.5
plot_functions.histogram(x, "x [cm]", "dN/dx", bins , range = (-20., 300.), f = False)



h13 = geometry.h_13 * 100 #cm
l = numpy.sqrt(x**2 + h13**2)
beta = l / (numpy.abs(TOF)*30) 



plot_functions.histogram(beta, "beta [cm]", "dN/dbeta", bins , range = (0., 10.), f = False)

print(beta.min(), beta.max())

plt.ion() 
plt.show()


