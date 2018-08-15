# Local-Coordination-Analysis-of-LAMMPS-Dump-Files
Part of Work at MIT

Python scripts to extract information about coordination number and local composition for a single type of particle
from LAMMPS dump files

##data_collector.py
Collects Conductivity and parameter data from 'conductivity.data' files of constant format

##avg_coord.py
Outputs a csv file containing avg Coordination Number and local composition for type of particle for a complete set of simulations

##plot_coord.py
Plots the variation of conductivity with the parameter in question changed
On secondary y - axis also plots how Coordination Number and local composition varies with parameter
