import random
import sys
from math import floor


from alns.ALNS import ALNS
from instance.parser import parse


memoryStorage = {}
def memory(key: object, value: object = None) -> object:
    global memoryStorage
    if " " in key:
        sys.stderr.write("ERREUR : Espace interdit dans les noms de variable : " + key + "\n")
        sys.exit()
    if value is not None:
        memoryStorage[key] = value
    else:
        try:
            return memoryStorage[key]
        except:
            sys.stderr.write("ERREUR : Nom de variable inconnue : " + key)
            sys.exit()

class Dna:
    def __init__(self,gene):
        self.gene = gene
        self.fitness = 0


    def calculateDistance(self,cities):
        dist = 0
        for i in range(0,len(self.dna)-1):
            dist+=cities[self.dna[i]].distance_to(cities[self.dna[i+1]])
        return dist

    def calculateFitness(self):
        """
        dist = 0
        for i in range(0,len(self.dna)-1):
            dist+=cities[self.dna[i]].distance_to(cities[self.dna[i+1]])

        self.fitness = 1/ (pow(dist, 8) + 1)
        """
        instance = parse("./data/Medium6.xlsx", fileDistPath="./data/MatricesDT.xlsx")
        alns = ALNS(instance)
        solution = alns.solve(self.gene[0], self.gene[1], self.gene[2], self.gene[3], self.gene[4], self.gene[5], self.gene[6], self.gene[7], self.gene[8], self.gene[9], self.gene[10], self.gene[11], self.gene[12])
        self.fitness = solution.getCost()

    def crossover(self,partner):
        gene=[]
        start = floor(random.randint(0, len(self.gene)-1))
        end = floor(random.randint(start+1, len(self.gene)))
        for i in range(0, len(self.gene)):
            if start<i<end:
                gene.append(self.gene[i])
            else:
                gene.append(partner.gene[i])


        return gene

    def mutation(self,range):
        if random.uniform(0,1)<range:
            print("mutation")
            i = random.randint(0,len(self.gene)-1)
            if 6<i<9:
                alpha = random.uniform(memory('parametres')[i][0],memory('parametres')[i][1])
                beta = random.uniform(memory('parametres')[i][0],memory('parametres')[i][1])
                gamma = 1 - alpha - beta
                while (0 < gamma < 1):
                    alpha = random.uniform(memory('parametres')[i][0],memory('parametres')[i][1])
                    beta = random.uniform(memory('parametres')[i][0],memory('parametres')[i][1])
                    gamma = 1 - alpha - beta

                self.gene[7] = alpha
                self.gene[8] = beta
                self.gene[9] = gamma
            else:
                if isinstance(memory('parametres')[i][0], int):
                    self.gene[i] = random.randint(memory('parametres')[i][0],memory('parametres')[i][1])
                else:
                    if isinstance(memory('parametres')[i][0], float):
                        self.gene[i] = random.uniform(memory('parametres')[i][0], memory('parametres')[i][1])
