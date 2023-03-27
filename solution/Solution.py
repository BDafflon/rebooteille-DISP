"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
from instance.TimeSlot import TimeSlot
import math
from solution.checkSolution import check


class Solution:
    facteurZ1 = 1
    facteurZ2 = 10
    facteurZ3 = 10
    facteurZ4 = 1

    def __init__(self, instance=None, time=0):
        self.instance = instance
        self.listTimeSlot = []
        self.cost = 0
        self.updateCost = False
        self.duration = 0  # Z1
        self.requestPriorityPenalty = 0  # Z2
        self.inventoryPriorityPenalty = 0  # Z3
        # Z4 = len(self.listTimeSlot)
        self.time = time
        self.nIter = 6000
        self.pu = 100
        self.rho = 0.3
        self.sigma1 = 130
        self.sigma2 = 70
        self.sigma3 = 25
        self.tau = 0.1
        self.c = 0.9995
        self.alpha = 0.5
        self.beta = 0.25
        self.gamma = 0.25
        self.nc = 2000
        self.theta = 0.5  # swaps
        self.ns = 10  # swaps

    def setTime(self, time):
        self.time = time

    def getCost(self):
        if self.updateCost:
            return self.calculateCost()
        return self.cost

    def getListTimeSlot(self):
        return self.listTimeSlot

    def addToListTimeSlot(self, timeSlot):
        self.listTimeSlot.append(timeSlot)
        self.updateCost = True

    def removeFromListTimeSlot(self, timeSlotToRemove):
        i = 0
        for timeSlot in self.listTimeSlot:
            if timeSlot.getIndice() == timeSlotToRemove.getIndice():
                break
            i += 1
        self.listTimeSlot.pop(i)
        self.updateCost = True

    def copy(self, solutionToCopy):
        # Copie des variables
        self.instance = solutionToCopy.instance
        self.time = solutionToCopy.time

        # Copie des timeslots
        self.listTimeSlot = []
        for timeSlotToCopy in solutionToCopy.listTimeSlot:
            timeSlot = TimeSlot()
            timeSlot.copy(timeSlotToCopy)
            self.listTimeSlot.append(timeSlot)
        self.cost = self.calculateCost()
        updateCost = False

    def calculateCost(self):
        self.cost = 0

        self.duration = 0
        self.requestPriorityPenalty = 0
        self.inventoryPriorityPenalty = 0

        for indiceTimeSlot in range(len(self.listTimeSlot)):

            timeSlot = self.listTimeSlot[indiceTimeSlot]

            # Calcul de Z1
            self.duration += timeSlot.getDuration(self.instance.getDistance)

            for indiceRoute in range(len(timeSlot.listRoute)):
                route = timeSlot.listRoute[indiceRoute]

                if len(route.getTrajet()) > 1:
                    for indiceClient in range(len(route.getTrajet()) - 1):
                        clientArrivee = route.getClientFromIndice(indiceClient + 1)

                        # Calcul de Z2
                        if indiceTimeSlot + 1 > 1:
                            self.requestPriorityPenalty += (math.floor(
                                10 * (clientArrivee.getQuantity() / clientArrivee.getCapacity())) * indiceTimeSlot) / 10

                            # Calcul de Z3
                            if clientArrivee.getIsRequested():
                                self.inventoryPriorityPenalty += indiceTimeSlot

        # Calcul de Z4
        Z4 = len(self.listTimeSlot)

        # Calcul du coût total
        self.cost = Solution.facteurZ1 * self.duration + Solution.facteurZ2 * self.requestPriorityPenalty
        self.cost += Solution.facteurZ3 * self.inventoryPriorityPenalty + Solution.facteurZ4 * Z4
        self.updateCost = False
        return self.cost

    def checkSolution(self, showLog=False, notSommetVisited=False):
        return check(self, showLog, notSommetVisited)

    def display(self):
        print("*** Solution {name} ***".format(name=self.instance.getName()))
        print("- Coût de la solution = {c} (= {k1}*{z1} + {k2}*{z2} + {k3}*{z3} + {k4}*{z4})".format(
            c=round(self.cost, 2),
            k1=Solution.facteurZ1,
            z1=round(self.duration, 2),
            k2=Solution.facteurZ2,
            z2=round(self.requestPriorityPenalty, 2),
            k3=Solution.facteurZ3,
            z3=self.inventoryPriorityPenalty,
            k4=Solution.facteurZ4,
            z4=len(self.listTimeSlot)
            ))
        i = 1
        for timeSlot in self.listTimeSlot:
            timeSlot.display(i)
            i += 1
