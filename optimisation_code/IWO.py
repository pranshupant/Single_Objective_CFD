from constants import maxIt, Gen0, sigma_final, sigma_initial, exponent, nPop, gen
from airfoil_Class import airfoil#, baby_airfoil
import subprocess as sp
import os
import numpy as np
from reproduction import reproduction
from multiprocessing import Pool
import pickle
import matplotlib.pyplot as plt
import itertools

Airfoil = []
A = []
st = [0]
s = np.array(st)
Af = []
it = []


for i in range(Gen0):
    it.append(i)
#gen = 0

if gen == 0:
    print('Generation-%d STARTED'%gen)
    for i in range(Gen0):

        Airfoil.append(airfoil(0,i))
        Airfoil[i].ctrlPoints()
        Airfoil[i].bspline()
        Airfoil[i].write()
        Airfoil[i].savefig()
        Airfoil[i].show(gen, i)
        #Airfoil[i].camber(gen, i)

    def run(i):
        Airfoil[i].cfd()
        print(Airfoil[i].cost)
        #np.savetxt('../../cost-%d'%i, Airfoil[i].cost)

    y = Pool(5)
    #y.starmap(run, zip(itertools.repeat(Airfoil), it))
    y.map(run, range(Gen0))
    
    y.close()
    
    y.join()

    for i in range(Gen0):
    #    #Airfoil[i].savefig()
    #    #Airfoil[i].xFoil()
    #    Airfoil[i].cfd()
        Airfoil[i].cost = np.loadtxt('Results_CFD/Generation_0/cost-%d'%i)
        #run(i)

pickle_out = open("pickle/gen-%d.pickle"%gen, "wb")
pickle.dump(Airfoil, pickle_out)
pickle_out.close()

if gen == 0:
    gen = 1
    
if __name__ == "__main__":

    while gen < maxIt:

        G = np.linspace(0, gen, num=gen+1)

        print('Generation-%d STARTED'%gen)

        ng = gen - 1

        pickle_in = open("pickle/gen-%d.pickle"%ng, "rb")
        Airfoil = pickle.load(pickle_in)

        sigma = (((maxIt - float(gen-1))/maxIt)**exponent)*(sigma_initial - sigma_final) + sigma_final

        #print('SIGMA')
        #print(sigma)
        
        Airfoil.sort(key = lambda Airfoil: Airfoil.cost, reverse = True)

        if(gen==1):

            A.append(Airfoil[0].cost)
                  
        for i in range(len(Airfoil)):
            print(Airfoil[i].cost)

        del Airfoil[nPop:]
               

        #for i in range(len(Airfoil)):
            #print(Airfoil[i].cost)
    
        for k in range(nPop):
            Airfoil[k].copy(gen, s[0])
            Airfoil[k].copy_Results(gen, s[0])
            Airfoil[k].show(gen, s[0])
            #Airfoil[k].camber(gen, s[0])
            #print(Airfoil[k].cost)
            s[0] += 1 
           
        #y = Pool(4)
        #y.map(run, range(len(Airfoil)))
        #
        #y.close()
        #
        #y.join()

        for x in range(len(Airfoil)):
            reproduction(Airfoil, gen, sigma, x, s)    

        Airfoil.sort(key = lambda x: x.cost, reverse = True)

        A.append(Airfoil[0].cost)

        pickle_out = open("pickle/gen-%d.pickle"%gen, "wb")
        pickle.dump(Airfoil, pickle_out)
        pickle_out.close()
                
        gen += 1 
        s[0] = 0 

        T = len(G) - len(A)

        if T > 0:   
            A.reverse()
            for i in range(T):
                A.append(0)
            A.reverse()

        plt.plot(G, A,'k',linewidth=1.5,label='Max Cost')
        plt.xlabel('Generation')
        plt.ylabel('Cost')
        plt.legend(loc='best')
        plt.axis([0, 50, 0, 200])
        #plt.axis('equal')
        plt.title('IWO Convergence')
        #plt.savefig('/home/pranshu/Documents/Visual_Studio_Code/optimisation_code/Results_CFD/Generation_%i/Specie_%i/airfoil_%i-%i.png'%(self.__generation,self.__specie,self.__generation,self.__specie), bbox_inches = "tight")
        #copyfile('airfoil_%i-%i.png', '/home/pranshu/Documents/Visual_Studio_Code/optimisation_code/Results_XFoil/Generation_%i/Specie_%i/airfoil_%i-%i.png'%(self.__generation,self.__specie,self.__generation,self.__specie))
        plt.savefig('IWO_convergence_%d.svg'%gen, bbox_inches = 'tight')
        plt.close()
       
    print("DONE")