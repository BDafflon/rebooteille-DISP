"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""


class Route:
    INDICE = 1

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.trajet = []
        self.startTime = [] # minutes au plus tôt de début de collecte
        self.endTime = [] # minutes au plus tard de fin de collecte
        self.delta = [] # minutes nécessaires à la collecte
        self.totalQuantity = 0
        self.duration = 0
        self.indice = Route.INDICE
        Route.INDICE += 1

    def getIndice(self):
        return self.indice

    def getTrajet(self):
        return self.trajet

    def getClientFromIndice(self, indice):
        return self.trajet[indice]

    def getIdClientByIndice(self, indice):
        return self.trajet[indice].getIndice()

    def appendClient(self, client):
        self.trajet.append(client)
        self.totalQuantity += client.getQuantity()

    def insertClient(self, indice, client):
        self.trajet.insert(indice, client)
        self.totalQuantity += client.getQuantity()

    def removeClient(self, clientToRemove):
        i = 0
        for client in self.trajet:
            if clientToRemove.getIndice() == client.getIndice():
                break
            i = i + 1
        client = self.trajet.pop(i)
        self.totalQuantity -= client.getQuantity()

    def getTotalQuantity(self):
        sum = 0
        for client in self.trajet:
            sum += client.getQuantity()
        self.totalQuantity = sum
        return self.totalQuantity

    def getDuration(self, distFunction):
        self.duration = 0

        if len(self.trajet) > 1:
            clientDepart = self.trajet[0]
            for i in range(1, len(self.trajet)):
                clientArrivee = self.trajet[i]

                time = distFunction(clientDepart.getIndice(),
                                    clientArrivee.getIndice()) / self.vehicle.getSpeed() * 60  # min
                self.duration += time
                # Pas de temps de collecte au depot !!!
                # if clientArrivee.getIndice() != 0:
                self.duration += self.vehicle.getFixedCollectionTime()
                self.duration += self.vehicle.getCollectionTimePerCrate() * clientArrivee.getQuantity()

                clientDepart = clientArrivee

        return self.duration

    def updateTimetables(self, distFunction):
        # initialisation de début de collecte au plus tôt = heure d'ouverture
        self.startTime = [client.morningOpening for client in self.trajet]
        # initialisation de fin de collecte au plus tard = heure de fermeture
        self.endTime = [client.morningClosing for client in self.trajet]
        # minutes nécessaires à la collecte = temps fixe dépendant du véhicule
        # + temps de chargement proportionnel au nombre de caisses
        self.delta = [0] + [self.vehicle.getFixedCollectionTime()
                            + self.vehicle.getCollectionTimePerCrate() * client.getQuantity()
                            for client in self.trajet[1:-1]] + [0]
        size = len(self.trajet)
        if size <= 2:
            return
        for i in range(1, size):
            # earliest start
            previousClientId = self.trajet[i - 1].getIndice()
            clientId = self.trajet[i].getIndice()

            arrivalTime = self.startTime[i - 1] + self.delta[i - 1]
            arrivalTime += distFunction(previousClientId, clientId)
            self.startTime[i] = max(self.startTime[i], arrivalTime)

            # latest start
            j = size - 1 - i
            nextClientId = self.trajet[j + 1].getIndice()
            clientId = self.trajet[j].getIndice()

            departTime = self.endTime[j + 1] - self.delta[j + 1]
            departTime -= distFunction(clientId, nextClientId)
            self.endTime[j] = min(self.endTime[j], departTime)

        self.startTime[0] = self.startTime[1] - distFunction(self.trajet[0].getIndice(), self.trajet[1].getIndice())
        self.endTime[-1] = self.endTime[-2] + distFunction(self.trajet[-2].getIndice(), self.trajet[-1].getIndice())
        self.endTime[-1] += self.delta[-1]

    def copy(self, routeToCopy):
        # Copie des variables
        self.indice = routeToCopy.indice
        self.duration = routeToCopy.duration

        # Copie des clients
        self.trajet = []

        for clientToCopy in routeToCopy.trajet:
            self.appendClient(clientToCopy)

    def display(self, positionInListTimeSlot="", showTimeTable=False):
        print("\tRoute {i} :".format(i=positionInListTimeSlot))
        print("\t\t- Total Quantity = {q}".format(q=self.totalQuantity))
        print("\t\t- Duration = {d}".format(d=round(self.duration, 2)))
        if len(self.trajet) == 0:
            return
        route = "{i}".format(i=self.trajet[0].getIndice())
        for client in self.trajet[1:]:
            route += " -> {i}".format(i=client.getIndice())
        print("\t\t- Trajet : {route}".format(route=route))
        if showTimeTable:
            print(self.delta)
            for i in range(len(self.trajet)):
                if i == 0:
                    print("Collection routing starts between {earliestStart} and {latestStart}"
                          .format(i=i, earliestStart=self.startTime[i], latestStart=self.endTime[i] - self.delta[i]))
                elif i == len(self.trajet) - 1:
                    print("Collection routing ends between {earliestStart} and {latestStart}"
                          .format(i=i, earliestStart=self.startTime[i], latestStart=self.endTime[i] - self.delta[i]))
                else:
                    print("Collection of point {i} starts between {earliestStart} and {latestStart} and ends "
                          "between {earliestEnd} and {latestEnd}".format(i=i, earliestStart=self.startTime[i],
                                                                         latestStart=self.endTime[i] - self.delta[i],
                                                                         earliestEnd=self.startTime[i] + self.delta[i],
                                                                         latestEnd=self.endTime[i]))