
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import numpy
from scipy.integrate import quad
from scipy.interpolate import interp1d

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
  if (res is None):
    res = resolution(len(x_s1), fit_functions.two_gauss,  1.98e-01, 1.068e+02, 0. , 1.74483e+00, 0.3856, 4.95658e-01 ) 
  Delta_T = (T_r - T_l) * (10**9) #[ns]
  DT_12 = Delta_T + delay + res
  return DT_12
  
#Calcola la differenza di tempo tra l'arrivo del segnale nel PMT1 e nel PMT3 (il ritardo si applica al PMT3)
def DT_13(x_s1, x_s3, delay, TOF, res = None): 
  T_l1 = x_s1  / geometry.v_gamma 
  T_l3 =  0.#x_s3 * (10**9)/ geometry.v_gamma 
  if (res is None):
    res = resolution(len(x_s1), fit_functions.two_gauss,  1.98e-01, 1.068e+02, 0. , 1.74483e+00, 0.3856, 4.95658e-01 ) 
  Delta_T = (T_l3 - T_l1) * (10**9) #[ns]   
  DT_13 = Delta_T + delay + TOF + res

  return DT_13
  
#Calcola la differenza di tempo tra l'arrivo del segnale nel PMT2 e nel PMT3 (il ritardo si applica al PMT3) 
def DT_23(x_s1, x_s3, delay, TOF, res = None): 
  T_l2 = (geometry.X1 - x_s1)  / geometry.v_gamma 
  T_l3 =  0.#x_s3 * (10**9)/ geometry.v_gamma 
  if (res is None):
    res = resolution(len(x_s1), fit_functions.two_gauss, 1.98e-01, 1.068e+02, 0. , 1.74483e+00, 0.3856, 4.95658e-01  )
  Delta_T = (T_l3 - T_l2) * (10**9) #[ns]     
  DT_23 = Delta_T + delay + TOF + res
  return DT_23
  

#Genera un numero casuale con distribuzione gaussiana con media 0 e sigma 1 ns, da applicare poi ad ogni segnale per simulare la risoluzione
def gauss_resolution(N, sigma):
  resolution = numpy.random.normal(0., sigma, N)
  return resolution   
  

def resolution(N, pdf, *args ):
  dt = numpy.linspace(-5., 5., 1000)
  cdf_y  = numpy.zeros(N)
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


