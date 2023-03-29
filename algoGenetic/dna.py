import random
from math import floor

import core
from alns.ALNS import ALNS
from instance.parser import parse


class Dna:
    def __init__(self, gene):
        self.gene = gene
        self.fitness = 0

    def calculateDistance(self, cities):
        dist = 0
        for i in range(0, len(self.dna) - 1):
            dist += cities[self.dna[i]].distance_to(cities[self.dna[i + 1]])
        return dist

    def calculateFitness(self):
        instance = parse("data/Medium6/")
        alns = ALNS(instance)
        meanCost = 0
        for i in range(10):
            solution = alns.solve(100, 0.33, 130, 70, 25, self.gene[0], self.gene[1], self.gene[2],
                                  self.gene[3], self.gene[4], 2000, self.gene[5], self.gene[6])
            meanCost += solution.getCost()
        self.fitness = meanCost/10

    def crossover(self, partner):
        gene = []
        start = floor(random.randint(0, len(self.gene) - 1))
        end = floor(random.randint(start + 1, len(self.gene)))
        for i in range(0, len(self.gene)):
            if start < i < end:
                gene.append(self.gene[i])
            else:
                gene.append(partner.gene[i])

        return gene

    def mutation(self, range):
        if random.uniform(0, 1) < range:
            print("mutation")
            i = random.randint(0, len(self.gene) - 1)
            if 1 < i < 5:
                alpha = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                beta = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                gamma = 1 - alpha - beta
                while gamma < 0 or 1 < gamma:
                    alpha = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                    beta = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                    gamma = 1 - alpha - beta

                self.gene[2] = alpha
                self.gene[3] = beta
                self.gene[4] = gamma
            else:
                if isinstance(core.memory('parametres')[i][0], int):
                    self.gene[i] = random.randint(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
                else:
                    if isinstance(core.memory('parametres')[i][0], float):
                        self.gene[i] = random.uniform(core.memory('parametres')[i][0], core.memory('parametres')[i][1])
