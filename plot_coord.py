"""
Plots the variation of conductivity with the parameter in question changed
On secondary y - axis also plots how Coordination Number and local composition varies with parameter
"""
import csv
import matplotlib.pyplot as plt
import os

radii = []
conductivities = []
CNs =[]
p_1s = []
p_2s = []
p_3s = []
p_4s = []

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, 'coord.csv'), 'r') as fin:
    reader = csv.reader(fin)
    for row in reader:
        radii.append(float(row[0]))
        conductivities.append(float(row[1]))
        CNs.append(float(row[2]))
        p_1s.append(float(row[3]))
        p_2s.append(float(row[4]))
        p_3s.append(float(row[5]))
        p_4s.append(float(row[6]))


y_vars = [CNs, p_1s, p_2s, p_3s, p_4s]
labels = ['Coordination Number', 'Local Proportion of Monomer', 'Local Proportion of Cation', 'Local Proportion of Anion', 'Local Proportion of Monomer']
files = ['CN', 'P1', 'P2', 'P3', 'P4']
titles = ['Correlation with CN', 'Do not use', 'Correlation with local amount of Cation', 'Correlation with local amount of Anion', 'Correlation with local amount of Monomer']

plt.style.use('seaborn-talk')

i = 0
while i < len(y_vars):
    fig, ax1 =plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Monomer Radius /Reduced Units')
    ax1.set_ylabel('Conductivity /S$cm^-1$', color=color)
    ax1.scatter(radii, conductivities, color=color )
    ax1. tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel(labels[i], color=color)  # we already handled the x-label with ax1
    ax2.scatter(radii, y_vars[i], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(titles[i])
    plt.tight_layout()
    
    plt.savefig('/Users/Arthur/Desktop/MIT/Param10_II/%s.png' % files[i])
    
    i += 1