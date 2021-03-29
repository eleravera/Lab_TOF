
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import numpy
import geometry


#Data la velocità e la posizioni di partenza del muone sullo scintillatore 1 e di arrivo sullo scintillatore 3 calcola il tempo di volo (ns)
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
    res = resolution(len(x_s1)) 
  Delta_T = (T_r - T_l) * (10**9) #[ns]
  DT_12 = Delta_T + delay + res
  return DT_12
  
#Calcola la differenza di tempo tra l'arrivo del segnale nel PMT1 e nel PMT3 (il ritardo si applica al PMT3)
def DT_13(x_s1, x_s3, delay, TOF, res = None): 
  T_l1 = x_s1  / geometry.v_gamma 
  T_l3 =  0.#x_s3 * (10**9)/ geometry.v_gamma 
  if (res is None):
    res = resolution(len(x_s1)) 
  Delta_T = (T_l3 - T_l1) * (10**9) #[ns]   
  DT_13 = Delta_T + delay + TOF + res

  return DT_13
  
#Calcola la differenza di tempo tra l'arrivo del segnale nel PMT2 e nel PMT3 (il ritardo si applica al PMT3) 
def DT_23(x_s1, x_s3, delay, TOF, res = None): 
  T_l2 = (geometry.X1 - x_s1)  / geometry.v_gamma 
  T_l3 =  0.#x_s3 * (10**9)/ geometry.v_gamma 
  if (res is None):
    res = resolution(len(x_s1)) 
  Delta_T = (T_l3 - T_l2) * (10**9) #[ns]     
  DT_23 = Delta_T + delay + TOF + res
  return DT_23
  

#Genera un numero casuale con distribuzione gaussiana con media 0 e sigma 1 ns, da applicare poi ad ogni segnale per simulare la risoluzione
def gauss_resolution(N):
  sigma_t = numpy.random.normal(0., 1., N)
  return sigma_t   
  

def double_gauss_resolution(N):







  return sigma_t 

  
  
