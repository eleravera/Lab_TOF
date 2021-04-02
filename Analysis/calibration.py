
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import plot_functions
import fit_functions
import utilities
import geometry

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--write_output_file', '-f', default=False, type=bool, help='')
options_parser.add_argument('--save_fig', '-p', default=False, type=bool, help='')

if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    write_output_file = options['write_output_file']
    save_fig = options['save_fig']
    
    x, sigma_x  = numpy.loadtxt('vecchie/Delta_x.txt', unpack = True)
           
    #T13 vs x
    input_file = 'vecchie/T13_2gauss.txt'
    x, n_13, fraction, norm, mean1_13, sigma1_13, mean2_13, sigma2_13, dfraction, dnorm, dmean1, dsigma1, dmean2_13, dsigma2  = numpy.loadtxt(input_file, unpack = True)
    
    c_preliminary = geometry.v_gamma * 10**-7
    sigma =  numpy.sqrt(dmean2_13**2 + (sigma_x/c_preliminary)**2 )
    opt, pcov = plot_functions.line_fit(x, mean2_13,  "x [cm]", "$T_{13}[ns]$" , dy = dmean2_13, dx = sigma_x, err_fit = sigma, title = '$T_{13}$ vs x')
    c = '  %s  %s' % (1/opt[0], numpy.sqrt(pcov[0][0]/(opt[0])**2))
    param_from_fit_T13 = utilities.make_opt_string(opt, pcov, s_f = c)
    print(param_from_fit_T13)

    if save_fig ==True:
      plt.savefig('vs_x/T13_vs_x.pdf', format = 'pdf') 

    print("\n----------------------------------------\n")

    #T23 vs x
    input_file = 'vecchie/T23_2gauss.txt'
    x, n_23, fraction, norm, mean1_23, sigma1_23, mean2_23, sigma2_23, dfraction, dnorm, dmean1, dsigma1, dmean2_23, dsigma2  = numpy.loadtxt(input_file, unpack = True)


    c_preliminary = geometry.v_gamma * 10**7
    sigma =  numpy.sqrt(dmean2_23**2 + (c_preliminary*sigma_x)**2 )
    opt, pcov = plot_functions.line_fit(x, mean2_23,  "x [cm]", "$T_{23}[ns]$", dy = dmean2_23, dx = sigma_x,  err_fit = sigma, title = '$T_{23}$ vs x' )
    opt[1] = fit_functions.line(280., *opt) 
    c = '  %s  %s' % (1/opt[0], numpy.sqrt(pcov[0][0]/(opt[0])**2))
    param_from_fit_T23 = utilities.make_opt_string(opt, pcov, s_f = c)    
    print(param_from_fit_T23)
    
    if save_fig ==True:
      plt.savefig('vs_x/T23_vs_x.pdf', format = 'pdf')    
      
    print("\n----------------------------------------\n")

    #Risoluzione misura di T13 e T23
    input_file = 'vecchie/T13_conv.txt'
    x, n_13, fraction, norm, mean1_13, sigma1_13, mean2_13, sigma2_13, dfraction, dnorm, dmean1_13, dsigma1_13, dmean2_13, dsigma2_13  = numpy.loadtxt(input_file, unpack = True)


    input_file = 'vecchie/T23_conv.txt'
    x, n_23, fraction, norm, mean1_23, sigma1_23, mean2_23, sigma2_23, dfraction, dnorm, dmean1_23, dsigma1_23, dmean2_23, dsigma2_23  = numpy.loadtxt(input_file, unpack = True)

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.errorbar(x, mean1_13, yerr= dmean1_13, fmt = '.r', label = '$\mu_{1}$ $T_{13}$')
    plt.errorbar(x, mean2_13, yerr= dmean2_13, fmt = '.b', label = '$\mu_{2}$ $T_{13}$')
    
    plot_functions.set_plot('x [cm]', '$\mu(T_{13})$', title = '')

    plt.subplot(2, 1, 2)
    plt.errorbar(x, mean1_23, yerr= dmean1_23, fmt = '.r', label = '$\mu_{1}$ $T_{23}$')
    plt.errorbar(x, mean2_23, yerr= dmean2_23, fmt = '.b', label = '$\mu_{2}$ $T_{23}$')
    plot_functions.set_plot('x [cm]', '$\mu(T_{23})$', title = '')

    if save_fig ==True:
      plt.savefig('vs_x/resolution_vs_x.pdf', format = 'pdf')    
      
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.errorbar(x, sigma1_13, yerr = dsigma1_13, fmt = '.r', label = '$\sigma_{1}$ $T_{13}$')
    plt.errorbar(x, sigma2_13, yerr = dsigma2_13, fmt = '.b', label = '$\sigma_{2}$ $T_{13}$')
    
    plot_functions.set_plot('x [cm]', '$\sigma_(T_{13})$', title = '')

    plt.subplot(2, 1, 2)
    plt.errorbar(x, sigma1_23, yerr = dsigma1_23 , fmt = '.r', label = '$\sigma_{1}$ $T_{23}$')
    plt.errorbar(x, sigma2_23, yerr = dsigma2_23 , fmt = '.b', label = '$\sigma_{2}$ $T_{23}$')
    plot_functions.set_plot('x [cm]', '$\sigma_(T_{23})$', title = '')

    if save_fig ==True:
      plt.savefig('vs_x/sigma_vs_x.pdf', format = 'pdf')          
      
      

    #Tof cost vs x     
   
    input_file = 'vecchie/TOF_cost.txt'
    x, n, fraction, norm, mean1, sigma1, mean2, sigma2, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)
    sigma =  numpy.sqrt(dmean2**2 + (sigma_x*1.01033e-03)**2 )
    opt, pcov = plot_functions.line_fit(x, mean2, "x [cm]", "$(T_{13}+T_{23})0.5[ns]$", dy = dmean2, dx = sigma_x, err_fit=sigma,  title = '$(T_{13}+T_{23})0.5$ vs x' )
    param_from_fit_Tsum = utilities.make_opt_string(opt, pcov)
    print(param_from_fit_Tsum)

    if save_fig ==True:
      plt.savefig('vs_x/Tsum_vs_x.pdf', format = 'pdf')    

    print("\n----------------------------------------\n")


    #T12 vs x
    
    input_file = 'vecchie/T12.txt'
    x, n, fraction, norm, mean1, sigma1, mean2, sigma2, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)
   
    sigma =  numpy.sqrt(dmean2**2 + (sigma_x*1.28916e-01)**2 )
    opt, pcov = plot_functions.line_fit(x, mean2,"x [cm]", "$T_{13}-T_{23}[ns]$", dy = dmean2, dx = sigma_x, err_fit = sigma, title = '$T_{13}-T_{23}$ vs x' )

    param_from_fit_Tdiff = utilities.make_opt_string(opt, pcov)
    print(param_from_fit_Tdiff)
    
    if save_fig ==True:
      plt.savefig('vs_x/Tdiff_vs_x.pdf', format = 'pdf')    
      
      
    if write_output_file ==True:
    
      header = '# T13,23, m[ns/cm], q[ns], dm, dq, 1/m[cm/ns], d1/m \n'
      with open("vs_x/T13_T23_vs_x.txt", "a") as output_file:
          output_file.write(header)    
    
      with open("vs_x/T13_T23_vs_x.txt", "a") as output_file:
          output_file.write(param_from_fit_T13)
      with open("vs_x/T13_T23_vs_x.txt", "a") as output_file:
          output_file.write(param_from_fit_T23)
      
      header = '# Tsum,diff, m[ns/cm], q[ns], dm, dq \n'
      with open("vs_x/Tsum_Tdiff_vs_x.txt", "a") as output_file:
          output_file.write(header)
          
      with open("vs_x/Tsum_Tdiff_vs_x.txt", "a") as output_file:
          output_file.write(param_from_fit_Tsum)
      with open("vs_x/Tsum_Tdiff_vs_x.txt", "a") as output_file:
          output_file.write(param_from_fit_Tdiff)

    plt.ion()
    plt.show()
