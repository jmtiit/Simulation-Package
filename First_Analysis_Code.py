import numpy as np
import sys
import time
import operator as op


txt_file = open("C:/Users/Jonathan/Downloads/verbose1simulation.txt", "r")  #opens the txt file for reading purposes, of course you want to put your own path to the txt file

lines = txt_file.readlines()                                                #creates a list with the lines of the txt as elements

txt_file.close()

particle_line_num = []                                                      #elements are the numbers of the lines which contains info about a new particle

particle_count = []                                                         #elements are lists with the particle type and the particle type count

particle_types = []                                                         #elements are different particle types

all_particle_types = []                                                     #elements are all the particle types in the order they appear in the txt file

run_count = 0

for line_num, line in enumerate(lines):
    
    if line[:44] == "G4WT0 > --------------------End of Local Run" :
        
        end_line_num = line_num

    if line[:17] == "G4WT0 > * G4Track" :                                   #finds the elements that contains particle type information
        
        if line[54:67] == "Track ID = 1,":
        
            run_count += 1
        
        particle_line_num.append(line_num)
        
        p_type = ""
        
        for letter in line[44:] :                                           #iterates over the letters to write down the particle type
            
            if letter == "," :
                
                all_particle_types.append(p_type)
                
                run_part_count = [run_count, p_type]
                
                if run_part_count not in particle_types :
                    
                    particle_types.append(run_part_count)
                    
                    p_count = [run_count, p_type, 1]                        #p_count is a two elements list to keep track of how many times a specific particle is created
                    
                    particle_count.append(p_count)
                    
                else:
                    
                    for n, counter in enumerate(particle_count):
                        
                        if run_part_count == counter[:2]:
                            
                            run_part_count = [counter[0] , counter[1], counter[2] + 1]              #every time the same particle occur p_count is updated
                            
                            particle_count[n] = run_part_count                                      #and saved into particle_count         
                            
                    
                break
                
            p_type += letter

            
#print(particle_types)

#print(all_particle_types)
            
#print(particle_count)


###########################################################################################################


energies = []

for n in particle_line_num :
   
    part_first_line = lines[n + 4]
    
    KinE_MeV = ""
    
    for number in part_first_line[41:51] :
        
        if number == " " :
            
            pass
            
        else :
            
            KinE_MeV += number
            
    KinE_MeV = float(KinE_MeV)
            
    energies.append(KinE_MeV)
    
#print(energies)


############################################################################################################


track_leng = []

for n in particle_line_num[1:] :
   
    part_last_line = lines[n - 3]
    
    length = ""
    
    for number in part_last_line[69:79] :
        
        if number == " " :
            
            pass
            
        else :
            
            length += number
    
    length = float(length)
    
    track_leng.append(length)

    
length = ""
    
last_line = lines[end_line_num - 2]

for number in last_line[69:79] :
    
    if number == " " :
            
        pass
            
    else :
            
        length += number
    
length = float(length)
    
track_leng.append(length)

#print(track_leng)
    

#############################################################################################################
    

time0 = time.time()

np.set_printoptions(threshold=sys.maxsize)
merged_list = list( zip(all_particle_types, energies, track_leng))

time = time.time() - time0

#print(time)


for n,particle in enumerate(merged_list) :
    
    #print(type(particle))
    if particle[0] == 'e-' :
        
        pass

#print(merged_list)


###############################################################################################################


x_start = []

for n in particle_line_num :
   
    part_first_line = lines[n + 4]
    
    x = ""
    
    for number in part_first_line[14:23] :
        
        if number == " " :
            
            pass
            
        else :
            
            x += number
            
    x = float(x)
            
    x_start.append(x)

    
#print(x_start)


y_start = []

for n in particle_line_num :
   
    part_first_line = lines[n + 4]
    
    y = ""
    
    for number in part_first_line[23:32] :
        
        if number == " " :
            
            pass
            
        else :
            
            y += number
            
    y = float(y)
            
    y_start.append(y)

    
#print(y_start)


z_start = []

for n in particle_line_num :
   
    part_first_line = lines[n + 4]
    
    z = ""
    
    for number in part_first_line[32:41] :
        
        if number == " " :
            
            pass
            
        else :
            
            z += number
            
    z = float(z)
            
    z_start.append(z)

    
#print(z_start)


################################################################################################################


x_end = []

for n in particle_line_num[1:] :
   
    part_last_line = lines[n - 3]
    
    x = ""
    
    for number in part_last_line[14:23] :
        
        if number == " " :
            
            pass
            
        else :
            
            x += number
    
    x = float(x)
    
    x_end.append(x)

    
x = ""
    
last_line = lines[end_line_num - 2]

for number in last_line[14:23] :
    
    if number == " " :
            
        pass
            
    else :
            
        x += number
    
x = float(x)
    
x_end.append(x)

#print(x_end)


y_end = []

for n in particle_line_num[1:] :
   
    part_last_line = lines[n - 3]
    
    y = ""
    
    for number in part_last_line[23:32] :
        
        if number == " " :
            
            pass
            
        else :
            
            y += number
    
    y = float(y)
    
    y_end.append(y)

    
y = ""
    
for number in last_line[23:32] :
    
    if number == " " :
            
        pass
            
    else :
            
        y += number
    
y = float(y)
    
y_end.append(y)

#print(y_end)


z_end = []

for n in particle_line_num[1:] :
   
    part_last_line = lines[n - 3]
    
    z = ""
    
    for number in part_last_line[32:41] :
        
        if number == " " :
            
            pass
            
        else :
            
            z += number
    
    z = float(z)
    
    z_end.append(z)

    
z = ""
    
for number in last_line[32:41] :
    
    if number == " " :
            
        pass
            
    else :
            
        z += number
    
z = float(z)
    
z_end.append(z)

#print(z_end)


###################################################################################################################


def square(list):
    return map(lambda x: x ** 2, list)

def sqrt(list):
    return map(lambda x: x ** 0.5, list)

x_start_square = square(x_start)

y_start_square = square(y_start)

z_start_square = square(z_start)

r_start_square = map(op.add, x_start_square, y_start_square)

#r = list(sqrt(r_start_square))

x_end_square = square(x_end)

y_end_square = square(y_end)

z_end_square = square(z_end)

r_end_square = map(op.add, x_end_square, y_end_square)

start_square = map(op.add, r_start_square, z_start_square)

end_square = map(op.add, r_end_square, z_end_square)

travel_dist_square = map(abs, map(op.sub, end_square, start_square))

travel_dist =map(sqrt, travel_dist_square)

print(list(travel_dist_square))