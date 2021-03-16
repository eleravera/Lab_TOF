import numpy

#Retta
def line(x, m , q):
  return m * x +q

#Gaussiana
def gauss(x, norm, mean, sigma): 
  return (norm) * numpy.exp(-0.5 * ((x - mean)/sigma )**2)
  
#Doppia gaussiana
def two_gauss(x, a, norm, mean1, sigma1, mean2, sigma2):
  return a * gauss(x, norm, mean1, sigma1) + (1.-a) * gauss(x, norm, mean2, sigma2)

#Esponenziale
def exponential(x, a, m): 
  return a * numpy.exp(-x * m)

#Convoluzione di due pdf
def create_convolution(pdf1, pdf2):
    
    def convolved_fit_function(x, *args):
        return numpy.convolve(pdf1(x), pdf2(x, *args), mode='same') 
    
    return convolved_fit_function  
