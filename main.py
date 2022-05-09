import pandas as pd
import csv
from math import pi
from openpyxl import load_workbook
from functions import convert_file_to_list, column_calculations, specific_energy_calc
from util import get_sample_info, read_file, write_to_file, get_args
from blanktest import calculate_blank_parameters


'''
This program calculates the corrected displacement data, specific energy, and compression ratio of a piston die press test. A piston die press test
is used to measure the compression and compaction behaviour of soils, rocks, and other powdered material.  
The inputs are: 
    1. Raw text files from the piston die press test machine
    2. Excel file containing sample information 
More information regarding the setup of these files can be found in the associated readme.txt file.

This code was written using Python 3.7 by Erin Furnell.
'''


#User input of excel file name (excel file must contain sample information)
excel_name = get_args()

#Reads sample information in the excel file into relevant python lists
file_list, mass_list, blank_test, initial_depth, final_depth = get_sample_info(excel_name)

#Function will calculate the parameters from the provided blank test
fit_a, fit_b = calculate_blank_parameters(blank_test)

#Loads the excel workbook 
wb = load_workbook('{x}'.format(x = excel_name))

#Calculates the area of the piston with 86 mm diameter
piston_area = pi * (43 ** 2)

'''
Primary *for* loop iterates through each text file produced by the piston die press test machine:
    1. the text file converted to python readable form
    2. the resulting force and corrected displacement are calculated
    3. the total work and compression ratio (area under the force vs. displacement curve) is calculated. These values are written to the excel workbook
Total specific energy is converted from Joules per gram to kilowatt hours per tonne using a conversion ratio of 3.6J/g = 1 kWh/t
'''
for i in range(len(file_list)):
    time, force, disp = read_file(file_list[i])
    abs_force, corrected_disp, work = column_calculations(force, disp, fit_a, fit_b)
    energy_kWh_per_t = specific_energy_calc(work, mass_list[i])
    total_energy_kWh_per_t = round(work[len(work)-1]/float(mass_list[i]), 4) / 3.6  #3.6 is used to convert J/g to kWh/t
    pressure = abs_force[len(abs_force)-1] * 1000 / piston_area
    compression_ratio = (initial_depth[i] - final_depth[i])/initial_depth[i]
    write_to_file(file_list[i], wb, abs_force, corrected_disp, energy_kWh_per_t, total_energy_kWh_per_t, pressure, excel_name, compression_ratio)
