import numpy as np
from scipy.optimize import curve_fit
from util import read_file
from functions import absolute_value_list



'''
    Function name:      calculate_blank_parameters
    Input parameters:   Blank test text file (blank.txt)
    Return parameters:  Constants for allometric fuctions fitted to the blank test information
    Description:        This function will use the blank test, if one is provided, to calculate allometric constants
                        (y = ax**b) at this is the equation that best fits the displacement versus force curve (see readme.txt
                        for more information). If a blank test is not provided, standard contanst will be used.
    Required library:   numpy
    Required funcs:     read_file, absolute_value_list, allometric_fit
'''
def calculate_blank_parameters(blank):
    if blank == 'none':
        allometric_a = 0.0357
        allometric_b = 0.4701
    else:
        time_blank, force_blank, disp_blank = read_file(blank)
        xdata = np.array(absolute_value_list(force_blank))
        ydata = np.array(absolute_value_list(disp_blank))
        allometric_a, allometric_b, r_squared = allometric_fit(xdata, ydata)
    return allometric_a, allometric_b



'''
    Function name:      allometric_func
    Input parameters:   x = list, a = multiplication constant, b = exponent constant
    Return parameters:  returns y of y = ax**b
'''
def allometric_func(x, a, b):
    return a * x**b



'''
    Function name:      allometric_fit
    Input parameters:   x_data = list of x value data to be fit to allometric function (typically be force values of the
                        blank test)
                        y_data = list of y value data to be fit to allometric function (typically the displacement values of
                        the blank test)
    Return parameters:  p1 = multiplication constant of allometric function
                        p2 = exponent constant of allometric function
                        r_squared = degree of fit of the allometric function
    Required library:   scipy, numpy
    Required funcs:     allometric_func
'''
def allometric_fit(xdata, ydata):
    popt, pcov = curve_fit(allometric_func, xdata, ydata)
    p1 = popt[0]
    p2 = popt[1]
    residuals1 = ydata - allometric_func(xdata, p1, p1)
    ss_res = sum(residuals1 ** 2)
    ss_tot = sum((ydata - np.mean(ydata)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return p1, p2, r_squared
