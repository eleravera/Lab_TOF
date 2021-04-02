import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import numpy
import matplotlib.pyplot as plt

import fit_functions
import plot_functions
import geometry
import analysis_functions
import utilities

if __name__ == '__main__' :   
    m, dm , costant, tau_diff = utilities.read_parameter('vs_x/T13_T23_vs_x.txt', 'vs_x/Tsum_Tdiff_vs_x.txt')
    
    print(m)
    t, ch0,  ch1  = numpy.loadtxt('dati/Run65.dat', unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    t_run = utilities.acquisition_duration(t)      
    t12, tau = utilities.TAC_scale(ch0, ch1) 
    mask_0 = t12 > 0.0
    t12 = t12[mask_0]
    
  
    t, ch0,  ch1  = numpy.loadtxt('dati/Run64.dat', unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    t_run = utilities.acquisition_duration(t)      
    T12, tau = utilities.TAC_scale(ch0, ch1) 
    mask_0 = T12 > 0.0
    T12 = T12[mask_0]    
     
    T12 = numpy.concatenate((t12, T12)) 
    mean = numpy.mean(T12)
    print("mean", mean)
            
    bins = 101
    range = (0., 70.)    
    title = '%d eventi %d secondi, %s' % (len(T12), t_run, '31/03/21')
    

    plt.figure()
    n, bins = numpy.histogram(T12,  bins = bins, range = range, density = None)
    n = n/n.max()
    n, bins, patches = plt.hist(bins[1:],  weights=n, bins = bins, label = '', alpha = 0.4)    
    plot_functions.set_plot('$T_{12}$ [ns]', 'a.u.', title = title)

    #T12 = T12 - mean    
    #x = (geometry.X1*100 - T12/numpy.abs(m))*0.5 
    #plot_functions.histogram(x, "x [cm]", "", f = False, bins = bins) 
    
    
    
    plt.ion()
    plt.show()
    
