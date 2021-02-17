" Questo script serve per visualizzare le distribuzioni della differenza dei tempi tra l'arrivo del segnale nel PM1 e il PM2 (o viceversa)"
" Per la misura della risoluzione possiamo provare a fittare con una gaussiana"

from const import costants
import numpy
import matplotlib.pyplot as plt

def gauss(x, mean, sigma, norm): 
  return (norm) * numpy.exp(-0.5 * ((x - mean)/sigma )**2)

"Da terminale si da in input il file dei tempi tra PM1 e PM2 (acquisizioni con FPGA)"
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('input_file', 'f', type=str, help='File dei tempi tra PM1 e PM2')

options = vars(options_parser.parse_args())  
input_file = options['input_file']


"Non so come saranno fatti i file di acquisizione, bisognerà adattare questa parte sul momento"
#T12,  = numpy.loadtxt(input_file, unpack = True)
#counts = da definire
#dcount = numpy.sqrt(counts)

"Istogramma"
plt.figure(1)
plt.xlabel("T_12 [ns]")
plt.ylabel("counts")
plt.errorbar(T_12, counts, yerr=dcount, xerr=None, fmt='.') #xerr? Da discutere l'incertezza da assegnare a T12

"Fit gaussiano e plot del fit"
#p0 = [, ,]
opt, pcov = curve_fit(gauss, T_12, counts, p0 = None)
T_12max = numpy.amax(T_12)
#Qual è il range dell ADC? Al posto di 500 bisogna mettere i bin totali dell'ADC
plt.plot(numpy.linspace(0, T_12max, 500), gauss(numpy.linspace(0, T_12max, 500) , *opt), '-')

print("mean, sigma, norm: " , *opt )
ptint("matrice di covarianza: ", *pcov)
print("chi_square: " , chi_square )


plt.ion()
plt.show()


