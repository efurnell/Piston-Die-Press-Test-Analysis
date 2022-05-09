import argparse
import pandas as pd
import numpy as np


'''
    Function name:      get_args
    Input parameters:   none
    Return parameters:  Returns the name of the excel file that conatins the sample information and to which all calculated data will be written 
                        (excel file should be in the same folder as the python program files)
    Required library:   argparse
'''
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', help='Please input the read/write excel file name (file_name.xlsx)', required=True)
    args = parser.parse_args()
    return args.file_name



'''
    Function name:      get_sample_info
    Input parameters:   Excel file name (format = file_name.xlsx)
    Return parameters:  Sample data listed in the excel file
    Description:        This function converts the excel data listed on the first page of the excel file to usable python lists. This function requires that
                        the excel file be set up in a specific way which is described in readme.txt. Additionally, this function will determine if there is a
                        blank piston die press test against which the regular sample data can be compared. 
                        This function calls get_bed_depth_height.
    Required library:   pandas, numpy
'''
def get_sample_info(f):
    df = pd.read_excel(f)
    files = df['File'].tolist()
    masses = df['Mass'].tolist()
    blank_test = df.iat[0, 9]
    try:
        np.isnan(blank_test)
        print('No blank file provided')
        blank_test = 'none'
    except TypeError:
        blank_test = blank_test
    initial_depth, final_depth = get_bed_depth_height(df)
    return files, masses, blank_test, initial_depth, final_depth



'''
    Function name:      convert_file_to_list
    Input parameters:   data (text file)
    Return parameters:  time, axialdisp, axialforce (list)
    Description:        This function converts the output piston die press test machine text file to usable python lists.
    Warnings:           1.  Assumes data begins on line 9 of the text file (this number should be change based on indiviual piston die press test
                            output)
                        2.  Requires that the data list within the text file is continous (no gaps or line breaks)
                        3.  Requires that there is only three data lists (time, displacement, and force). If there are additional data lists in the
                            file then this function should be adjusted to reflect that
    Required library:   none
'''
def convert_file_to_list(data):
    time, axialdisp, axialforce = [], [], []
    i = 8
    while i < len(data):
        m = 0
        x = data[i].split('\t')
        while m < 3:
            if m == 0:
                time.append(float(x[m]))
            elif m == 1:
                axialforce.append(float(x[m]))
            elif m == 2:
                axialdisp.append(float(x[m]))
            m += 1
        i += 1
    return time, axialdisp, axialforce



'''
    Function name:      get_bed_depth_height
    Input parameters:   Pandas DataFrame (from inital excel file)
    Return parameters:  Inital and final bed depth measured prior to and following the piston die press test 
                        (these data are instrument specific and the code should be adjusted to suit individual set ups (see readme.txt for further details))
    Required library:   pandas, numpy
'''
def get_bed_depth_height(df):
    i_depth, f_depth = [], []
    i_depth_1 = df['Initial_depth_1'].tolist()
    i_depth_2 = df['Initial_depth_2'].tolist()
    i_depth_3 = df['Initial_depth_3'].tolist()
    f_depth_1 = df['Final_depth_1'].tolist()
    f_depth_2 = df['Final_depth_2'].tolist()
    f_depth_3 = df['Final_depth_3'].tolist()
    i = 0
    for i in range(len(i_depth_1)):
        i_depth.append((153 - i_depth_1[i] - i_depth_2[i] - i_depth_3[i])/(len(f_depth_1) + 1))
        f_depth.append((153 - f_depth_1[i] - f_depth_2[i] - f_depth_3[i])/(len(f_depth_1) + 1))
        i =+ 1
    return i_depth, f_depth



'''
    Function name:      read_file
    Input parameters:   Text file produced by piston die press test machine containing three data columns: time, axial force (N), and axial 
                        displacement (mm)
    Return parameters:  Time, axial displacement, and axial force as lists
    Warnings:           This function requires the text file to meet specific requirements. See readme.txt for further details
    Required library:   none
'''
def read_file(file_name):
    file = open('{x}'.format(x=file_name))
    data = file.readlines()
    time, axialforce, axialdisp = convert_file_to_list(data)
    return time, axialdisp, axialforce



'''
    Function name:      write_to_file
    Input parameters:   Excel file name and excel workbook
                        Force = force applied to during the piston die press test (positive values, format = list)
                        Corrected displacement = displacement of the piston die during the test adjusted based on the provided blank test information (format = list)
                        Specific energy = incremental areas under the force-displacement curve (kWh/t)
                        Work = total area under the force displacement curve (kWh/t)
                        Piston pressure = the pressure applied to the piston based on the area of the piston
                        excel_name = name of the excel file to which all data will be written
                        comp_ratio(compression ratio) = comparison of sample height before and after the piston die press test
    Return parameters:  none
    Notes:              This function will write all input data to a worksheet in the specified excel file
    Required library:   pandas
'''
def write_to_file(file_name, wb, force, corrected_disp, specific_energy, work, piston_pressure, excel_name, comp_ratio):
    f = file_name.split('.')[0]
    sheet = wb.create_sheet('{x}'.format(x = f))
    headers = ['Corrected Displacement (mm)', 'Force (kN)', 'Specific Energy (kWh/t)']
    for i in range(len(headers)):
        c = sheet.cell(row = 1, column = i + 1)
        c.value = headers[i]

    for i in range(len(force)):
        c = sheet.cell(row = i + 2, column = 1)
        c.value = corrected_disp[i]
        d = sheet.cell(row = i + 2, column = 2)
        d.value = force[i]
        f = sheet.cell(row = i + 2, column = 3)
        f.value = specific_energy[i]


    a = sheet.cell(row = 1, column = 5)
    a.value = 'Specific Energy (kWh/t)'
    b = sheet.cell(row = 2, column = 5)
    b.value = work
    a = sheet.cell(row = 1, column = 7)
    a.value = 'Pressure (N/mm^2)'
    b = sheet.cell(row = 2, column = 7)
    b.value = piston_pressure
    a = sheet.cell(row = 1, column = 9)
    a.value = 'Compression Ratio'
    b = sheet.cell(row = 2, column = 9)
    b.value = comp_ratio
    wb.save(excel_name)
