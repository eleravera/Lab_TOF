
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import plot_functions
import fit_functions
import utilities

#T13 vs x
input_file = 'risoluzione/T13_2gauss.txt'
x, n, fraction, norm, mean1, sigma1, mean2, sigma2, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)

opt, pcov = plot_functions.line_fit(x, mean2, sigma2/numpy.sqrt(n),  "x [cm]", "$T_{13}[ns]$" , title = '$T_{13}$ vs x')
param_from_fit = utilities.make_opt_string(opt, pcov, s = 'T13 vs x: ')
print(param_from_fit)
print("\nVelocità della luce: %s +- %s\n" %(1/opt[0], numpy.sqrt(pcov[0][0])/opt[0]**2))

print("\n\n----------------------------------------\n\n")

#T23 vs x
input_file = 'risoluzione/T23_2gauss.txt'
x, n, fraction, norm, mean1, sigma1, mean2, sigma2, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)

opt, pcov = plot_functions.line_fit(x, mean2, sigma2/numpy.sqrt(n),  "x [cm]", "$T_{23}[ns]$", title = '$T_{23}$ vs x' )
param_from_fit = utilities.make_opt_string(opt, pcov, s = 'T13 vs x: ')
print(param_from_fit)
print("\nVelocità della luce: %s +- %s\n" %(1/opt[0], numpy.sqrt(pcov[0][0])/opt[0]**2))

print("\n\n----------------------------------------\n\n")


#Risoluzione misura di T13 e T23
input_file = 'risoluzione/T13_conv.txt'
x, n_13, fraction, norm, mean1_13, sigma1_13, mean2_13, sigma2_13, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)


input_file = 'risoluzione/T23_conv.txt'
x, n_23, fraction, norm, mean1_23, sigma1_23, mean2_23, sigma2_23, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)

plt.figure()
plt.subplot(2, 1, 1)
plt.errorbar(x, mean1_13, yerr= sigma1_13/numpy.sqrt(n_13), fmt = '.r', label = '$\mu_{1}$ $T_{13}$')
plt.errorbar(x, mean1_23, yerr= sigma1_23/numpy.sqrt(n_23), fmt = '.b', label = '$\mu_{1}$ $T_{23}$')
plot_functions.set_plot('x [cm]', 'mean', title = '')

plt.subplot(2, 1, 2)
plt.errorbar(x, mean2_13, yerr= sigma2_13/numpy.sqrt(n_13), fmt = '.r', label = '$\mu_{2}$ $T_{13}$')
plt.errorbar(x, mean2_23, yerr= sigma2_23/numpy.sqrt(n_23), fmt = '.b', label = '$\mu_{2}$ $T_{13}$')
plot_functions.set_plot('x [cm]', 'mean', title = '')


#Tof cost vs x 
input_file = 'risoluzione/TOF_cost.txt'
x, n, fraction, norm, mean1, sigma1, mean2, sigma2, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)
opt, pcov = plot_functions.line_fit(x, mean2, sigma2/numpy.sqrt(n),  "x [cm]", "$Tof cost[ns]$", title = '$Tof cost$ vs x' )


print("\n\n----------------------------------------\n\n")

#T12 vs x
input_file = 'risoluzione/T12.txt'
x, n, fraction, norm, mean1, sigma1, mean2, sigma2, dfraction, dnorm, dmean1, dsigma1, dmean2, dsigma2  = numpy.loadtxt(input_file, unpack = True)
opt, pcov = plot_functions.line_fit(x, mean2, sigma2/numpy.sqrt(n),  "x [cm]", "$T12[ns]$", title = '$T12$ vs x' )



plt.ion()
plt.show()
