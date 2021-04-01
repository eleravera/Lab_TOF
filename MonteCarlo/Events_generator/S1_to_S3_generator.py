import numpy
import matplotlib.pyplot as plt
import argparse 
import datetime
import time

import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import muon_generator_functions
import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--number_events', '-n', default=100, type=int, help='Numero di muoni da generare')
options_parser.add_argument('--output_File_events', '-f', default='None', type=str, help='File su cui scrivere gli eventi')
options_parser.add_argument('--plot_flag', '-p', default= False, type=bool, help='Flag to plot some distributions to test')

if __name__ == '__main__' :   
    
    start_time = time.time()   
    options = vars(options_parser.parse_args())  
    N = options['number_events']
    output_file_events = options['output_File_events']
    plot_flag = options['plot_flag']
     
    #Genero un muone con le funzioni di muon_generator_functions nella configurazione con scintillatore 3 sotto la barra       
    E, P, beta = muon_generator_functions.muon_energy_generator(N, muon_generator_functions.distr_energy, 300., 1.e5) 
    theta, phi = muon_generator_functions.muon_angle_generator(N, muon_generator_functions.dist_theta)
    
    x1, y1 = muon_generator_functions.position_on_S1_generator(N) 
    x3, y3, mask, z = muon_generator_functions.propagation_from_S1_to_S3(x1, y1, theta, phi)
    f = mask>0
    
    #Stampa i dati su terminale
    data = numpy.vstack((x1, y1, theta, phi, x3, y3, f)).T    
    print("x1, y1, theta, phi, x3, y3, flag \n", data)             
       
    #Calcolo l'accettanza
    epsilon = numpy.sum(f)/N    
    print("Number of events hitting S3/Total number of events on S1:", numpy.sum(f), "/", N, "=", epsilon)


    #Se passato un file di uscita scrive i dati su file            
    if(output_file_events.endswith('.txt')): 
      header ='%s \nE[MeV], P [MeV], beta, x1[m], y1[m], theta, phi, x3[m], y3[m], flag\n' % datetime.datetime.now()
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.6f', '%.2f', '%.2f', '%.4f', '%.6f', '%d']
      numpy.savetxt(output_file_events, numpy.transpose([E[mask], P[mask], beta[mask], x1[mask], y1[mask], theta[mask], phi[mask], x3[mask], y3[mask], f[mask]]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")
      
    print("Time of execution: %s seconds " % (time.time() - start_time))
           
         #Plot sulle distribuzioni dei dati generati: da usare come test
    if(plot_flag == True): 
      plot_functions.multiple_histogram(theta, phi, "theta", "phi", bins = 45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))  
      plot_functions.multiple_histogram(theta[mask], phi[mask], "theta[mask]", "phi[mask]", bins=45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))       
      plot_functions.multiple_histogram(x3, y3, "x3", "y3", bins=45)      
      plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]", bins=45)  
      plot_functions.multiple_histogram(x1, y1, "x1", "y1", bins=45)      
      plot_functions.multiple_histogram(x1[mask], y1[mask], "x1[mask]", "y1[mask]", bins=45)  
      
      plt.ion()
      plt.show()
      
      
      
