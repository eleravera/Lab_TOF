
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import numpy
from scipy.integrate import quad
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

import geometry
import fit_functions

#time of flight vero
def Time_Of_Flight(x_s1, x_s3, y_s1, y_s3, z12, beta):
  dx = x_s1 - x_s3
  dy = y_s1 - y_s3
  dz = (geometry.Z1 + geometry.Z3)*0.5 + z12  
  TOF = numpy.sqrt(dx**2 + dz**2) / (beta*geometry.c)
  TOF = TOF * (10**9) #[ns]
  return TOF

#Calcola la differenza di tempo tra l'arrivo del segnale nel PMT1 e nel PMT2 (il ritardo si applica al PMT2)
def DT_12(x_s1, delay, res = None): 
  T_r = (geometry.X1 - x_s1) / geometry.v_gamma 
  T_l = x_s1 / geometry.v_gamma 
  #if (res is None):
  #  res = resolution(len(x_s1), fit_functions.two_gauss,  1.98e-01, 1.068e+02, 0. , 1.74483e+00, 0.3856, 4.95658e-01 ) 
  
  
  
  Delta_T = (T_r - T_l) * (10**9) #[ns]
  DT_12 = Delta_T + delay + res
  return DT_12
  
#Calcola la differenza di tempo tra l'arrivo del segnale nel PMT1 e nel PMT3 (il ritardo si applica al PMT3)
def DT_13(x_s1, x_s3, y_s3, delay, TOF, res = None): 
  T_l1 = x_s1  / geometry.v_gamma 
  T_l3 =  (geometry.s3_y + geometry.Y3 - y_s3) / geometry.v_gamma  
  if (res is None):
    res = numpy.zeros(len(x_s1))   
    x, n, frac, norm, mean1, sigma1, mean2, sigma2, dfrac, dnorm, dmean1, dsigma1, dmean2, dsigma2 = numpy.loadtxt('risoluzione/simulazioni/vecchie/T13_conv.txt', unpack = True)
    x_s1 = x_s1 * 100
    mask = (x_s1 > 0. ) * (x_s1 < 40. )
    res[mask] = resolution(len(x_s1[mask]), fit_functions.two_gauss,  frac[0], norm[0], mean1[0], sigma1[0], mean2[0], sigma2[0])
    mask = (x_s1 > 230. ) * (x_s1 < 270. )
    res[mask] = resolution(len(x_s1[mask]), fit_functions.two_gauss,  frac[6], norm[6], mean1[6], sigma1[6], mean2[6], sigma2[6])
    for i in range (1, len(x)-1) :
      mask = (x_s1 > (x[i-1] + x[i]) * 0.5 ) * (x_s1 < (x[i+1] + x[i]) * 0.5 )
      res[mask] = resolution(len(x_s1[mask]), fit_functions.two_gauss,  frac[i], norm[i], mean1[i], sigma1[i], mean2[i], sigma2[i])  
    plt.figure()
    plt.hist(res)       
  Delta_T = (T_l3 - T_l1) * (10**9) #[ns]   
  DT_13 = Delta_T + delay + TOF + res
  return DT_13, res
  
#Calcola la differenza di tempo tra l'arrivo del segnale nel PMT2 e nel PMT3 (il ritardo si applica al PMT3) 
def DT_23(x_s1, x_s3, y_s3, delay, TOF, res = None): 
  T_l2 = (geometry.X1 - x_s1)  / geometry.v_gamma 
  T_l3 =  (geometry.s3_y + geometry.Y3 - y_s3) / geometry.v_gamma  
  if (res is None):
    x_s1 = x_s1 * 100
    res = numpy.zeros(len(x_s1))   
    x, n, frac, norm, mean1, sigma1, mean2, sigma2, dfrac, dnorm, dmean1, dsigma1, dmean2, dsigma2 = numpy.loadtxt('risoluzione/simulazioni/vecchie/T23_conv.txt', unpack = True)
    mask = (x_s1 > 0. ) * (x_s1 < 40. )
    res[mask] = resolution(len(x_s1[mask]), fit_functions.two_gauss,  frac[0], norm[0], mean1[0], sigma1[0], mean2[0], sigma2[0])
    mask = (x_s1 > 230. ) * (x_s1 < 270. )
    res[mask] = resolution(len(x_s1[mask]), fit_functions.two_gauss,  frac[6], norm[6], mean1[6], sigma1[6], mean2[6], sigma2[6])
    for i in range (1, len(x)-1) :
      mask = (x_s1 > (x[i-1] + x[i]) * 0.5 ) * (x_s1 < (x[i+1] + x[i]) * 0.5 )
      res[mask] = resolution(len(x_s1[mask]), fit_functions.two_gauss,  frac[i], norm[i], mean1[i], sigma1[i], mean2[i], sigma2[i]) 
  Delta_T = (T_l3 - T_l2) * (10**9) #[ns]   
  DT_23 = Delta_T + delay + TOF + res
  return DT_23, res
  

#Genera un numero casuale con distribuzione gaussiana con media 0 e sigma = sigma ns
def gauss_resolution(N, sigma):
  resolution = numpy.random.normal(0., sigma, N)
  return resolution   
  

def resolution(N, pdf, *args ):
  dt = numpy.linspace(-5., 5., 1000)
  cdf_y  = numpy.zeros(len(dt))
  for i in range(len(dt)):
    y, rest = quad(pdf, dt[0], dt[i], args = args)  
    cdf_y[i] = y 
  cdf_y, unique_indices = numpy.unique(cdf_y, return_index=True)
  cdf_y /= cdf_y[-1]
  dt = dt[unique_indices] 
  funzione = interp1d(cdf_y, dt)
  x = numpy.random.uniform(0., 1., N)
  res = funzione(x)
  return res 


