import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.stats import pearsonr


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

    print("efficienza/tot:", numpy.sum(mask), len(mask))
    T1, T2, T12 = signal_propagation.DT_12(x1[mask], delay)
    TOF = signal_propagation.Time_Of_Flight(x1[mask], x3[mask], 0., beta[mask]) #geometry.h_13
    T13 = signal_propagation.DT_13(x1[mask], x3[mask], delay, TOF) 
    T23 = signal_propagation.DT_23(x1[mask], x3[mask], delay, TOF) 
    n_bins = 50
    
    
    #correlazione
    r, p = pearsonr(T12, T13)
    print("r, p T12 and T13:", r, p)
    
       
    plt.figure("x")
    plt.subplot(2, 1, 1)
    plt.hist(x1[mask],  bins = n_bins)   
    plt.subplot(2, 1, 2)
    plt.hist(x3[mask],  bins = n_bins)   


    plt.figure("T23,T13")
    plt.subplot(2, 1, 1)
    plt.hist(T23,  bins = n_bins, range= (22., 24))#T23.min(), T23.max()
    plt.subplot(2, 1, 2)   
    plt.hist(T13, bins = n_bins, range= (22., 24))   

    plt.figure("TOF")
    plt.hist(TOF,  bins = n_bins, range= (0, 2.))

    plt.figure("T12vsT13")
    plt.plot(T13, T12, '.')
    plt.xlabel("T13 [ns]")
    plt.xlim(0., 50.)
    plt.ylabel("T12 [ns]")
    plt.ylim(0., 50.)
    
    


    r, p = pearsonr(T23, T13)
    print("r, p T23 and T13:", r, p)
    
    plt.figure("T23vsT13")
    plt.plot(T23, T13, '.')
    plt.xlabel(" T23 [ns]")
    plt.xlim(0., 50.)
    plt.ylabel("T13 [ns]")
    plt.ylim(0., 50.)
        
    
    plt.ion()
    plt.show()
    
    
     
    
    
