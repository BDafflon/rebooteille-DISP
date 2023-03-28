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

    def __init__(self, instance=None):
        self.instance = instance
        self.listTimeSlot = []
        self.cost = -1
        self.updateCost = False
        self.duration = -1  # Z1
        self.requestPriorityPenalty = -1  # Z2
        self.inventoryPriorityPenalty = -1  # Z3
        # Z4 = len(self.listTimeSlot)
        self.foundTime = -1
        self.totalTime = -1
        self.nIter = -1
        self.pu = -1
        self.rho = -1
        self.sigma1 = -1
        self.sigma2 = -1
        self.sigma3 = -1
        self.tau = -1
        self.c = -1
        self.alpha = -1
        self.beta = -1
        self.gamma = -1
        self.nc = -1
        self.theta = -1
        self.ns = -1

    def setTime(self, foundTime, totalTime):
        self.foundTime = foundTime
        self.totalTime = totalTime

    def setParameters(self, nIter, pu, rho, sigma1, sigma2, sigma3, tau, c, alpha, beta, gamma, nc, theta, ns):
        self.nIter = nIter
        self.pu = pu
        self.rho = rho
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.sigma3 = sigma3
        self.tau = tau
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.nc = nc
        self.theta = theta
        self.ns = ns

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
        self.foundTime = solutionToCopy.foundTime

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