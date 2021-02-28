""" Questo script serve per visualizzare le distribuzioni della differenza dei tempi tra l'arrivo del segnale nel PM1 e il PM2 e tra PM1 e PM3"""
import argparse 
import numpy
import matplotlib.pyplot as plt

"""Da terminale si da in input il file di acquisizione"""
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, help='File di acquisizione')

options = vars(options_parser.parse_args())  
input_file = options['input_file']


t, T12,  T13  = numpy.loadtxt(input_file, unpack = True)

t_run = t.max() -t.min()
print(len(t), "events recorded in ", t_run, "s")


"""Istogramma"""
bins = int(numpy.sqrt(len(T12))) 
print(bins)
bins = 40

plt.figure(1)
plt.xlabel("T_12 [arb_unit]")
plt.ylabel("dN/dT_12")
plt.hist(T12,  bins = bins, range = (0.4, 0.7))


plt.figure(2)
plt.xlabel("T_13 [arb_unit] ")
plt.ylabel("dN/dT_13")
plt.hist(T13,  bins = bins, range = (0.25, 0.6))

plt.ion()
plt.show()


