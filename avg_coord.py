"""
Creates an output file coord.csv that prints the average coordination number and local proportions of cation, anion and monomer for
Li+ ions in electrolyte simulation.
"""

from collections import Counter
import os
import matplotlib.pyplot as plt
import csv

half_side_length = 1.1197216739351800e+01

def local_environment(ref_particle_id, filename, cutoff_radius):
    """
    find Coordination number and local composition around an individual Li + ion
    ref_particle_id: id of reference particle
    dump_file: dump file corresponding to snapshot of interest
    """ 
    #### find coordinates of reference particle
    with open(filename, 'r') as fin:
        for _ in range(9):
            fin.readline()
        for line in fin:
            vals = line.split()
            if vals[0] == str(ref_particle_id):
                ref_x = float(vals[3]) + half_side_length #add half side length to avoid negative coordinate values
                ref_y = float(vals[4]) + half_side_length
                ref_z = float(vals[5]) + half_side_length
                break
    
    CN = 0
    comp = Counter()
    with open(filename, 'r') as fin:      
        for _ in range(9):
            fin.readline()      
        for line in fin:
            vals = line.split()
            particle_type = vals[2]
            x = float(vals[3]) + half_side_length
            y = float(vals[4]) + half_side_length
            z = float(vals[5]) + half_side_length
            ### Bring all particles within the bounds of the simulation box
            x = x % (2 * half_side_length)
            y = y % (2 * half_side_length)
            z = z % (2 * half_side_length)
            
            ### The following set of if statements account for periodicity.
            ### If a particle is over half a side length's distance from the reference particle,
            ### its periodic image may be within the cutoff radius for consideration

            if abs(x - ref_x) > half_side_length: 
                if x > ref_x:
                    x -= 2*half_side_length
                elif x < ref_x:
                    x += 2*half_side_length
            if abs(y - ref_y) > half_side_length:
                if y > ref_y:
                    y -= 2*half_side_length
                elif y < ref_y:
                    y += 2*half_side_length
            if abs(z - ref_z) > half_side_length:
                if z > ref_z:
                    z -= 2*half_side_length
                elif z < ref_z:
                    z += 2*half_side_length  
            ### Using updated coordinates, calculate distance from ref particle                          
            r = ((x-ref_x)**2 + (y-ref_y)**2 + (z-ref_z)**2)**0.5
            ### if within cutoff radius, add 1 to coordinatio number and record the type of particle
            if r <= cutoff_radius:
                CN += 1
                comp[particle_type]+=1

    ### compute Coordination number and local composition            
    total_num_particles = sum(comp.values())
    percentage_type_1 = comp['1']/total_num_particles
    percentage_type_2 = comp['2']/total_num_particles
    percentage_type_3 = comp['3']/total_num_particles
    percentage_type_4 = comp['4']/total_num_particles
    return CN, percentage_type_1, percentage_type_2, percentage_type_3, percentage_type_4

def avg_local_environment_snap(particle_type, filename):
    """
    Compute the Coordination number and local composition for 50 particles of common type in a snapshot,
    return the mean values
    particle_type: int
        1 = monomer(none in simulation), 2 = cation, 3 = anion, 4 = monomer(present in situation)
    filename: float
        path of file to be examined
    """

    CNs =[]
    p_1s = []
    p_2s = []
    p_3s = []
    p_4s = []

    with open(filename, 'r') as fin:
        #skip first 9 lines    
        for _ in range(9):
            fin.readline()

        count = 0
        while count <= 50:
                
            for line in fin:
                nums = line.split()
                if nums[2] == str(particle_type):
                    #print('Found it!')
                    CN, p_1, p_2, p_3, p_4 = local_environment(nums[0], filename, cutoff_radius=1.5)
                    CNs.append(CN)
                    p_1s.append(p_1)
                    p_2s.append(p_2)
                    p_3s.append(p_3)
                    p_4s.append(p_4)
                    count += 1
    return mean(CNs), mean(p_1s), mean(p_2s), mean(p_3s), mean(p_4s)


def mean(values):
    """
    Returns mean of array
    values: array
        array for which mean is to be calculated
    """
    return (sum(values)/len(values))
    
def avg_local_environment_subdir(particle_type, subdirectory):
    """
    returns average Coordination number and local composition information for a set of snapshots in a simulation
    particle_type: int
        1 = monomer(none in simulation), 2 = cation, 3 = anion, 4 = monomer(present in situation)
    subdirectory: str
        subdirectory of simulation to be examined
    """
    CNs =[]
    p_1s = []
    p_2s = []
    p_3s = []
    p_4s = []
    for item in os.listdir(subdirectory):
        if item == 'conductivity.data':
            with open(subdirectory + '/' + item, 'r') as fin:
                for _ in range(11):
                    fin.readline()
                radius = float(fin.readline())
                conductivity = float(fin.readline())
                print('Radius = ' + str(radius))
                
    for num in range(0, 10000001, 500000):
        if num % 1000000 == 0:
            print('Calculating Coordination Number for dump%s' % str(num))
        filename = 'dump' + str(num)
        
        CN, p_1, p_2, p_3, p_4 = avg_local_environment_snap(2, subdirectory + '/' + str(filename))
        CNs.append(CN)
        p_1s.append(p_1)
        p_2s.append(p_2)
        p_3s.append(p_3)
        p_4s.append(p_4)
    return  radius, conductivity, mean(CNs), mean(p_1s), mean(p_2s), mean(p_3s), mean(p_4s)

def avg_dir(particle_type, directory):
    """
    outputs csv file with coordination number and local compositional data for a set of different simulations
    with different parameters within a folder
    particle_type: int
        1 = monomer(none in simulation), 2 = cation, 3 = anion, 4 = monomer(present in situation)
    directory: str
        path to directory in which the simulation directories to be examined are located
    """
    radii = []
    conductivities = []
    CNs =[]
    p_1s = []
    p_2s = []
    p_3s = []
    p_4s = []

    contents = os.listdir(directory)
    for item in contents:
        if item.startswith('run'):
            print('Looking at subdir: ' + str(item))
            radius, conductivity, CN, p_1, p_2, p_3, p_4 = avg_local_environment_subdir(particle_type, directory + '/' + item)
            radii.append(radius)
            conductivities.append(conductivity)
            CNs.append(CN)
            p_1s.append(p_1)
            p_2s.append(p_2)
            p_3s.append(p_3)
            p_4s.append(p_4)            

    rows = zip(radii,conductivities,CNs,p_1s,p_2s,p_3s,p_4s)
    with open('coord.csv', 'w') as fout:
        writer = csv.writer(fout)
        for row in rows:
            writer.writerow(row)


avg_dir(2, '/Users/Arthur/Desktop/MIT/Param10_II/Results')