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

    def __init__(self, instance=None, Z1=facteurZ1, Z2=facteurZ2, Z3=facteurZ3, Z4=facteurZ4):
        self.listTimeSlot = []
        self.instance = instance
        self.cost = 0
        self.z1 = Z1
        self.z2 = Z2
        self.z3 = Z3
        self.z4 = Z4

    def addToListTimeSlot(self, timeSlot):
        self.listTimeSlot.append(timeSlot)

    def removeFromListTimeSlot(self, timeSlotToRemove):
        i = 0
        for timeSlot in self.listTimeSlot:
            if(timeSlot.getIndice() == timeSlotToRemove.getIndice()):
                break
            i += 1
        self.listTimeSlot.pop(i)

    def setInstance(self, instance):
        self.instance = instance

    def copy(self, solutionToCopy):
        #Copie des variables
        self.instance = solutionToCopy.instance
        self.cost = solutionToCopy.cost
        self.z1 = solutionToCopy.z1
        self.z2 = solutionToCopy.z2
        self.z3 = solutionToCopy.z3
        self.z4 = solutionToCopy.z4

        #Copie des timeslots
        self.listTimeSlot = []

        for timeSlotToCopy in solutionToCopy.listTimeSlot:
            timeSlot = TimeSlot()
            timeSlot.copy(timeSlotToCopy)

            self.listTimeSlot.append(timeSlot)

    def calculateCost(self):
        self.cost = 0

        self.z1 = 0
        self.z2 = 0
        self.z3 = 0
        self.z4 = 0

        for indiceTimeSlot in range(len(self.listTimeSlot)):

            timeSlot = self.listTimeSlot[indiceTimeSlot]

            #Calcul de Z1
            self.z1 += timeSlot.getDuration(
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
                            self.z2 += (math.floor(10*(clientArrivee.getFillingRate() / clientArrivee.getCapacity())) * indiceTimeSlot)/10

                            #Calcul de Z3
                            if(clientArrivee.getIsRequested()):
                                self.z3 += indiceTimeSlot

        #Calcul de Z4
        self.z4 += len(self.listTimeSlot)

        #Calcul du coût total
        self.cost = Solution.facteurZ1 * self.z1 + Solution.facteurZ2 * self.z2
        self.cost += Solution.facteurZ3 * self.z3 + Solution.facteurZ4 * self.z4



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
        res = "*** Solution ***\n"
        res += "- Coût de la solution = " + str(round(self.cost,2)) + "\n"

        if(showDetailedCost):
            res += "- Z1 = " + str(round(self.z1, 2)) + "\n"
            res += "- Z2 = " + str(round(self.z2, 2)) + "\n"
            res += "- Z3 = " + str(self.z3) + "\n"
            res += "- Z4 = " + str(self.z4) + "\n"

        i = 1
        for timeSlot in self.listTimeSlot:
            res += timeSlot.toString(i)
            i += 1

        print(res)
