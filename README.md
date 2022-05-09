# Piston-Die-Press-Test-Analysis
The objective of this code is to preform the necessary calculations on piston die press test data to produce the required force displacement curves, calculate the input specific energy into the pressed sample, and calculate the compaction ratio of the sample. 


## Summary of piston die press test experiments
Piston die press tests are used to measure the energy required to compact soils and powders. This can give information about soil compaction properites, rock competency and breakage behaviours.  

The sample is added to a confined piston die, it is then compacted at a constant rate, either:
	1. force controlled, where the force is increased incrementally to a preset maximum force and the compression displacement is the measured variable or,
	2. displacement controlled, where the displacement is increased incrementally to a preset maximum distance compressed and the force applied is the measure variable.
  
## Preparing the files for analysis
The piston die press test machine produces a .txt or .dat file of a specific format which includes (in this order):
	1. Time in seconds - time, starting at 0 seconds, at which a force, displacement measurement is taken
	2. Force in kilonewtons - force which is being applied to the piston
	3. Displacement in millimeters - displacement of the piston from position zero
To prepare the .txt/.dat files: ensure that the data of interest starts on line 9, and that there are no line breaks in or after the data

The excel file should contain the sample file names (inluding extensions), sample mass (in grams), the initial and final bed heights, and the name a blank sample test file. The file should look as below:
