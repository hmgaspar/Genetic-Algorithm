#! /usr/bin/env python

from pylab import *

#Functions
# Define the x function
def x_function(x):
	#_function = (sin(300)**2)/(1+(x-500)**2)*50
	#_function = sin(x)*5+sin(x/10)*5+sin(x/100)*10
	_function = 8000*x - 0.25*x**2
	return _function


# Convert decimal to a binary string
def den2bin(f):
	bStr = ''
	n = int(f)
	if n < 0: raise
	if n == 0: return '0'
	while n > 0:
		bStr = str(n % 2) + bStr
		n = n >> 1
	return bStr

#Convert decimal to a binary string of desired size of bits 
def d2b(f, b):
	n = int(f)
	base = int(b)
	ret = ""
	for y in range(base-1, -1, -1):
		ret += str((n >> y) & 1)
	return ret


#Invert Chromosome
def invchr(string, position):
	if int(string[position]) == 1:
		
		string = string[:position] + '0' + string[position+1:]
	else:
		string = string[:position] + '1' + string[position+1:]
	return string


#Roulette Wheel
def roulette(values, fitness):
	n_rand = random()*fitness
	sum_fit = 0
	for i in range(len(values)):
		sum_fit += values[i]
		if sum_fit >= n_rand:
			break
	return i	




# Genetic Algorithm Code to find the Maximum of F(X)


#Range of Values
x_max = 32000
x_min = 0

#GA Parameters
# Due my laziness to do the code, the population size must be a even number and the values for x are always integers.
# Feel free to correct it :) 
pop_size = 100
mutation_probability = 0.0
number_of_generations = 1


#Variables & Lists to be used during the code
gen_1_xvalues = []
gen_1_fvalues = []
generations_x = []
generations_f = []
fitness = 0


#Size of the string in bit
x_size = int(len(den2bin(x_max)))


print "Maximum chromosome size of x is", x_size,  "bits, i.e.,", pow(2,x_size), "variables."


#first population - random values
for i in range(pop_size):
	x_tmp = int(round(randint(x_max-x_min)+x_min))
	gen_1_xvalues.append(x_tmp)

	f_tmp = x_function(x_tmp)
	gen_1_fvalues.append(f_tmp)

	#Create total fitness
	fitness += f_tmp
#print 'gen 1', gen_1_xvalues

#Getting maximum value for initial population
max_f_gen1 = 0
for i in range(pop_size):
		if gen_1_fvalues[i] >= max_f_gen1:
			max_f_gen1 = gen_1_fvalues[i]
			max_x_gen1 = gen_1_xvalues[i]





#Starting GA loop

for i in range(number_of_generations):
	#Reseting list for 2nd generation
	gen_2_xvalues = []
	gen_2_fvalues = []
	selected = []

	#Selecting individuals to reproduce
	for j in range(pop_size):
		ind_sel = roulette(gen_1_fvalues,fitness)
		selected.append(gen_1_xvalues[ind_sel])

	#Crossing the selected members
	for j in range(0, pop_size, 2):
		sel_ind_A = d2b(selected[j],x_size)
		sel_ind_B = d2b(selected[j+1],x_size)
	
	#select point to cross over
		cut_point = randint(1,x_size)
	
	#new individual AB
		ind_AB = sel_ind_A[:cut_point] + sel_ind_B[cut_point:]

	#mutation AB
		ran_mut = random()
		if ran_mut < mutation_probability:
			gene_position = randint(0,x_size)
			ind_mut = invchr(ind_AB, gene_position)
			ind_AB = ind_mut
	
	#new individual BA
		ind_BA = sel_ind_B[:cut_point] + sel_ind_A[cut_point:]		


	#mutation BA
		ran_mut = random()
		if ran_mut < mutation_probability:
			gene_position = randint(0,x_size)
			ind_mut = invchr(ind_BA, gene_position)
			ind_BA = ind_mut

	#Creating Generation 2
		new_AB = int(ind_AB,2)
		gen_2_xvalues.append(new_AB)

		new_f_AB = x_function(new_AB)
		gen_2_fvalues.append(new_f_AB)

		new_BA = int(ind_BA,2)
		gen_2_xvalues.append(new_BA)

		new_f_BA = x_function(new_BA)
		gen_2_fvalues.append(new_f_BA)
	#print 'gen',i+2, gen_2_xvalues


	#Getting maximum value
	max_f_gen2 = 0
	for j in range(pop_size):
		if gen_2_fvalues[j] >= max_f_gen2:
			max_f_gen2 = gen_2_fvalues[j]
			max_x_gen2 = gen_2_xvalues[j]

	#Elitism one individual
	if max_f_gen1 > max_f_gen2:
		max_f_gen2 = max_f_gen1
		max_x_gen2 = max_x_gen1
		gen_2_fvalues[0] = max_f_gen1
		gen_2_xvalues[0] = max_x_gen1
	
	#Transform gen2 into gen1
	gen_1_xvalues = gen_2_xvalues
	gen_1_fvalues = gen_2_fvalues
	max_x_gen1 = max_x_gen2
	max_f_gen1 = max_f_gen2
	generations_x.append(max_x_gen2)
	generations_f.append(max_f_gen2)

	#Creating new fitness
	fitness = 0
	for j in range(pop_size):
		f_tmp = x_function(gen_1_xvalues[j])
		fitness += f_tmp


#Ploting

#Ploting  Function
x = arange(x_min,x_max,0.01)
y = x_function(x)

#figure(1)
plot(x,y)
xlabel('x')
ylabel('F(x)')
title(r'$F(x)$')

#Ploting data for last generation
figure(2)
plot(gen_2_xvalues,gen_2_fvalues, 'bo')
xlabel('x')
ylabel('F(x)')
title(r'Data for last generation')

#Ploting data for maximum values for each generation
figure(3)
plot(range(number_of_generations),generations_f, 'ro')
xlabel('Generations')
ylabel('F(x) Maximum')
title(r'$F(x)$')
show()

	



