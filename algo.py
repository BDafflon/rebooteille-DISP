import copy
import random
import core
from pygame.math import Vector2
from dna import Dna
import matplotlib.pyplot as plt
from collections import deque

def setup():
    print("Setup START---------")
    core.fps = 360
    core.WINDOW_SIZE = [800, 800]

    core.memory('file',open("./gene.csv","w+"))
    core.memory('file').write('Pu;rho;sigma1;sigma2;sigma3;tau;c;alpha;beta;gamma;Nc,theta;Ns;\n')
    core.memory("metaParametres", [])
    core.memory("metaParametresNb", 13)
    core.memory("metaParametresHistorique", [])

    core.memory("bestFintness", 89999999999999999999999999)
    core.memory("bestMetaParametres", [])

    core.memory("popSize", 5);
    core.memory("population", []);
    core.memory("matingpool", [])


    for i in range(0,core.memory("popSize")):
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

        core.memory("population").append(Dna(gene))



    print("Setup END-----------")


def evaluate():
    for p in core.memory("population"):
        p.calculateFitness()

    indexBest = -1
    maxfit = core.memory("population")[0].fitness

    for i, p in enumerate(core.memory("population")):
        if p.fitness > maxfit:
            maxfit = p.fitness
            indexBest=i


    if indexBest >= 0:
        core.memory("bestMetaParametres", core.memory("population")[indexBest].gene)
        core.memory("metaParametresHistorique").append(core.memory("population")[indexBest].gene)
        core.memory('file').write(str(core.memory("population")[indexBest].gene[0])+";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[1])+";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[2]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[3]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[4]) + ";")
        core.memory('file').write(str( core.memory("population")[indexBest].gene[5]) + ";")
        core.memory('file').write(str( core.memory("population")[indexBest].gene[6]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[7]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[9]) + ";")
        core.memory('file').write(str( core.memory("population")[indexBest].gene[10]) + ";")
        core.memory('file').write( str(core.memory("population")[indexBest].gene[11]) + ";")
        core.memory('file').write(str( core.memory("population")[indexBest].gene[12]) + ";\n")


    for p in core.memory("population"):
        p.fitness = p.fitness / maxfit

    core.memory("matingpool", [])
    for p in core.memory('population'):
        n = p.fitness * 10
        for i in range(0, int(n)):
            core.memory("matingpool").append(p)


def selection():
    newPopulation = []
    for i in range(0, core.memory("popSize")):
        parentA = copy.deepcopy(core.memory("matingpool")[random.randint(0, len(core.memory("matingpool")) - 1)])
        parentB = copy.deepcopy(core.memory("matingpool")[random.randint(0, len(core.memory("matingpool")) - 1)])
        child = parentA.crossover(parentB)
        newPath = Dna(child)
        #newPath.mutation(0.05)
        newPopulation.append(newPath)

    core.memory('population', newPopulation)


def displaySolution():
    print("meta",core.memory("metaParametresHistorique"))
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

    for h in core.memory("metaParametresHistorique"):
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


    '''start=i*10
        h=core.memory("metaParametresHistorique")[len(core.memory("metaParametresHistorique"))-i-1]
        Pu=  core.Math.map(h[0],50,150,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((255,0,0),(start,800-Pu,10,Pu))
        rho = core.Math.map(h[1],0,1,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((0, 255, 0), (start, 800 - Pu-rho, 10, rho))
        sg1=core.Math.map(h[2],0,200,0,core.WINDOW_SIZE[1]/13)
        core.Draw.rect((0, 0, 255), (start, 800 - Pu - rho-sg1, 10, sg1))
        sg2=core.Math.map(h[3],0,100,0,core.WINDOW_SIZE[1]/13)
        core.Draw.rect((255, 0, 255), (start, 800 - Pu - rho - sg1-sg2, 10, sg2))
        sg3=core.Math.map(h[4],0,50,0,core.WINDOW_SIZE[1]/13)
        core.Draw.rect((0, 255, 255), (start, 800 - Pu - rho - sg1 - sg2-sg3, 10, sg3))
        to=core.Math.map(h[5],0,100,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((255, 255, 0), (start, 800 - Pu - rho - sg1 - sg2-sg3-to, 10, to))
        c=core.Math.map(h[6],0,1,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((255, 255, 255), (start, 800 - Pu - rho - sg1 - sg2 - sg3 - to-c, 10, c))
        alpha=core.Math.map(h[7],0,1,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((100, 100, 100), (start, 800 - Pu - rho - sg1 - sg2 - sg3 - to-c-alpha, 10, alpha))
        beta=core.Math.map(h[8], 0, 1, 0, core.WINDOW_SIZE[1]/13)  # 50-150
        core.Draw.rect((250, 100, 0), (start, 800 - Pu - rho - sg1 - sg2 - sg3 - to - c - alpha-beta, 10, beta))
        gamma = core.Math.map(h[9],0,1,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((250, 100, 0), (start, 800 - Pu - rho - sg1 - sg2 - sg3 - to - c - alpha-beta-gamma, 10, gamma))
        nc = core.Math.map(h[10],100,2000,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((0, 100, 250), (start, 800 - Pu - rho - sg1 - sg2 - sg3 - to - c - alpha-beta-gamma-nc, 10, nc))
        theta = core.Math.map(h[11],0,1,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((40, 250, 10), (start, 800 - Pu - rho - sg1 - sg2 - sg3 - to - c - alpha-beta-gamma-nc-theta, 10,theta ))
        ns = core.Math.map(h[12],0,20,0,core.WINDOW_SIZE[1]/13)  #50-150
        core.Draw.rect((100, 0, 200), (start, 800 - Pu - rho - sg1 - sg2 - sg3 - to - c - alpha-beta-gamma-nc-theta-ns, 10,ns ))
'''





def run():
    core.cleanScreen()

    evaluate()
    selection()

    displaySolution()

core.main(setup, run)
