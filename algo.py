import copy
import random
import core
from pygame.math import Vector2
from path import Path


def setup():
    print("Setup START---------")
    core.fps = 360
    core.WINDOW_SIZE = [800, 800]

    core.memory("cities", [])
    core.memory("citiesNb", 13)

    core.memory("bestDistance", 89999999999999999999999999)
    core.memory("bestPath", [])

    core.memory("popSize", 500);
    core.memory("population", []);
    core.memory("matingpool", [])

    order = [i for i in range(0, core.memory("citiesNb"))]
    core.memory("cities").append(random.randint(50, 150)) #Pu
    core.memory("cities").append(random.randint(0, 100)/100) #rho
    core.memory("cities").append(135) #sigma1
    core.memory("cities").append(70) #sigma2
    core.memory("cities").append(25) #sigma3
    core.memory("cities").append(random.randint(0, 100)) #tau
    core.memory("cities").append(random.randint(0, 100)/100) #c
    alpha = random.randint(0, 100)/100
    beta = random.randint(0, 100)/100
    gamma = 1-alpha-beta
    while(0 < gamma < 1):
        alpha = random.randint(0, 100)/100
        beta = random.randint(0, 100)/100
        gamma = 1-alpha-beta
    core.memory("cities").append(alpha) #alpha
    core.memory("cities").append(beta) #beta
    core.memory("cities").append(gamma) #gamma
    core.memory("cities").append(random.randint(100, 2000)) #Nc
    core.memory("cities").append(0.5) #theta
    core.memory("cities").append(10) #Ns

    for i in range(0, core.memory("popSize")):
        l = copy.deepcopy(order)
        random.shuffle(l)
        core.memory("population").append(Path(l))

    core.memory("bestPath", order)

    print("Setup END-----------")


def evaluate():
    for p in core.memory("population"):
        p.calculateFitness(core.memory("cities"))

    indexBest = -1
    maxfit = core.memory("population")[0].fitness

    for i, p in enumerate(core.memory("population")):
        if p.fitness > maxfit:
            maxfit = p.fitness
        if p.calculateDistance(core.memory("cities")) < core.memory("bestDistance"):
            indexBest = i
            core.memory("bestDistance", p.calculateDistance(core.memory("cities")))

    print(core.memory("bestDistance"))
    if indexBest >= 0:
        core.memory("bestPath", core.memory("population")[indexBest].dna)

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
        newPath = Path(child)
        #newPath.mutation(0.05)
        newPopulation.append(newPath)

    core.memory('population', newPopulation)


def run():
    core.cleanScreen()

    evaluate()
    selection()

    if core.getKeyPressList("r"):
        reset()

    if core.getMouseLeftClick():
        for p in core.memory("population"):
            p.dna.append(len(p.dna))
        core.memory("cities").append(Vector2(core.getMouseLeftClick()[0],core.getMouseLeftClick()[1]))
        core.memory("bestPath").append(len(core.memory("bestPath")))
        core.memory("bestDistance", core.memory("bestDistance")+100000)

    for city in core.memory("cities"):
        core.Draw.circle((255, 255, 255), city, 2)

    bestPathOrder = []
    for i in core.memory("bestPath"):
        bestPathOrder.append(core.memory("cities")[i])

    core.Draw.lines((200, 0, 0), False, bestPathOrder, 2)


def reset():
    core.memory("cities", [])

    core.memory("bestDistance", 89999999999999999999999999)
    core.memory("bestPath", [])

    core.memory("popSize", 500);
    core.memory("population", []);
    core.memory("matingpool", [])

    order = []
    for i in range(0, core.memory("citiesNb")):
        core.memory("cities").append(
            Vector2(random.randint(0, core.WINDOW_SIZE[0]), random.randint(0, core.WINDOW_SIZE[1])))
        order.append(i)

    for i in range(0, core.memory("popSize")):
        l = copy.deepcopy(order)
        random.shuffle(l)
        core.memory("population").append(Path(l))

    core.memory("bestPath", order)


core.main(setup, run)
