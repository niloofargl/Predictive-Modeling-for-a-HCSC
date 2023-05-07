from Solution import Solution
from random import random, randint
from Population import Population
import matlab.engine
import os.path
from matplotlib import pyplot as plt
import pandas as pd

# Data File Path

filepath = 'Edmonton.txt'
data = pd.read_csv(filepath, comment='#',sep='\t', header=None)
'''
n_days: Number of days for training
start_day: The proposed initial day for training 
'''
start_day = 360
n_days =  560 #Ontario 160  380           #Alberta -20 compared to CANADA            ##CANADA # 485 #340      #120 
data = data.values
data = data[:,start_day:n_days]

# Parameters of the genetic algorithm:
max_iter = 3       #maximum iteration
pop_size = 5      #population size
mutation_rate = 0.3
crossover_rate = 0.8

#Math model params
eng = matlab.engine.start_matlab()

print("Generating first pop")   #Generate an initial population

my_pop = Population(pop_size, eng, data)

#Ierative process
generation_count = 0
print("Generation : %s Fittest : %s " % (generation_count, my_pop.get_best().fitness()))
#my_pop.get_best().DisplayPlots(eng)
wape_history = []

''' Optimal error rate: 
                WAPE: Weighted Absolute Percentage Error'''

for i in range(max_iter):
    generation_count += 1

    my_pop = my_pop.evolve_population(eng,mutation_rate, crossover_rate)
    current_best = generation_count, my_pop.get_best().fitness()
    print("Generation : %s Fittest : %s " % (current_best))

   
    print (my_pop.get_best().wape)
    wape_history.append( my_pop.get_best().wape )
    print("******************************************************")

print("My Best parameter is: ", my_pop.get_best().NestedParameters)

best_sol  = my_pop.get_best()
best_sol.evaluate(eng,data,isshow = 1)
'****'

if not os.path.isfile("output.txt"):
    # If the file does not exist, print the header
    file = open("output.txt", "a")
    print("Train data for",filepath,my_pop.get_best().NestedParameters, file=file)
    print("The Error rate for",filepath,my_pop.get_best().wape, file=file)
    file.close()
else:
    # Open the file in append mode
    with open("output.txt", "a") as file:
    # Print the output to the file
        print("This is the next output.", file=file)

#with open("output.txt", "a") as file:
  #  print("Train data for",filepath,my_pop.get_best().NestedParameters, file=file)
#with open("output.txt", "a") as file:
    # Run your code and redirect the output to the file
    #print("Output of second run", file=file)
#file.close()