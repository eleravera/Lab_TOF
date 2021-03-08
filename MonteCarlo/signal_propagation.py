import numpy
import matplotlib.pyplot as plt

import geometry

"""Propagazione dei fotoni dentro lo scintillatore """
def DT_12(x_s1, delay): 
  T_r = (geometry.X1 - x_s1) * (10**9) / geometry.v_gamma #[ns]
  T_l = x_s1 * (10**9) / geometry.v_gamma #[ns]
  DT_12 = numpy.abs(T_r - T_l) + delay
  
  #plt.figure("Delta t PM1 and 2")
  #plt.hist(DT_12 * 10**9)
  #plt.xlabel("DT_12 [ns]")
  return T_l, T_r, DT_12
  
  
def DT_13(x_s1, x_s3, delay, beta): 
  T_l1 = x_s1 * (10**9) / geometry.v_gamma #[ns]
  T_l3 = x_s3 * (10**9)/ geometry.v_gamma #[ns] 
  TOF = (numpy.sqrt((x_s1-x_s3)**2 + geometry.h_13**2) * (10**9) / (beta*geometry.c)) #[s]
  DT_13 = T_l3 + delay + TOF - T_l1
  
  print("Tl1", T_l1)
  print("Tl3", T_l3)
  print("TOF", TOF)  
  print("delay ", delay)
  
  
  return TOF, DT_13
