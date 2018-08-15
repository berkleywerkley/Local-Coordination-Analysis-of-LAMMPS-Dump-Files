"""
Pulls conductivity and parameter values from conductivity.data files in a set of subdirectories
"""

import matplotlib.pyplot as plt
import os

directory_contents= os.listdir('/Users/Arthur/Desktop/MIT/Param10_II/Results')

ss_radius = []
conductivity = []
cat_con = []
Dcs = []
Das = []

def readfile(filename):
    """
    Function to read data file of known format and extra desired info
    filename: string
        path of file from which values are to be extracted
    """
    data = []
    with open(str(filename), 'r') as fin:
        for line in fin:
            data.append(line.strip()) # read each line and add to list
        ss_radius.append(float(data[11]))
        conductivity.append(float(data[12]))
        Dc = float(data[13])
        Dcs.append(Dc)
        Da = float(data[14])
        Das.append(Da)
        cat_con.append((Dc/(Dc + Da)) * float(data[12]))

#iterate through directory, opening sub-directories that start with 'run'
script_dir = os.path.dirname(os.path.realpath('__file__'))
#print(script_dir)
for item in directory_contents:
    if item.startswith('run'):
        dest_file = 'Results/' + item + '/conductivity.data'
        filename = os.path.join(script_dir, dest_file)
        #print(filename)
        readfile(filename)

###plot and save desired graphs

plt.style.use('seaborn-talk')

plt.figure()
plt.scatter(ss_radius, conductivity)
plt.xlabel('Secondary Site Radius /Reduced Units')
plt.ylabel('Conductivity /$Scm^-1$')
plt.title('Effect of Monomer Radius on Conductivity')
plt.tight_layout()
plt.savefig('Conductivity_Plot.png')

plt.figure()
plt.scatter(ss_radius,cat_con)
plt.xlabel('Secondary Site Radius /Reduced Units')
plt.ylabel('Cation Conductivity')
plt.tight_layout()
plt.savefig('Cat_Con.png')

plt.figure()
plt.scatter(ss_radius, Dcs)
plt.xlabel('Secondary Site Radius /Reduced Units')
plt.ylabel('Dc')
plt.ylim(0,1e-5)
plt.tight_layout()
plt.savefig('Dc.png')

plt.figure()
plt.scatter(ss_radius, Das)
plt.xlabel('Secondary Site Radius /Reduced Units')
plt.ylabel('Da')
plt.ylim(0,1e-6)
plt.tight_layout()
plt.savefig('Da.png')