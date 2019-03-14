from constants import maxIt, Gen0, sigma_final, sigma_initial, exponent, nPop
from airfoil_Class import airfoil#, baby_airfoil
import subprocess as sp
import os
import numpy as np
from NS_reproduction import *
from multiprocessing import pool

Airfoil = []
st = [0]
s = np.array(st)
gen = 0


for i in range(Gen0):
    
    Airfoil.append(airfoil(0,i))
    Airfoil[i].ctrlPoints()
    Airfoil[i].bspline()
    Airfoil[i].write()
    Airfoil[i].savefig()
    Airfoil[i].show(gen, i)
        
for i in range(Gen0):
    #Airfoil[i].savefig()
    Airfoil[i].xFoil()
    #Airfoil[i].random()

    #Airfoil[i].camber(gen, i)
    Airfoil[i].mean_camber(gen, i)
    
    #Airfoil[i].cfd()
    print(Airfoil[i].cost)

    gen = 1

if __name__ == "__main__":

    while gen < maxIt:

        Cost0 = []
        Cost1 = []
        Cost2 = []

        for j in range(len(Airfoil)):
            Cost0.append(Airfoil[j].cost)
            Cost1.append(-Airfoil[j].max_Camber)
            Cost2.append(Airfoil[j].max_Camber)
        print('******')
            #print(Cost0)

        plt.scatter(Cost0,Cost2,s=5,c='black')
	    #plt.scatter(Cost[0],Cost[1],s=3.5,c='blue')
        plt.xlim(-25, 250)
        plt.ylim(-5, 25)
        plt.savefig('Pics/%i.svg'%(gen))
        #plt.close() 

        #nsga_Airfoil = copy.deepcopy(Airfoil)
        r = []
        NDSa = []
        total = 0
        NDSa = Rank_Assign(Airfoil, Cost0, Cost1)
        l = len(NDSa)
        for i in range(len(NDSa)):
            count = len(NDSa[i])
            total += count
            r.append(total)
        
        sigma = (((maxIt - float(gen-1))/maxIt)**exponent)*(sigma_initial - sigma_final) + sigma_final

        #sigma1=(((max(Rank_List) - float(Specie_List[i].Rank))/max(Rank_List))**Exponent1 )* (sigma_best - sigma_worst) + sigma_worst

        #sigma = sigma + sigma1

        print('SIGMA')
        print(sigma)

        print('RANK')
        for i in range(len(Airfoil)):
            print(Airfoil[i].rank)

        Airfoil.sort(key = lambda Airfoil: Airfoil.cost, reverse = True)
        #Airfoil.sort(key = lambda Airfoil: Airfoil.rank)

        for i in range(len(Airfoil)):
            print('-----------')
            print(Airfoil[i].rank)
            print('-----------')
            print(Airfoil[i].cost)
            print(Airfoil[i].max_Camber)
            
        S_Cost0 = []
        S_Cost1 = []

        del Airfoil[nPop:]

        for j in range(len(Airfoil)):
            S_Cost0.append(Airfoil[j].cost)
            S_Cost1.append(Airfoil[j].max_Camber)

        plt.scatter(S_Cost0,S_Cost1,s=5,c='red')
	    #plt.scatter(Cost[0],Cost[1],s=3.5,c='blue')
        plt.xlim(-50, 250)
        plt.ylim(-5, 30)
        plt.savefig('Pics/%i.svg'%(gen))
        plt.close() 
               

        for i in range(len(Airfoil)):
            print(Airfoil[i].cost)
    
        for k in range(nPop):
            Airfoil[k].copy(gen, s[0])
            Airfoil[k].copy_Results(gen, s[0])
            Airfoil[k].show(gen, s[0])
            #Airfoil[k].camber(gen, s[0])
            Airfoil[k].mean_camber(gen, s[0])

            s[0] += 1 

                
        for x in range(len(Airfoil)):
            reproduction(Airfoil, gen, sigma, x, s, r, l)    
            #Airfoil[x].mutate(sigma)

        #Airfoil.sort(key = lambda x: x.cost, reverse = True)
        #Airfoil.sort(key = lambda Airfoil: Airfoil.rank)

        gen += 1 
        s[0] = 0      

        