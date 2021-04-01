import numpy
import argparse

import utilities

__description__ = 'Parse a data file containing both values and their '\
                  'uncertainties and properly round them up to their'\
                  'significant digits.'
parser = argparse.ArgumentParser(description=__description__)
parser.add_argument('infile', type=str, help='path to the input file')
parser.add_argument('--output-file-path', '-o', type=str,
                    help='path to the output file')
parser.add_argument('--separator', type=str, default=' ',
                   help='column separator')
parser.add_argument('--terminator', type=str, default='\n',
                   help='row terninator')



def parse_row(row, column_dict, separator=' ', terminator='\n', **fmt_opts):
    """
    """
    formatted = []
    for name, (val_pos, err_pos) in column_dict.items():
        val, err = row[val_pos], row[err_pos]
        formatted.append(utilities.format_value_error(val, err, **fmt_opts))
    return separator.join(formatted) + terminator


def header_line(column_dict, start='# ', separator=' ', terminator='\n'):
    """
    """
    middle = separator.join([name for name in column_dict])
    return '{}{}{}'.format(start, middle, terminator)
    

def format_input_file(input_file_path, column_dict, output_file_path=None,
                      separator=' ', terminator='\n', header_start='# ', 
                      **fmt_opts):
    """ The input dictionary must contain the name of the parameters as keys 
    and tuples of two indices as values: the position of the
    value column and the position of the uncertainty column in the data array.
    """
    data = numpy.loadtxt(input_file_path, unpack=False)
    if output_file_path is None:
        output_file_path = input_file_path.replace('.txt', '_formatted.txt')
    if output_file_path.endswith('tex'):
        separator = ' & '
        terminator = '\\\ \n' # We need three backslash to get two in the file
        header_start = ''
        fmt_opts['pm'] = '\pm'
    with open(output_file_path, 'w') as outfile:
        outfile.write(header_line(column_dict, separator=separator,
                      terminator=terminator, start=header_start))
        for i in range(len(data)):
            outfile.write(parse_row(data[i, :], column_dict,
                          separator=separator, terminator=terminator,
                          **fmt_opts))


if __name__ == '__main__':
    """
    """
    args = vars(parser.parse_args())
    COLUMN_DICT = {'fraction'      : (2, 8),
                   'normalization' : (3, 9),
                   'mean_1'        : (4, 10),
                   'sigma_1'       : (5, 11),
                   'mean_2'        : (6, 12),
                   'sigma_2'       : (7, 13)
                  }
    input_file_path = args.pop('infile')
    format_input_file(input_file_path, COLUMN_DICT, **args)
                  
