import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse
import numpy
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

import geometry
import plot_functions
import signal_propagation_functions
import fit_functions
import utilities


def convolution_and_fit(T_sim, T_measured, xlabel, ylabel, data_bins, data_range, sim_bins, sim_range, title = None, figlabel='', save_fig = False): 
    #Calcola la spline
    plt.figure()
    n, bins, patches = plt.hist(T_sim, bins = sim_bins, range = sim_range)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    x = bin_centers
    y = n
    polynomial_f = interp1d(x, y, kind='linear')    
    plt.plot(x, polynomial_f(x), '-', label = 'Spline geometria')
    plot_functions.set_plot(xlabel, ylabel, title='Simulazione Monte Carlo')
    if save_fig ==True:
      plt.savefig('dati_risoluzione/plot/spline%s.pdf' % figlabel, format = 'pdf')    
        
    data_mean = T_measured.mean()
    p0 = [0.15, len(T_measured)/data_bins,  data_mean - 1., 4., data_mean, 0.9]
    bounds = (0.1, 0., data_mean*0.7, 1., data_mean*0.7 , 0.3 ), (0.4, numpy.inf, data_mean*1.3, 6., data_mean*1.3, 1.)


    #calcola i parametri della doppia gaussiana e calcola la convoluzione
    opt_true, pcov_true = plot_functions.fit2gauss(T_measured, xlabel, ylabel, bins = data_bins, range=data_range, f = True, p0=p0,
    bounds = bounds, title = title)
    if save_fig ==True:    
      plt.savefig('dati_risoluzione/plot/2gauss_fit%s.pdf' % figlabel, format = 'pdf')    
    
    convolved_fit_function = fit_functions.create_convolution(polynomial_f, fit_functions.two_gauss)
    #Fa il fit  
    plt.figure()    
    ni, bins, pat = plt.hist(T_measured, bins = data_bins, range=data_range)
    x = 0.5 * (bins[1:] + bins[:-1])
    nj = ni
    mask_fit = nj>0

    middle_point = (min(x[mask_fit]) + max(x[mask_fit])) * 0.5
    p0 = numpy.copy(opt_true)
    p0[2] = middle_point - (opt_true[4] - opt_true[2])
    p0[4] = middle_point
    bounds = (0.1, 0., p0[2]*0.9, 1., p0[4]*0.9 , 0.4 ), (0.4, numpy.inf, p0[2]*1.1, 6., p0[4]*1.1, 1.)
    opt, pcov = curve_fit(convolved_fit_function, x[mask_fit], nj[mask_fit], p0 = p0, bounds = bounds)

    chi2 = (nj[mask_fit] - convolved_fit_function(x[mask_fit], *opt))**2 / nj[mask_fit]
    chi2 = chi2.sum()
    ndof = len(nj[mask_fit])- len(opt)
    
    param_errors = numpy.sqrt(pcov.diagonal())  
    param_values = numpy.copy(opt) 
    param_values[2] = param_values[2] - middle_point
    param_values[4] = param_values[4] - middle_point
    param_names = ['fraction', 'norm', '$\mu_{1}$', '$\sigma_1$', '$\mu_{2}$', '$\sigma_2$']    
    param_units = ['', 'ns$^{-1}$', 'ns', 'ns', 'ns', 'ns']        
    legend = plot_functions.fit_legend(param_values, param_errors, param_names, param_units, chi2, ndof)
    
    x_grid = x[mask_fit]
    y = convolved_fit_function(x_grid, *opt)
    plt.plot(x_grid, y, '-', label = legend)
    plot_functions.set_plot(xlabel, ylabel, title = title)

    if save_fig ==True:
      plt.savefig('dati_risoluzione/plot/conv_fit%s.pdf' % figlabel, format = 'pdf')    
    
    
    plt.figure()
    middle_point = (bins[-1] + bins[0]) * 0.5
    integral = numpy.sum(fit_functions.two_gauss(x_grid, *opt))
    plt.plot(x_grid - middle_point, fit_functions.two_gauss(x_grid, *opt)/integral, 'r-', label='Response function')     
    plot_functions.set_plot('Time [s]', 'pdf', title = 'Risoluzione ')
    if save_fig ==True:
      plt.savefig('dati_risoluzione/plot/risoluzione%s.pdf' % figlabel, format = 'pdf')
    
    return opt_true, pcov_true, param_values, pcov


description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file_simulation', '-f', default='None', type=str, help='Input file sim')
options_parser.add_argument('--data_file', '-ff', default='None', type=str, help='Input file: dati')
options_parser.add_argument('--save_fig', '-p', default=False, type=bool, help='')
options_parser.add_argument('--s3_position', '-x', type=str, help='position of s3')
options_parser.add_argument('--date', '-d', type=str, help='date')

if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file_sim = options['input_file_simulation']
    input_file_data = options['data_file']
    save_fig = options['save_fig']
    position = options['s3_position']
    date = options['date']

    E, P, beta, x1, y1, theta, phi, x3, y3, f = numpy.loadtxt(input_file_sim, unpack = True)
    mask = f > 0.5
    
    t, ch0, ch1 = numpy.loadtxt(input_file_data, unpack = True)
    t_run = utilities.acquisition_duration(t)      
    T13, T23 = utilities.TAC_scale(ch0, ch1) 
    string_x_n = '%s  %s' %(position, len(T13))
    


    delay_T13 = 26.1
    delay_T23 = 26.2
    res = 0.
    TOF_sim = signal_propagation_functions.Time_Of_Flight(x1[mask], x3[mask], y1[mask], y3[mask], 0., beta[mask])
    T13_sim = signal_propagation_functions.DT_13(x1[mask], x3[mask], delay_T13, TOF_sim, res = res) 
    T23_sim = signal_propagation_functions.DT_23(x1[mask], x3[mask], delay_T23, TOF_sim, res = res) 
 
    mask = (T13 > 2.)
    T13 = T13[mask] 
    
    data_bins = 201
    data_range = (0., 40.)
    sim_bins = 2001
    sim_range = (0., 40.)

    title = '%s cm , %d eventi %d secondi, %s' % (position, len(T13), t_run, date)  
    figlabel = position + 'cm_T13'   
    opt, pcov, opt_conv, pcov_conv = convolution_and_fit(T13_sim, T13, "$T_{13}[ns]$", "entries/bin", data_bins, data_range, sim_bins, sim_range, title, figlabel, save_fig )
 
    param_2gauss_fit = utilities.make_opt_string(opt, pcov, s = string_x_n)
    param_conv_fit = utilities.make_opt_string(opt_conv, pcov_conv, s = string_x_n)


    with open("T13_2gauss.txt", "a") as output_file:
        output_file.write(param_2gauss_fit)
 
    with open("T13_conv.txt", "a") as output_file:
        output_file.write(param_conv_fit)
        
    print("\n\n-----------------------------------\n\n")
    
    mask = (T23 > 2.)
    T23 = T23[mask] 
    
    title = '%s cm , %d eventi %d secondi, %s' % (position, len(T23), t_run, date)
    figlabel = position + 'cm_T23'   
    opt, pcov, opt_conv, pcov_conv = convolution_and_fit(T23_sim, T23, "$T_{23}[ns]$", "entries/bin", data_bins, data_range, sim_bins, sim_range, title, figlabel, save_fig)        
    
    param_2gauss_fit = utilities.make_opt_string(opt, pcov, s = string_x_n)
    param_conv_fit = utilities.make_opt_string(opt_conv, pcov_conv, s = string_x_n)
    print(param_2gauss_fit, '\n')
    print(param_conv_fit)

    with open("T23_2gauss.txt", "a") as output_file:
        output_file.write(param_2gauss_fit)
 
    with open("T23_conv.txt", "a") as output_file:
        output_file.write(param_conv_fit)

    print("\n\n-------------------------------------------------\n\n")
    
    tof_cost =  0.5 * (T13 + T23 )
    p0 = [0.2, len(tof_cost),  tof_cost.mean() , 4., tof_cost.mean(), 0.9]
    bounds = (0.1, 0., tof_cost.mean()*0.7, 1., tof_cost.mean()*0.7 , 0.3 ), (0.4, numpy.inf, tof_cost.mean()*1.3, 6., tof_cost.mean()*1.3, 1.)

    title = '%s cm , %d eventi %d secondi, %s' % (position, len(tof_cost), t_run, date)
    figlabel = position + 'cm'
    opt_true, pcov_true = plot_functions.fit2gauss(tof_cost, "$(T_{13}+T_{23})*0.5[ns]$",  "entries/bin", bins = data_bins, range = data_range, f = True, p0= p0, bounds = bounds, title = title)
    if save_fig ==True:
      plt.savefig('dati_risoluzione/plot/tof_costant_%s.pdf' % figlabel, format = 'pdf')    
    
    param_2gauss_fit = utilities.make_opt_string(opt_true, pcov_true, s = string_x_n)
    print(param_2gauss_fit)      

    with open("TOF_cost.txt", "a") as output_file:
        output_file.write(param_2gauss_fit)
 
    print("\n\n---------------------------------------------------\n\n")

    T12 = T13 - T23 
    
    p0 = [0.2, len(T12),  T12.mean() , 4., T12.mean(), 0.9]    
    bounds = (0.1, 0., T12.mean()-2, 1., T12.mean()-2 , 0.3 ), (0.4, numpy.inf, T12.mean()+2, 6., T12.mean()+2, 1.)



    title = '%s cm , %d eventi %d secondi, %s' % (position, len(tof_cost), t_run, date)
    figlabel = position + 'cm'
    opt_true, pcov_true = plot_functions.fit2gauss(T12, "$(T_{13}-T_{23}) [ns]$",  "entries/bin", bins = data_bins, range = (-30., +30), f = True, p0= p0, bounds = bounds, title = title)
    if save_fig ==True:
      plt.savefig('dati_risoluzione/plot/T12_%s.pdf' % figlabel, format = 'pdf')    

    param_2gauss_fit = utilities.make_opt_string(opt_true, pcov_true, s = string_x_n)      
    print(param_2gauss_fit)

    with open("T12.txt", "a") as output_file:
        output_file.write(param_2gauss_fit)
 
    #plt.ion()
    #plt.show()   
    
