import copy
import random
import sys

from dna import Dna, memory
import matplotlib.pyplot as plt
from collections import deque

def setup():
    print("Setup START---------")

    memory('parametres',[])
    memory('file',open("./gene.csv","w+"))
    memory('file').write('Pu;rho;sigma1;sigma2;sigma3;tau;c;alpha;beta;gamma;Nc,theta;Ns;Fitness\n')
    memory("metaParametres", [])
    memory("metaParametresNb", 13)
    memory("metaParametresHistorique", [])

    memory("bestFintness", 89999999999999999999999999)
    memory("bestMetaParametres", [])

    memory("popSize", 5);
    memory("population", []);
    memory("matingpool", [])

    memory('parametres').append((50,150)) #Pu
    memory('parametres').append((0.0, 1.0))#rho
    memory('parametres').append((135, 135))#sig1
    memory('parametres').append((70, 70))#sig2
    memory('parametres').append((25, 25))#Sig3
    memory('parametres').append((0, 100))#tau
    memory('parametres').append((0.0, 1.0))#c
    memory('parametres').append((0.0, 1.0))#alpha
    memory('parametres').append((0.0, 1.0))#beta
    memory('parametres').append((0.0, 1.0))#gamma
    memory('parametres').append((100, 2000))#Nc
    memory('parametres').append((0.5, 0.5))#theta
    memory('parametres').append((10, 10))#Ns


    for i in range(0,memory("popSize")):
        gene = []
        gene.append(random.randint(50, 150)) #Pu
        gene.append(random.randint(0, 100)/100) #rho
        gene.append(135) #sigma1
        gene.append(70) #sigma2
        gene.append(25) #sigma3
        gene.append(random.randint(0, 100)) #tau
        gene.append(random.randint(0, 100)/100) #c
        alpha = random.randint(0, 100)/100
        beta = random.randint(0, 100)/100
        gamma = 1-alpha-beta
        while(0 < gamma < 1):
            alpha = random.randint(0, 100)/100
            beta = random.randint(0, 100)/100
            gamma = 1-alpha-beta
        gene.append(alpha) #alpha
        gene.append(beta) #beta
        gene.append(gamma) #gamma
        gene.append(random.randint(100, 2000)) #Nc
        gene.append(0.5) #theta
        gene.append(10) #Ns

        memory("population").append(Dna(gene))



    print("Setup END-----------")


def evaluate():
    for p in memory("population"):
        p.calculateFitness()

    indexBest = -1
    maxfit = memory("population")[0].fitness

    for i, p in enumerate(memory("population")):
        if p.fitness > maxfit:
            maxfit = p.fitness
            indexBest=i


    if indexBest >= 0:
        memory("bestMetaParametres", memory("population")[indexBest].gene)
        memory("metaParametresHistorique").append(memory("population")[indexBest].gene)
        memory('file').write(str(memory("population")[indexBest].gene[0])+";")
        memory('file').write(str(memory("population")[indexBest].gene[1])+";")
        memory('file').write(str(memory("population")[indexBest].gene[2]) + ";")
        memory('file').write(str(memory("population")[indexBest].gene[3]) + ";")
        memory('file').write(str(memory("population")[indexBest].gene[4]) + ";")
        memory('file').write(str( memory("population")[indexBest].gene[5]) + ";")
        memory('file').write(str( memory("population")[indexBest].gene[6]) + ";")
        memory('file').write(str(memory("population")[indexBest].gene[7]) + ";")
        memory('file').write(str(memory("population")[indexBest].gene[9]) + ";")
        memory('file').write(str( memory("population")[indexBest].gene[10]) + ";")
        memory('file').write( str(memory("population")[indexBest].gene[11]) + ";")
        memory('file').write(str( memory("population")[indexBest].gene[12]) + ";")
        memory('file').write(str(maxfit) + ";\n")


    for p in memory("population"):
        p.fitness = p.fitness / maxfit

    memory("matingpool", [])
    for p in memory('population'):
        n = p.fitness * 10
        for i in range(0, int(n)):
            memory("matingpool").append(p)


def selection():
    newPopulation = []
    for i in range(0, memory("popSize")):
        parentA = copy.deepcopy(memory("matingpool")[random.randint(0, len(memory("matingpool")) - 1)])
        parentB = copy.deepcopy(memory("matingpool")[random.randint(0, len(memory("matingpool")) - 1)])
        child = parentA.crossover(parentB)
        newPath = Dna(child)
        newPath.mutation(0.05)
        newPopulation.append(newPath)

    memory('population', newPopulation)


def displaySolution():
    print("meta",memory("metaParametresHistorique"))
    Pu= deque(maxlen=40)
    rhp= deque(maxlen=40)
    sg1= deque(maxlen=40)
    sg2= deque(maxlen=40)
    sg3= deque(maxlen=40)
    to = deque(maxlen=40)
    c = deque(maxlen=40)
    alpha = deque(maxlen=40)
    beta = deque(maxlen=40)
    gamma = deque(maxlen=40)
    nc = deque(maxlen=40)
    theta = deque(maxlen=40)
    ns = deque(maxlen=40)

    for h in memory("metaParametresHistorique"):
        Pu.append(h[0])
        rhp.append(h[1])
        sg1.append(h[2])
        sg2.append(h[3])
        sg3.append(h[4])
        to.append(h[5])
        c.append(h[6])
        alpha.append(h[7])
        beta.append(h[8])
        gamma.append(h[9])
        nc.append(h[10])
        theta.append(h[11])
        ns.append(h[12])

        plt.plot(Pu)
        plt.scatter(range(len(Pu)), Pu, c='#c12e2e')

        plt.plot(rhp)
        plt.scatter(range(len(rhp)), rhp, c='#48c569')

        plt.plot(sg1)
        plt.scatter(range(len(sg1)), sg1, c='#5bc12e')
        plt.plot(sg2)
        plt.scatter(range(len(sg2)), sg2, c='#6ea49b')
        plt.plot(sg3)
        plt.scatter(range(len(sg3)), sg3, c='#4166e3')

        plt.plot(to)
        plt.scatter(range(len(to)), to, c='#d964e7')

        plt.plot(c)
        plt.scatter(range(len(c)), c, c='#bbb1bd')

        plt.plot(alpha)
        plt.scatter(range(len(alpha)), alpha, c='#dea68e')

        plt.plot(beta)
        plt.scatter(range(len(beta)), beta, c='#000000')

        plt.plot(gamma)
        plt.scatter(range(len(gamma)), gamma, c='#16f8ff')

        plt.plot(nc)
        plt.scatter(range(len(nc)), nc, c='#c2478a')

        plt.plot(theta)
        plt.scatter(range(len(theta)), theta, c='#c14343')

        plt.plot(ns)
        plt.scatter(range(len(ns)), ns, c='#16f8ff')

        # DRAW, PAUSE AND CLEAR
        plt.draw()
        plt.pause(0.1)
        plt.clf()



def run():


    evaluate()
    selection()
    #displaySolution()


if __name__=="__main__":
    setup()
    nbGeneration=200
    for i in range(0,nbGeneration):
        run()
