"""
Code from project ALNS 2022, ALEXI OMAR DJAMA
"""
from Instance import Instance
from TimeSlot import TimeSlot
import math

class Solution:

    facteurZ1 = 1
    facteurZ2 = 10
    facteurZ3 = 10
    facteurZ4 = 1

    def __init__(self, instance=None):
        self.instance = instance
        self.listTimeSlot = []
        self.cost = 0
        self.duration = 0 #Z1
        self.requestPriorityPenalty = 0 #Z2
        self.inventoryPriorityPenalty = 0 #Z3
        #Z4 = len(self.listTimeSlot)
        self.time = 0
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
        self.theta = 0.5 #swaps
        self.ns = 10 #swaps

    def getCost(self):
        return self.cost

    def getListTimeSlot(self):
        return self.listTimeSlot

    def addToListTimeSlot(self, timeSlot):
        self.listTimeSlot.append(timeSlot)

    def removeFromListTimeSlot(self, timeSlotToRemove):
        i = 0
        for timeSlot in self.listTimeSlot:
            if(timeSlot.getIndice() == timeSlotToRemove.getIndice()):
                break
            i += 1
        self.listTimeSlot.pop(i)

    def copy(self, solutionToCopy):
        #Copie des variables
        self.instance = solutionToCopy.instance
        self.cost = solutionToCopy.cost
        self.duration = solutionToCopy.duration
        self.requestPriorityPenalty = solutionToCopy.requestPriorityPenalty
        self.inventoryPriorityPenalty = solutionToCopy.inventoryPriorityPenalty

        #Copie des timeslots
        self.listTimeSlot = []

        for timeSlotToCopy in solutionToCopy.listTimeSlot:
            timeSlot = TimeSlot()
            timeSlot.copy(timeSlotToCopy)

            self.listTimeSlot.append(timeSlot)

    def calculateCost(self):
        self.cost = 0

        self.duration = 0
        self.requestPriorityPenalty = 0
        self.inventoryPriorityPenalty = 0

        for indiceTimeSlot in range(len(self.listTimeSlot)):

            timeSlot = self.listTimeSlot[indiceTimeSlot]

            #Calcul de Z1
            self.duration += timeSlot.getDuration(
                self.instance.timeTravel,
                self.instance.fixedCollectionTime,
                self.instance.collectionTimePerCrate
                )

            for indiceRoute in range(len(timeSlot.listRoute)):
                route = timeSlot.listRoute[indiceRoute]

                if(len(route.getTrajet()) > 1):
                    for indiceClient in range(len(route.getTrajet()) - 1):
                        clientArrivee = route.getClientFromIndice(indiceClient + 1)

                        #Calcul de Z2
                        if(indiceTimeSlot + 1 > 1):
                            self.requestPriorityPenalty += (math.floor(10*(clientArrivee.getFillingRate() / clientArrivee.getCapacity())) * indiceTimeSlot)/10

                            #Calcul de Z3
                            if(clientArrivee.getIsRequested()):
                                self.inventoryPriorityPenalty += indiceTimeSlot

        #Calcul de Z4
        Z4 = len(self.listTimeSlot)

        #Calcul du coût total
        self.cost = Solution.facteurZ1 * self.duration + Solution.facteurZ2 * self.requestPriorityPenalty
        self.cost += Solution.facteurZ3 * self.inventoryPriorityPenalty + Solution.facteurZ4 * Z4



    def checkSolution(self, showLog = False, notSommetVisited = False):
        #Calcul du coût de la solution
        self.calculateCost()

        #Méthode permettant de vérifier que l'on satisfait toutes les contraintes du problème
        '''Contrainte du nombre de time slot utilisés'''
        if(len(self.listTimeSlot) > self.instance.numberTimeSlotMax):
            if(showLog):
                print("Solution incompatible - Nombre de time slots")
                return False

        durationTimeSlot = 0
        for timeSlot in self.listTimeSlot:
            #Si le time slot ne contient pas de routes
            if(len(timeSlot.listRoute) == 0):
                #Alors on peut le supprimer
                self.removeFromListTimeSlot(timeSlot)
                #On relance un check de la solution
                self.checkSolution()

            #Calcul de la durée du time slot
            durationTimeSlot = timeSlot.getDuration(
                    self.instance.timeTravel,
                    self.instance.fixedCollectionTime,
                    self.instance.collectionTimePerCrate
                )

            '''Contrainte du nombre de routes par time slot'''
            if(len(timeSlot.listRoute) > self.instance.routePerTimeSlotMax):
                if(showLog):
                    print("Solution incompatible - Nombre de routes par time slot")
                return False

            for route in timeSlot.getListRoute():
                #Si la route courante n'a que 2 clients alors elle ne passe par aucun sommet
                #Elle fait 0 => 0
                if(len(route.trajet) == 2):
                    #On peut donc la supprimer
                    timeSlot.removeFromListRoute(route)
                    #On relance le check de la solution
                    self.checkSolution()

                '''Contrainte de capacité du véhicule'''
                if(route.getTotalFillingRate() > self.instance.vehiculeCapacityMax):
                    #print(route.getTotalFillingRate())
                    #print(self.instance.vehiculeCapacityMax)
                    if(showLog):
                        print("Solution incompatible - Capacité max du véhicule")
                    return False

                '''Contrainte de démarrer du dépôt'''
                if(route.getTrajet()[0].getIndice() != 0):
                    if(showLog):
                        print("Solution incompatible - Début d'une route sans dépôt")
                    return False

                '''Contrainte de finir par le dépôt'''
                if(route.getTrajet()[len(route.getTrajet()) - 1].getIndice() != 0):
                    if(showLog):
                        print("Solution incompatible - Fin d'une route sans dépôt")
                    return False

                #Sauf si on spécifie de ne pas vérifier les sommets visités
                #Utiliser dans les opérateurs de réparation
                if(not notSommetVisited):
                    #Validation du passage par le sommet
                    if (len(route.getTrajet()) > 1):
                        for i in range(0, len(route.getTrajet()) - 1):
                            clientDepart = route.getClientFromIndice(i)
                            clientArrivee = route.getClientFromIndice(i+1)

                            #Mise à jour pour assurer que les sommets sont visités
                            clientDepart.setVisited()
                            clientArrivee.setVisited()

            '''Contrainte de durée du time slot'''
            if (durationTimeSlot > self.instance.durationTimeSlotMax):

                if(showLog):
                    #print(str(durationTimeSlot ))
                    #print(self.instance.durationTimeSlotMax)
                    print("Solution incompatible - Durée du time slot " + str(timeSlot.getIndice()) + " dépassée")
                return False

        #Si on spécifie de ne pas vérifier les sommets visités
        #Utilisé dans les opérateurs de réparation
        if (not notSommetVisited):
            '''Contrainte de visite de tous les sommets'''
            for client in self.instance.listClient:
                if (not client.isVisited()):
                    if(showLog):
                        print("Solution incompatible - Client " + str(client.getIndice()) + " non visité ")

                    #○Réinitialisation complète de la liste avant de return False
                    for clientVisited in self.instance.listClient:
                        clientVisited.setnotVisited()

                    return False
                else:
                    #S'il a bien été visité on le réinitialise
                    client.setnotVisited()

        return True

    def toString(self, showDetailedCost = True):
        res = "*** Solution " + self.instance.getName() + " ***\n"
        res += "- Coût de la solution = " + str(round(self.cost,2)) + "\n"

        if(showDetailedCost):
            res += "- Z1 = " + str(round(self.duration, 2)) + "\n"
            res += "- Z2 = " + str(round(self.requestPriorityPenalty, 2)) + "\n"
            res += "- Z3 = " + str(self.inventoryPriorityPenalty) + "\n"
            res += "- Z4 = " + str(len(self.listTimeSlot)) + "\n"

        i = 1
        for timeSlot in self.listTimeSlot:
            res += timeSlot.toString(i)
            i += 1
        return res

    def display(self, showDetailedCost=False):
        print(self.toString(showDetailedCost))
