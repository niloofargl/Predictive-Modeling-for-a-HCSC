import matlab
#import pandas as pd
from statistics import mean
from random import random, randint,uniform
'''
Here, we classified the parameters in different sublists
for mutation and crossover:
*Note: the definition of each parameter is in Population.py
'''
class Solution:
    def __init__(self,parameters):
        self.parameters = parameters
        self.NestedParameters = [0] * 28
        index = 0

        #The first 18 parameters in Population.py file:
        for i in range(18):
            self.NestedParameters[i] = self.parameters[i]
            index +=1

        #Rho parameters (rhomi,rhos, rhomo)
        sublist=[]
        for i in range(18,21):
            sublist.append(self.parameters[i])
        self.NestedParameters[index] = sublist
        index += 1


        #Etami parameters (etamir,etamid,etamih)
        sublist = []
        for i in range(21, 24):
            sublist.append(self.parameters[i])
        self.NestedParameters[index] = sublist
        index += 1


        #Etamo parameters (etamor, etamoi, etamod, etamoh)
        sublist = []
        for i in range(24, 28):
            sublist.append(self.parameters[i])
        self.NestedParameters[index] = sublist
        index += 1

        #Etas parameters (etash, etasd, etasi)
        sublist = []
        for i in range(28, 31):
            sublist.append(self.parameters[i])
        self.NestedParameters[index] = sublist
        index += 1

        #Lambdah parameters (lambdahr,lambdahd, lambdahi)
        sublist = []
        for i in range(31, 34):
            sublist.append(self.parameters[i])
        self.NestedParameters[index] = sublist
        index += 1


        #Delta parameters (deltaid, deltair)
        sublist = []
        for i in range(34, 36):
            sublist.append(self.parameters[i])
        self.NestedParameters[index] = sublist
        index += 1

        # scale_r parameter
        self.NestedParameters[index] = self.parameters[36]
        index += 1

        # scale_d parameter
        self.NestedParameters[index] = self.parameters[37]
        index += 1

        # scale_h parameter
        self.NestedParameters[index] = self.parameters[38]
        index += 1

        # scale_i parameter
        self.NestedParameters[index] = self.parameters[39]
        index += 1

        '''Error'''
        #Initial error rate
        self.rmse = [0,0,0,0]       #rmse: Root-mean-square error
        self.mae = [0, 0, 0, 0]     #mae: Mean absolute error
        self.wape = [0, 0, 0, 0]    #wape: Weighted absolute percentage error
        self.mape = [0, 0, 0, 0]    #mape: Mean absolute percentage error
        
        '''
        *** NOTE: The results are based on WAPE error.
        '''
       
       #Initial Average:
        self.averageRmse=0
        self.averageMae = 0
        self.averageWape = 0
        self.averageMape = 0
       
    # The definition of each label mentioned in Population.py file
    def __str__(self) -> str:
        txt = ""
        labels = ["Tu" , "Tmax" , "tau" ,
               "taumir", "taumih", "taumid",
                "taumor", "taumoh", "taumod", "taumoi",
                "taush", "tausi", "tausd",
                "tauhr", "tauhi", "tauhd",
                "tauir","tauid",  
                "rhomi", "rhomo", "rhos",
                "etamir", "etamih", "etamid",
                "etamoi", "etamor", "etamoh", "etamod",
                "etash", "etasi", "etasd", 
                "lambdahr","lambdahi", "lambdahd",
                "deltaid", "deltair", 'scale_r' , 'scale_d' , 'scale_h' , 'scale_i' ]
        for label, val in zip(labels,self.parameters):
            txt+= f"{label}:{val}\n"
        return txt

        
    def evaluate(self, eng, data , isshow = 0):
        self.parameters = []
        for i in range(0, len(self.NestedParameters)):
            if isinstance(self.NestedParameters[i], list):
                for j in range(0, len(self.NestedParameters[i])):
                    self.parameters.append(self.NestedParameters[i][j])
            else:
                self.parameters.append(self.NestedParameters[i])


       # Input data 
        daily_smooth, recovered_smooth, death, hospital_smooth , icu_smooth = data

        ret = eng.plotsmape(matlab.double(self.parameters),
                        matlab.double(list(daily_smooth.astype(float))), 
                        matlab.double(list(recovered_smooth.astype(float))), 
                        matlab.double(list(death.astype(float))),
                        matlab.double(list(hospital_smooth.astype(float))),
                        matlab.double(list(icu_smooth.astype(float))),isshow)

        # The location of each error in the error list
        self.rmse = ret[0][0:4]
        self.mae = ret[0][4:8]
        self.wape = ret[0][8:12]
        self.mape = ret[0][12:16]
        


        self.averageRmse = mean(self.rmse)
        self.averageMae = mean(self.mae)
        self.averageWape = mean(self.wape)
        self.averageMape = mean(self.mape)
        



    def DisplayPlots(self, eng):

        ret = eng.modelwithWAPECompleteDataPlotsCopied(matlab.double(self.parameters))

    def fitness(self):
        return self.averageWape


    ''' Mutation:
    How it works:
            The new random value is going to be found in a bigger range. 
            It helps the algorithm to find the best result even out of the proposed initial range.
    ''' 
    def mutation(self, eng):
        index = randint(2,27)
        #print("original param", self.NestedParameters)
        ranges = [None, None, (2, 14) , 
        (2, 14), 
        (2, 14),  
        (2, 14),   
        (2, 14),   
        (2, 14), 
        (2, 14),  
        (2, 14),   
        (2, 14),
        (2, 14), 
        (2, 14),  
        (2, 14),   
        (2, 14),
        (2, 14), 
        (2, 14),  
           ]     
        if index <= 17 :
            
            newdelay = randint(1,30) 
            self.NestedParameters[index] = newdelay

        elif index >=24 :
            
            newscale = uniform(0.001, 3)
            self.NestedParameters[index] = newscale
            
        else:
            
            sublist = []
            for i in range(0, len(self.NestedParameters[index])):
                sublist.append(random())
            self.NestedParameters[index] = sublist
            # normalize to sum equal to one
            sum = 0
            for i in range(0, len(self.NestedParameters[index])):
                sum += self.NestedParameters[index][i]
            for i in range(0, len(self.NestedParameters[index])):
                self.NestedParameters[index][i] = self.NestedParameters[index][i]/sum

        

    '''Crossover:
                The "for" loop illustrates the way that the algorithm chooses the gene from each parent '''
    def crossover(self, sol2):
        empty_param = [0] * 40
        new_sol = Solution(empty_param)
        for i in range(28):
            if random() <= 0.5:
                new_sol.NestedParameters[i] = self.NestedParameters[i]
            else:
                new_sol.NestedParameters[i] = sol2.NestedParameters[i]

        return new_sol
