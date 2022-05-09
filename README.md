# Piston-Die-Press-Test-Analysis
The objective of this code is to preform the necessary calculations on piston die press test data to produce the required force displacement curves, calculate the input specific energy into the pressed sample, and calculate the compaction ratio of the sample. 


## Summary of piston die press test experiments
Piston die press tests are used to measure the energy required to compact soils and powders. This can give information about soil compaction properites, rock competency and breakage behaviours.  

The sample is added to a confined piston die, it is then compacted at a constant rate, either:
	1. force controlled, where the force is increased incrementally to a preset maximum force and the compression displacement is the measured variable or,
	2. displacement controlled, where the displacement is increased incrementally to a preset maximum distance compressed and the force applied is the measure variable.

There is also consideration for the effect of the stain applied to the machine which is not attributable to the sample. The addition of a correction factor based on a blank test (i.e., a test in the piston die press test without soil or powder) is used to correct for the inherent machine strain. The blank test behaviour best fit an allometric function (y = ax^b) (see below). The calculated a and b values for the blank test is based on the blank sample provided in the excel file (see below). This function will then be used to calculate the correction factor over the entier force profile of the test.  
![allometricfit](https://user-images.githubusercontent.com/103532979/167487099-1800fe77-ee1b-4e2b-bfea-4a0684a09b4a.png)

  
## Preparing the files for analysis
The piston die press test machine produces a .txt or .dat file of a specific format which includes (in this order):
	1. Time in seconds - time, starting at 0 seconds, at which a force, displacement measurement is taken
	2. Force in kilonewtons - force which is being applied to the piston
	3. Displacement in millimeters - displacement of the piston from position zero
To prepare the .txt/.dat files: ensure that the data of interest starts on line 9, and that there are no line breaks in or after the data

The excel file should be save in the same folder as the 4 python code files and should contain the piston press test file names (inluding extensions), sample mass (in grams), the initial and final bed heights, and the name a blank sample test file. The file should look as below:
![excelsnip_readme](https://user-images.githubusercontent.com/103532979/167482221-80a68be9-ba7b-4fcc-b90a-e85718d2cb1b.png)

*Note:* 1. The sample name must have the file extenstion (.dat or .txt are acceptable)
	2. The calculation for the compaction ratio is based on the difference between the initial and final sample height and will depend heighly on the individual 		setup. The code should be adjusted for different setup scenarios.
	
