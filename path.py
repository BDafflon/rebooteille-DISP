import random
from math import floor
from alns.ALNS import ALNS
from instance.parser import parse


class Path:
    def __init__(self,dna):
        self.dna = dna
        self.fitness = 0


    def calculateDistance(self,cities):
        dist = 0
        for i in range(0,len(self.dna)-1):
            dist+=cities[self.dna[i]].distance_to(cities[self.dna[i+1]])
        return dist

    def calculateFitness(self,cities):
        """
        dist = 0
        for i in range(0,len(self.dna)-1):
            dist+=cities[self.dna[i]].distance_to(cities[self.dna[i+1]])

        self.fitness = 1/ (pow(dist, 8) + 1)
        """
        instance = parse("./data/Medium6.xlsx", fileDistPath="./data/MatricesDT.xlsx")
        alns = ALNS(instance)
        solution = alns.solve(cities[0], cities[1], cities[2], cities[3], cities[4], cities[5], cities[6], cities[7], cities[8], cities[9], cities[10], cities[11], cities[12])
        self.fitness = solution.getCost()

    def crossover(self,partner):
        gene=[]
        start = floor(random.randint(0, len(self.dna)-1))
        end = floor(random.randint(start+1, len(self.dna)))
        for i in range(start, end):
            gene.append(self.dna[i])

        for i in partner.dna:
            if i not in gene:
                gene.append(i)
        return gene
"""
    def mutation(self,range):
        if random.uniform(0,1)<range:
            i = random.randint(0,len(self.dna)-1)
            j = random.randint(0,len(self.dna)-1)
            c = self.dna[i]
            self.dna[i] = self.dna[j]
            self.dna[j] = c
"""
