import numpy
from scipy.interpolate import interp1d

#Retta
def line(x, m , q):
  return m * x +q

def proportional(x, m ):
  return m * x


def costant(x,  q): 
  q = numpy.ones(len(x))*q
  return q



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
def create_convolution(pdf1, pdf2, mode='same'):
    def convolved_fit_function(x, *args):
        x_grid = numpy.linspace(min(x), max(x), 1000)
        y_grid = numpy.convolve(pdf1(x_grid), pdf2(x_grid, *args), mode=mode)
        spline = interp1d(x_grid, y_grid, kind='linear') 
        return spline(x)
    return convolved_fit_function
