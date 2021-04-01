"""Genero un muone che passa nello scintillatore 3 a x fissato, e calcolo le cordinate in cui passerebbe nella barra scintillante. Le cordinate nello scintillatore 3 la chiamo _m (measured), e quelle nella barra scintillante _t (true)"""

import numpy
import argparse 
import datetime
import time
import matplotlib.pyplot as plt

import muon_generator_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--number_events', '-n', default=100, type=int, help='Numero di muoni da generare')
options_parser.add_argument('--position', '-x', default=1., type=float, help='Posizione dello scintillatore 3 sulla barra [m]')
options_parser.add_argument('--output_File_events', '-f', default='None', type=str, help='File su cui scrivere gli eventi')

if __name__ == '__main__' :   

    start_time = time.time()      
    options = vars(options_parser.parse_args())  
    N = options['number_events']
    x = options['position']
    output_file_events = options['output_File_events']

    #Genero un muone con le funzioni di muon_generator_functions nella configurazione con scintillatore 3 sopra la barra              
    E, P, beta = muon_generator_functions.muon_energy_generator(N, muon_generator_functions.distr_energy, 300., 1.e4) 
    x3, y3 = muon_generator_functions.position_on_S3_generator(N, x)
    theta, phi = muon_generator_functions.muon_angle_generator(N, muon_generator_functions.dist_theta)
    x1, y1, f = muon_generator_functions.propagation_from_S3_to_S1(x3, y3, theta, phi)


    #Stampa i dati su terminale
    data = numpy.vstack((x1, y1, theta, phi, x3, y3, f)).T  
    print("x1[m], y1[m], theta, phi, x3[m], y3[m], flag \n", data)

    #Calcolo l'accettanza    
    epsilon = numpy.sum(f)/N            
    print("Number of events hitting S1/Total number of events:", numpy.sum(f), "/", N, "=", epsilon)
    mask = (f == 1 )

    #Se passato un file di uscita scrive i dati su file                
    if(output_file_events.endswith('.txt')): 
      header ='%s\nx_input = %.4f [m]\naccettanza %d / %d \nE[MeV], P[MeV], beta, x1[m], y1[m], theta, phi, x3[m], y3[m], flag\n' % (datetime.datetime.now() , x, numpy.sum(f), N)
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.6f', '%.2f', '%.2f', '%.4f', '%.6f', '%d']
      numpy.savetxt(output_file_events, numpy.transpose([E[mask], P[mask], beta[mask], x1[mask], y1[mask], theta[mask], phi[mask], x3[mask], y3[mask], f[mask]]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")


    print("Time of execution: %s seconds " % (time.time() - start_time))


