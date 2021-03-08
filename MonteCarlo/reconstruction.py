import numpy
import matplotlib.pyplot as plt
import argparse 

import geometry
import signal_propagation

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file', '-f', default='None', type=str, help='File of the events')
options_parser.add_argument('--delay', '-d', default='30', type=int, help='Delay')

if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    delay_ns = options['delay']
     
    #E[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag     
    E, P, beta, x1, y1, theta, phi, x3, y3, f  = numpy.loadtxt(input_file, unpack = True)
    y1 = y1*100
    y3 = y3*100
   
    mask = (f == 1) 
    delay = numpy.ones(len(E[mask])) * delay_ns


    T1, T2, T12 = signal_propagation.DT_12(x1[mask], delay)
    TOF, T13 = signal_propagation.DT_13(x1[mask], x3[mask], delay, beta[mask]) 
    n_bins = 50

    print(T12, T13)

    plt.figure("T12,T13")
    plt.subplot(2, 1, 1)
    plt.hist(T12,  bins = n_bins)
    plt.subplot(2, 1, 2)   
    plt.hist(T13,  bins = n_bins)   

    plt.figure("TOF")
    plt.hist(TOF,  bins = n_bins, range= (6., 14.))

    plt.figure("T12vsT13")
    plt.plot(T12, T13, '.')

    plt.ion()
    plt.show()
    
    
     
    
    
