'''
    Function name:      absolute_value_list
    Input parameters:   list
    Return parameters:  list
    Description:        This function takes the absolute value of each element in a list
    Required library:   none
'''
def absolute_value_list(x):
    y = []
    for i in range(len(x)):
        y.append(abs(x[i]))
    return y



'''
    Function name:      displacement_correction_factor
    Input parameters:   force (list)
                        a = allometric multiplication constant of allometric function (calculated via allometric_fit)
                        b = allometric exponent constant of allometric function (calculated via allometric_fit)
    Return parameters:  corr_factor = corrected displacement factor (list)
    Description:        This function calculates the factor at each force value which needs to be applied to the sample data to account for
                        the strain inherent in the system (based on the blank test) (see readme.txt for more information)
'''
def dispacement_correction_factor(force, a, b):
    i = 0
    corr_disp = []
    while i < len(force):
        corr_factor.append(a * pow(force[i], b))
        i += 1
    return corr_factor



'''
    Function name:      displacement_correction
    Input parameters:   displacement = absolute value of press test displacement (list)
                        corr_factor = correction factor calculated via displacement_correction_factor function (list)
                        corr_disp = empty list to which the corrected displacment will be input
    Return parameters:  corr_disp
    Required library:   none
'''
def dispacement_correction(displacement, corr_factor, corr_disp):
    i = 0
    while i < len(displacement):
        corr_disp.append(displacement[i] - corr_factor[i])
        i += 1
    return corr_disp



'''
    Function name:      work_calc
    Input parameters:   force = force applied to a particular sample (list)
                        corr_disp = corrected displacement for a particular sample (list)
    Return parameters:  incremental and cumulative work under the force displacement curve (list)
    Description:        This function uses the trapezoidal rule to calculate the area under the curve and takes the cumulative sum of calculated
                        trapezoidal areas
    Required library:   none
'''
def work_calc(force, corr_disp):
    i = 1
    work = [0]
    while i < len(force):
        x = 0.5 * (force[i] + force[i - 1]) * (corr_disp[i] - corr_disp[i - 1]) + work[i - 1]
        work.append(x)
        i += 1
    return work



'''
    Function name:      column_calculations
    Input parameters:   axialforce = force information extracted from the sample text file produced by the piston die press test machine (list)
                        axialdisp = displacement information extracted from the sample text file produced by the piston die press test machine (list)
                        allometric_a = multiplication constant in allometric function (y = ax**b) fitted to the blank sample test (float)
                        allometric_b = exponent constant in allometric function (y = ax**b) fitted to the blank sample test (float)
                        (see readme.txt for more information regarding allometric functions)
    Return parameters:  forceN = list of absolute values of forces from axialforce (list)
                        corrected_disp = displacement values which have been corrected to account for offset measure during the blank test (list)
                        work = work calculated based on the force-displacement behaviour of the sample (list)
    Description:        This function will prepare the displacement, force, and work lists which are to be written to excel for each sample. This function
                        will have to be run for each sample of interest; allometric_a and allometric_b will not change but axialforce and axialdisp will.
    Required library:   none
    Required func:      absolute_value_list
                        displacement_correction_factor
                        displacement_correction
                        work_calc
'''
def column_calculations(axialforce, axialdisp, allometric_a, allometric_b):
    forceN, disp, correction_factor, corrected_disp = [], [], [], []
    forceN = absolute_value_list(axialforce)
    disp = absolute_value_list(axialdisp)
    correction_factor = dispacement_correction_factor(forceN, allometric_a, allometric_b)
    corrected_disp = dispacement_correction(disp, correction_factor, corrected_disp)
    work = work_calc(forceN, corrected_disp)
    return forceN, corrected_disp, work



'''
    Function name:      specific_energy_calc
    Input parameters:   work = list of the cumulative area under force-displacement curve at each point (list)
                        mass = total sample mass (float, int, or str)
    Return parameters:  specific_e_list = list of specific energy (work/mass); based on incremental work (area under force displacement curve)
    Description:        This function will convert work (J) to specific energy (kWh/t) by dividing by the sample mass (g). The factor of 3.6 is used to
                        convert J/g to kWh/t.
    Required library:   none
'''
def specific_energy_calc(work, mass):
    i = 0
    specific_e_list = []
    while i < len(work):
        specific_e_list.append(work[i] / float(mass) / 3.6)
        i += 1
    return specific_e_list
