import random
from random import *
from Solution import Solution
import pandas as pd


class Population:
    def __init__(self,size, eng, data): #def __init__(self,size, eng, filepath):
        #self.filepath = filepath
        self.data = data    

        self.size = size
        self.popMembers = []
        # generate random parameter for each solution
        for i in range(0, size):
            Tu = 14     #stabilize DDE

            Tmax = self.data.shape[1]   #Number of training data


            tau = randint(0,200)    #Incubation period 

            # mild
            taumih = randint(1, 20)   #The expected time for mild infected people to develop symptoms requiring hospitalization
            taumid = randint(1, 20)   #The expected time for mild infected people to die from the infection
            taumir = randint(1, 20)   #The expected time for mild infected people to recover from the infection

            # moderate
            taumor = randint(1, 20)   #The expected time for moderate infected people to recover from the infection
            taumoh = randint(1, 20)   #The expected time for moderate infected people to develop symptoms requiring hospitalization 
            taumoi = randint(1, 20)   #The expected time for moderate infected people to develop symptoms requiring ICU
            taumod = randint(1, 20)   #The expected time for moderate infected people to die from the infection

            # severe
            taush = randint(1, 20)     # The expected time for severe infected people to develop symptoms requiring hospitalization
            tausi = randint(1, 20)     #The expected time for severe infected people to develop symptoms requiring ICU hospitalization
            tausd = randint(1, 20)     #The expected time for severe infected people to die from the infection

            # hosp
            tauhr = randint(1,20)     #The expected time for hospitalized people to recover from the infection
            tauhi = randint(1,20)     #The expected time for hospitalized people to develop symptoms requiring transfer to ICU hospitalization
            tauhd = randint(1, 20)    # The expected time for hospitalized people to die from the infection

            # ICU
            tauir = randint(1,20)    #The expected time for ICU hospitalized people to recover from the infection
            tauid = randint(1, 20)   # The expected time for ICU hospitalized people to die from the infection
            

            # Rates Parameters

            # rho
            rhomi = uniform(0.85, 0.999)    #The expected proportion of infected people to develop mild symptoms after the incubation period
            rhos = uniform(0.005, 0.1)      #The expected proportion of infected people to develop severe symptoms after the incubation period
            rhomo = uniform(0.05, 0.15)     ##The expected proportion of infected people to develop moderate symptoms after the incubation period
            '''normalize'''
            ro = rhomi + rhos + rhomo
            
            rhomi = rhomi/ ro
            rhos = rhos/ ro
            rhomo = rhomo/ ro

            # eta
            etamir = uniform(0.0, 0.99)    #The expected proportion of mildly infected people to recover from symptoms after the delay period
            etamid = uniform(0.0,0.05)     #The expected proportion of mildly infected people to die from symptoms after the delay period 
            etamih = uniform(0.0,0.4)      #The expected proportion of mildly infected people to hospitalization from symptoms after the delay period       
            '''normalize'''
            mi = etamir+etamid+etamih
            etamir = etamir/mi
            etamih = etamih/mi
            etamid = etamid/mi


            etamor = uniform(0.0, 0.95)       #The expected proportion of moderate infected people to recover from symptoms after the delay period
            etamoi= uniform(0.0, 0.5)         #The expected proportion of moderate infected people to ICU from symptoms after the delay period     
            etamod = uniform(0.000, 0.05)     #The expected proportion of moderate infected people to die from symptoms after the delay period
            etamoh = uniform(0.0, 0.45)       #The expected proportion of moderate infected people to hospitalization from symptoms after the delay period          
            '''normalize'''
            eta = etamor + etamoi + etamod + etamoh

            etamor =etamor / eta
            etamoi= etamoi / eta
            etamod = etamod /eta
            etamoh = etamoh / eta 
            

            etash = uniform(0.0, 0.85)      #The expected proportion of severe infected people to hospitalization from symptoms after the delay period    
            etasd = uniform(0.001, 0.005)   #The expected proportion of severe infected people to die from symptoms after the delay period 
            etasi = 1 - (etash+ etasd)      #The expected proportion of severe infected people to ICU from symptoms after the delay period

            # lambda
            lambdahr = uniform(0.0, 0.90)           #The expected proportion of hospitalized infected people to recover from symptoms after the delay period
            lambdahd = uniform(0.000, 0.005)        #The expected proportion of hospitalized infected people to die from symptoms after the delay period
            lambdahi = 1 - (lambdahr + lambdahd)    #The expected proportion of hospitalized infected people to ICU from symptoms after the delay period

            # delta
            deltaid = uniform(0.000, 0.05)          #The expected proportion of ICU hospitalized infected people to die from symptoms after the delay period    
            deltair = 1- deltaid                    #The expected proportion of ICU hospitalized infected people to recover from symptoms after the delay period
 
            
            #Scale 
            scale_r= uniform(0.001, 20) #recovered
            scale_d= uniform(0.001, 20) #death  
            scale_h= uniform(0.001, 20) #hospitalized
            scale_i= uniform(0.001, 20) #ICU

            params = [Tu, Tmax, tau,    #1,2,3
                     taumir, taumih, taumid, #4,5,6
                    taumor, taumoh, taumod, taumoi, #7.8.9,10
                    taush, tausi, tausd, #11,12,13
                    tauhr, tauhi, tauhd, #14,15,16
                    tauir,tauid,  #17,18

                    rhomi, rhomo, rhos,   #19,20,21
                       
                    etamir, etamih, etamid,  #22,23,24
                    etamoi, etamor, etamoh, etamod, #25,26,27,28
                    etash, etasi, etasd,    #29,30,31
                         
                    lambdahr,lambdahi, lambdahd, #32,33,34
                    deltaid, deltair, #35,36
                    scale_r, #37
                    scale_d, #38
                    scale_h, #39
                    scale_i, #40
                    ]
            
            
            sol = Solution(params)
            sol.evaluate(eng,self.data)
 

            self.popMembers.append(sol)



    def __str__(self):
        str="all rmse(s): "
        for i in range(0,self.size):
            str = str + " rmse " + self.popMembers[i].averageRmse.__str__() + "\n mae " + self.popMembers[i].averageMae.__str__()  + "\n \n"
        return str


    def __getitem__(self,idx):
        return self.popMembers[idx]

#finding the best result:
    def get_best(self):
            fittest = self.popMembers[0]
            for i in range(self.size):
                if self.popMembers[i].fitness() <= fittest.fitness():
                    fittest =self.popMembers[i]
            return fittest


    def tournament_selection(self):
            #Tournament pool of size 4
            """ Tournament selection technique.
               How it works: The algorithm choose randomly four
               individuals from the population and returns the fittest one """

            random_id = int(random() * self.size)
            fittest = self.popMembers[random_id]
            for i in range(4):
                random_id = int(random() * self.size)
                if self.popMembers[random_id].fitness() < fittest.fitness():
                    fittest = self.popMembers[random_id]
            return fittest

    def evolve_population(self,eng,mutation_rate, crossover_rate):
        print("Evolving population...")
        new_population = Population(0, eng, self.data)


        # Do crossover over the entire population -> getting a new population of the same size
        '''
        How it works: 
        Two parents (individual 1 and individual 2) are chosen. 
        The algorithm take a random number. 
        If the number is less than crossover rate: 
            New individual inherent its value from individual 2
            Otherwise: New individual inherent its value from individual 1
        '''
        for i in range(self.size):
            individual1 = self.tournament_selection()
            if random() <= crossover_rate:
                individual2 = self.tournament_selection()
                new_individual = individual1.crossover(individual2)
                new_individual.evaluate(eng,self.data)
            else:
                new_individual = individual1
            new_population.popMembers.append(new_individual)
            new_population.size += 1
        
        # Do mutation randomly
        '''
        How it works: 
        The algorithm take a random number. 
        If the number is less than mutation rate: 
            The value of that parameters are going to be changed based on mutation rate 
        '''
        for i in range(self.size):
            if random() <= mutation_rate:
                new_population.popMembers[i].mutation(eng)
                new_population.popMembers[i].evaluate(eng,self.data)

        return new_population

    def read_data(self,path):
        data = pd.read_csv(path, comment='#',sep='\t', header=None)
        data = data.values
        return data
        
    
