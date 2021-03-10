import numpy

import geometry

def Time_Of_Flight(x_s1, x_s3, beta):
  TOF = (numpy.sqrt((x_s1-x_s3)**2 + (geometry.Z1/2+geometry.Z3/2 + geometry.h_13)**2) * (10**9) / (beta*geometry.c)) #[s] geometry.h_13**2
  return TOF

"""Propagazione dei fotoni dentro lo scintillatore """
def DT_12(x_s1, delay): 
  T_r = (geometry.X1 - x_s1) * (10**9) / geometry.v_gamma #[ns]
  T_l = x_s1 * (10**9) / geometry.v_gamma #[ns]
  DT_12 = T_r - T_l + delay
  return T_l, T_r, DT_12
  
  
def DT_13(x_s1, x_s3, delay, beta): 
  T_l1 = x_s1 * (10**9) / geometry.v_gamma #[ns]
  T_l3 =  0.#x_s3 * (10**9)/ geometry.v_gamma #[ns] 
  TOF = Time_Of_Flight(x_s1, x_s3, beta )
  DT_13 = T_l3 + delay + TOF - T_l1
  return DT_13
  
  
 
def DT_23(x_s1, x_s3, delay, beta): 
  T_l2 = (geometry.X1 - x_s1) * (10**9) / geometry.v_gamma #[ns]
  T_l3 =  0.#x_s3 * (10**9)/ geometry.v_gamma #[ns] 
  TOF = Time_Of_Flight(x_s1, x_s3, beta )
  DT_23 = T_l3 + delay + TOF - T_l2
  
  print("Tl2", T_l2)
  print("Tl3", T_l3)  
  return DT_23
  
