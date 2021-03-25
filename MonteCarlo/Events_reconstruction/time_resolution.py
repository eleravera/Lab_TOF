import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import argparse
import numpy
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

def convolution_and_fit(T_sim, T_measured, xlabel, ylabel, data_bins, data_range, sim_bins, sim_range): 
    #Calcola la spline
    plt.figure()
    n, bins, patches = plt.hist(T_sim, bins = sim_bins, range = sim_range)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    index_max = n.argmax()
    delta_bin =  20 * int(len(bin_centers)/(max(bin_centers) - min(bin_centers)))
    index_low = index_max - delta_bin
    index_high = index_max + delta_bin    
    x = bin_centers[index_low:index_high]
    polynomial_f = interp1d(x, n[index_low:index_high], kind='cubic')    
    plt.plot(x, polynomial_f(x), '-', label = 'Spline geometria')
    plt.xlabel(xlabel)
    plt.legend()
    
    p0 = [0.2, len(x), 25. , 3., 26. , 0.6]
    bounds = (0., -numpy.inf, numpy.mean(x)-5., 1., numpy.mean(x)-5. , 0.1 ), (1., numpy.inf, numpy.mean(x)+5., 5., numpy.mean(x)+5., 0.9 )    
    #calcola i parametri della doppia gaussiana e calcola la convoluzione
    opt_true, pcov_true = plot_functions.fit2gauss(T_measured, xlabel, ylabel, bins = data_bins, range=data_range, f = True, p0=p0, bounds = bounds)    
    convolved_fit_function = fit_functions.create_convolution(polynomial_f, fit_functions.two_gauss) 
    
    #Fa il fit  
    plt.figure()
    ni, bins, pat = plt.hist(T_measured, bins = data_bins, range=data_range)
    nj = ni[index_low:index_high] 
    mask_fit = nj>0
    opt, pcov = curve_fit(convolved_fit_function, x[mask_fit], nj[mask_fit], p0 = opt_true, bounds = bounds)
    results = ''
    for v, dv in zip(opt, pcov.diagonal()):
        results += '%f +- %f\n' % (v, numpy.sqrt(dv))
    print('\nParametri fit convoluzione:\n%s' % results)
    chi2 = (nj[mask_fit] - convolved_fit_function(x[mask_fit], *opt))**2 / nj[mask_fit]
    chi2 = chi2.sum()
    print("Chi quadro/ndof: ", chi2, len(nj[mask_fit]), len(opt))  

    param_errors = numpy.sqrt(pcov.diagonal())  
    param_names = ['fraction', 'norm', 'mean', 'sigma1', 'mean2', 'sigma2']    
    legend = ''
    for (name, value, error) in zip(param_names, opt, param_errors):
        legend += ("%s: %.3f $\pm$ %.3f\n" % (name, value, error))
    legend += ("$\chi^2$/d.o.f.=%.2f/%d "% (chi2, len(x) - len(opt)))

    y = convolved_fit_function(x[mask_fit], *opt)
    plt.plot(x[mask_fit], y, '-', label = legend)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.yticks(fontsize=14, rotation=0)
    plt.xticks(fontsize=14, rotation=0)    

    
    plt.legend()
    return   
     
import geometry
import plot_functions
import signal_propagation_functions
import fit_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file_simulation', '-f', default='None', type=str, help='Input file')
options_parser.add_argument('--data_file', '-ff', default='None', type=str, help='Input file: dati')
options_parser.add_argument('--plot_flag', '-p', default= False, type=bool, help='Flag to plot some distributions to test')
options_parser.add_argument('-full_scale', '-s', default = 200, type=int, help='TAC s full scale')
  


if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file_sim = options['input_file_simulation']
    input_file_data = options['data_file']
    plot_flag = options['plot_flag']
    scale = options['full_scale']
    
    E, P, beta, x1, y1, theta, phi, x3, y3, f= numpy.loadtxt(input_file_sim, unpack = True)
    mask = f > 0.5
    
    t, ch0, ch1 = numpy.loadtxt(input_file_data, unpack = True)
    T23 = ch1
    T13 = ch0
    T23 = T23 * scale/10 #[ns]
    T13 = T13 * scale/10 #[ns]

    #Plot sulle distribuzioni dei dati generati: da usare come test
    if(plot_flag == True): 
      plot_functions.multiple_histogram(theta, phi, "theta", "phi", bins = 45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))  
      plot_functions.multiple_histogram(theta[mask], phi[mask], "theta[mask]", "phi[mask]", bins=45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))       
      plot_functions.multiple_histogram(x3, y3, "x3", "y3", bins=45)      
      plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]", bins=45)  
      plot_functions.multiple_histogram(x1, y1, "x1", "y1", bins=45)      
      plot_functions.multiple_histogram(x1[mask], y1[mask], "x1[mask]", "y1[mask]", bins=45)  
    
    
    delay = 26.1
    res = 0.
    TOF_sim = signal_propagation_functions.Time_Of_Flight(x1, x3, y1, y3, 0., beta)
    T13_sim = signal_propagation_functions.DT_13(x1, x3, delay, TOF_sim, res = res) 
    T23_sim = signal_propagation_functions.DT_23(x1, x3, delay, TOF_sim, res = res) 
    
    data_bins13 = 101
    data_range13 = (10., 45.)
    sim_bins13 = 101
    sim_range13 = (10., 45.)
    plt.figure()
    plt.hist(T13, bins = 80)
    plt.figure()
    plt.hist(T13_sim, bins = 80)   

    
    convolution_and_fit(T13_sim, T13, "$T_{13}[ns]$", "$dN/dT_{13}$", data_bins13, data_range13, sim_bins13, sim_range13 )
    
    
    
    
    print("-----------------------------------")
    data_bins23 = 100
    data_range23 = (0., 30.)
    sim_bins23 = 100
    sim_range23 = (0., 30.)    
   #convolution_and_fit(T23_sim, T23, "T23[ns]", data_bins23, data_range23, sim_bins23, sim_range23 )        
    
    
    plt.ion()
    plt.show()   
    
