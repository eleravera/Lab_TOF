import numpy
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import fit_functions
import geometry

def acquisition_duration(t):
    Delta_t = numpy.ediff1d(t)
    mask_restart = Delta_t < 0.
    t_run = t[len(t)-1] - t[0] +  numpy.sum(mask_restart) * 6553.6
    print("\n%d events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) ) 
    return t_run  
    
    
    
def decimal_places(val):
    """Calculate the number of decimal places so that a given value is rounded
    to exactly two signficant digits.

    Note that we add epsilon to the argument of the logarithm in such a way
    that, e.g., 0.001 is converted to 0.0010 and not 0.00100. For values greater
    than 99 this number is negative.
    """
    return 1 - int(numpy.log10(val + sys.float_info.epsilon)) + 1 * (val < 1.)


def decimal_power(val):
    """Calculate the order of magnitude of a given value,i.e., the largest
    power of ten smaller than the value.
    """
    return int(numpy.log10(val + sys.float_info.epsilon)) - 1 * (val < 1.)


def format_value_error(value, error, pm='+/-', max_dec_places=6):
    """Format a measurement with the proper number of significant digits.
    """
    value = float(value)
    error = float(error)
    if not numpy.isnan(error):
        assert error >= 0
    else:
        return '%s %s nan' % (format_value(value), pm)
    if error == 0 or error == numpy.inf:
        return '%e' % value
    dec_places = decimal_places(error)
    if dec_places >= 0 and dec_places <= max_dec_places:
        fmt = '%%.%df %s %%.%df' % (dec_places, pm, dec_places)
    else:
        p = decimal_power(abs(value))
        scale = 10 ** p
        value /= scale
        error /= scale
        dec_places = decimal_places(error)
        if dec_places > 0:
            if p > 0:
                exp = 'e+%02d' % p
            else:
                exp = 'e-%02d' % abs(p)
            fmt = '%%.%df%s %s %%.%df%s' %\
                  (dec_places, exp, pm, dec_places, exp)
        else:
            fmt = '%%d %s %%d' % pm
    return fmt % (value, error)


def TAC_scale(ch0, ch1, scale = 200): 
  T23 = ch1
  T13 = ch0

  t23 = T23 * scale/10 #[ns]
  t13 = T13 * scale/10 #[ns]

  #mask_t13 = t13 > 2.
  #mask_t23 = t23 > 2.
  #mask = mask_t13 * mask_t23
  T13 = t13#[mask]
  T23 = t23#[mask]
  #print("Numero di eventi con Ti3 < 3ns:", numpy.sum(mask))
  
  return T13, T23

def rate_and_saturation(t, ch0, ch1): 
#Calcola il rate degli eventi
  Delta_t = numpy.ediff1d(t)
  mask_t = Delta_t < 0
  t_run = t.max() -t.min() +  numpy.sum(mask_t) * 6553.6

  print("Il clock dell'FPGA è ripartito %d volte durante l'acquisizione:" % numpy.sum(mask_t) )
  print("\n%d Events recorded in %f s\nRate: %f Hz\n" % (len(t), t_run, len(t)/t_run) )

  #Cotrolla se ci sono eventi che hanno saturato l'FPGA
  saturation_ch0_mask = ch0 > 3.2
  saturation_ch1_mask = ch1 > 3.2

  print("Rate di eventi sopra soglia sul ch0:", numpy.sum(saturation_ch0_mask)/t_run)
  print("Rate di eventi sopra soglia sul ch1:", numpy.sum(saturation_ch1_mask)/t_run)
  print("Frazione di eventi sopra soglia: %f., %f.\n\n" % (numpy.sum(saturation_ch0_mask)/len(t), numpy.sum(saturation_ch1_mask)/len(t)))
  return 
  
  
def make_opt_string(opt, pcov, s = '', s_f = ''):
  numpy.set_printoptions(linewidth=numpy.inf, precision=5)
  opt_err = numpy.sqrt(pcov.diagonal())
  array_str = numpy.array_str(numpy.concatenate((opt, opt_err)) )
  array_str = array_str.strip('[]')  
  string = s + ' ' + array_str + s_f + '\n'
  return string  
  
  
def read_parameter(input_file1, input_file2):   
 
    m, q, dm, dq, c, dc  = numpy.loadtxt(input_file1, unpack = True)
    a, b, da, db = numpy.loadtxt(input_file2, unpack = True)  
    weights = 1/dm**2  
    average_m = sum(a * weights) / sum(weights)
    daverage_m = numpy.sqrt(dm[0]**2 + dm[1]**2 )
    
    #x = numpy.linspace(-10., 300., 1000)
    #costant = fit_functions.line(x, a[0], b[0])
    costant = 17.24 #da definire in funzione di x 
     
    #tau13 = q[0]
    #tau23 = m[1] * geometry.X1 * 100 + q[1]   
    
    tau_diff = q[1]-q[0]#tau23 - tau13    

    return average_m, daverage_m , costant, tau_diff
  
  
  

