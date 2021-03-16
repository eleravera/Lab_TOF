import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.optimize import curve_fit

import plot_functions

def dx_correlation(x, opt, pcov): 
  sigma_m = pcov[0][0] * (x /opt[0]) **2 
  sigma_q = pcov[1][1] / opt[0]**2
  correlation = 2 * pcov[0][1] * (x / opt[0]**2) 
  return sigma_m + sigma_q + correlation


description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-fi', type=str, help='File dei tempi tra PM1 e PM2')
options_parser.add_argument('-output_file', '-fo', type=str, help='File di output')


if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    output_file = options['output_file']

    scale = 200
    t, ch0, ch1  = numpy.loadtxt(input_file, unpack = True)
    T23 = ch0 
    T13 = ch1
    T23 = T23 * scale/10 #[ns]
    T13 = T13 * scale/10 #[ns]

    #ATTENZIONE CHE DEVI ESPRIMERE TUTTO IN CM E NS
    
    cal13_file = '~/Scrivania/LABORATORIO/TOF/Lab_TOF/Analysis/calibration_T13.txt'
    #cal23_file = '' 
    #m_13, dm_13, q_13, dq_13  = numpy.loadtxt(cal13_file, unpack = True)
    #m_23, dm_23, q_23, dq_23  = numpy.loadtxt(cal23_file, unpack = True)
    #m, cost_tof  = numpy.loadtxt(input_file, unpack = True)  

    with open(cal13_file, 'r') as f:
      l = [[int(num) for num in line.split(',')] for line in f]
    print(l)


    #Calcola da T13 e T23 i valori di x: 
    x_13 = (T13 - q_13 )/m_13
    dx_13 = dx_correlation(x_13, opt_13, pcov_13) 

    x_23 = (T23 - q_23 )/m_23
    dx_23 = dx_correlation(x_23, opt_23, pcov_23) 
     

    #Calcola il TOF    
    cost_tof = 30.
    TOF = (T13 + T23) * 0.5 + cost_tof
    #dTOF = 



    #Calcola beta
    l = numpy.sqrt(() + (T13/m_13)**2 -(2*q_13 / m_13 + geometry.X1/m_13) * T13/m_13)
    beta = l / (TOF * geometry.c) 
    
    
    data = numpy.vstack((T13, x_13, dx_13, T23, x_23, dx_23, beta)).T       
    print("T13, x_13, dx_13, T23, x_23, dx_23, beta\n", data)             
     
    #Se passato un file di uscita scrive i dati su file            
    if(output_file.endswith('.txt')): 
      header ='%s \nT13[ns], x_13[cm], dx_13[cm], T23[ns], x_23[cm], dx_23[cm], beta\n' % datetime.datetime.now()
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f']
      numpy.savetxt(output_file, numpy.transpose([T13, x_13, dx_13, T23, x_23, dx_23, beta]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")
        

