import numpy
from matplotlib import pyplot as plt

#gaussiana
def gauss(x, norm, mean, sigma): 
  return norm * numpy.exp(-0.5 * ((x - mean)/sigma )**2)
  
def res_function(x, a, norm, mean1, sigma1, mean2, sigma2):
  return a * gauss(x, norm, mean1, sigma1) + \
         (1.-a) * gauss(x, norm, mean2, sigma2)

  
def plot_resolution(data, *plot_positions, x_grid=None, figname=None, title=None):
    """
    """
    positions = data[:, 0]
    fig = plt.figure(figname)
    if x_grid is None:
        x_grid = numpy.linspace(-4., 4., 1000)
    fmts = ['--', '-', '-.']
    for i, p in enumerate(plot_positions):
        _mask = (positions == p)
        params = data[_mask][0][2:8]
        y = res_function(x_grid, *params)
        plt.plot(x_grid, y, fmts[i], label='x=%.2f' % p)
    plt.xlabel("$T_{meas} - T_{true}$ [ns]", fontsize=14)    
    plt.ylabel("a.u.", fontsize=14)    
    plt.yticks(fontsize=14, rotation=0)
    plt.xticks(fontsize=14, rotation=0) 
    plt.subplots_adjust(bottom = 0.13, left = 0.15)  
    plt.legend()
    if title is not None:
        plt.title(title)
    return fig

if __name__ == '__main__':
    """
    """
    t13_fit_data = numpy.loadtxt('T13_conv.txt', unpack=False)
    t23_fit_data = numpy.loadtxt('T23_conv.txt', unpack=False)
    plot_positions = (10, 140, 260)
    plot_resolution(t13_fit_data, *plot_positions, figname='T13',
                    title='Funzione di risoluzione $\Delta t_{13}$')
    plot_resolution(t23_fit_data, *plot_positions, figname='T23',
                    title='Funzione di risoluzione $\Delta t_{23}$')
    plt.ion()
    plt.show()
