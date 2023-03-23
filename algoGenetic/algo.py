import copy
import random
import core
from dna import Dna
import matplotlib.pyplot as plt
from collections import deque


def setup():
    print("Setup START---------")
    core.fps = 360
    core.WINDOW_SIZE = [800, 800]

    core.memory('parametres', [])
    core.memory('file', open("algoGenetic/gene.csv", "w+"))
    core.memory('file').write('Pu;rho;tau;c;alpha;beta;gamma;theta;Ns;Fitness\n')
    core.memory("metaParametres", [])
    core.memory("metaParametresNb", 13)
    core.memory("metaParametresHistorique", [])

    core.memory("bestFintness", 89999999999999999999999999)
    core.memory("bestMetaParametres", [])

    core.memory("popSize", 5)
    core.memory("population", [])
    core.memory("matingpool", [])

    # bornes min/max pour mutation
    core.memory('parametres').append((100, 100))  # Pu
    core.memory('parametres').append((0.33, 0.33))  # rho
    core.memory('parametres').append((0, 100))  # tau
    core.memory('parametres').append((0.0, 1.0))  # c
    core.memory('parametres').append((0.0, 1.0))  # alpha
    core.memory('parametres').append((0.1, 1.0))  # beta
    core.memory('parametres').append((0.1, 1.0))  # gamma
    core.memory('parametres').append((0.5, 0.5))  # theta
    core.memory('parametres').append((10, 10))  # Ns

    for j in range(0, core.memory("popSize")):
        gene = list(range(0, 9))
        for i in range(0, 9):
            if 3 < i < 7:
                alpha = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                beta = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                gamma = 1 - alpha - beta
                while gamma <= 0 or 1 < gamma:
                    alpha = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                    beta = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                    gamma = 1 - alpha - beta

                gene[4] = alpha
                gene[5] = beta
                gene[6] = gamma
            else:
                if isinstance(core.memory('parametres')[i][0], int):
                    gene[i] = random.randint(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                else:
                    if isinstance(core.memory('parametres')[i][0], float):
                        gene[i] = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])

        core.memory("population").append(Dna(gene))

    print("Setup END-----------")


def evaluate():
    for p in core.memory("population"):
        p.calculateFitness()

    indexBest = -1
    minfit = core.memory("population")[0].fitness
    maxfit = core.memory("population")[0].fitness

    for i, p in enumerate(core.memory("population")):
        if p.fitness <= minfit:
            minfit = p.fitness
            indexBest = i

        if p.fitness > maxfit:
            maxfit = p.fitness

    if indexBest >= 0:
        core.memory("bestMetaParametres", core.memory("population")[indexBest].gene)
        core.memory("metaParametresHistorique").append(core.memory("population")[indexBest].gene)
        core.memory('file').write(str(core.memory("population")[indexBest].gene[0]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[1]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[2]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[3]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[4]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[5]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[6]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[7]) + ";")
        core.memory('file').write(str(core.memory("population")[indexBest].gene[8]) + ";")
        core.memory('file').write(str(minfit) + ";\n")

    for p in core.memory("population"):
        f = core.Math.map(p.fitness, minfit, maxfit, 1, 0)
        print(p.fitness, ' ', f)
        p.fitness = f

    core.memory("matingpool", [])
    for p in core.memory('population'):
        n = p.fitness * 10
        for i in range(0, int(n)+1):
            core.memory("matingpool").append(p)


def selection():
    newPopulation = []
    for i in range(0, core.memory("popSize")):
        parentA = copy.deepcopy(core.memory("matingpool")[random.randint(0, len(core.memory("matingpool")) - 1)])
        parentB = copy.deepcopy(core.memory("matingpool")[random.randint(0, len(core.memory("matingpool")) - 1)])
        child = parentA.crossover(parentB)
        newPath = Dna(child)
        newPath.mutation(0.05)
        newPopulation.append(newPath)

    core.memory('population', newPopulation)


def displaySolution():
    print("meta", core.memory("metaParametresHistorique"))
    Pu = deque(maxlen=40)
    rhp = deque(maxlen=40)
    to = deque(maxlen=40)
    c = deque(maxlen=40)
    alpha = deque(maxlen=40)
    beta = deque(maxlen=40)
    gamma = deque(maxlen=40)
    theta = deque(maxlen=40)
    ns = deque(maxlen=40)

    for h in core.memory("metaParametresHistorique"):
        Pu.append(h[0])
        rhp.append(h[1])
        to.append(h[2])
        c.append(h[3])
        alpha.append(h[4])
        beta.append(h[5])
        gamma.append(h[6])
        theta.append(h[7])
        ns.append(h[8])

        plt.plot(Pu)
        plt.scatter(range(len(Pu)), Pu, c='#c12e2e')

        plt.plot(rhp)
        plt.scatter(range(len(rhp)), rhp, c='#48c569')

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

        plt.plot(theta)
        plt.scatter(range(len(theta)), theta, c='#c14343')

        plt.plot(ns)
        plt.scatter(range(len(ns)), ns, c='#16f8ff')

        # DRAW, PAUSE AND CLEAR
        plt.draw()
        plt.pause(0.1)
        plt.clf()


def run():
    core.cleanScreen()

    evaluate()
    selection()

    displaySolution()


core.main(setup, run)
