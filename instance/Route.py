"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""


class Route:
    INDICE = 1

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.trajet = []
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

    def copy(self, routeToCopy):
        # Copie des variables
        self.indice = routeToCopy.indice
        self.duration = routeToCopy.duration

        # Copie des clients
        self.trajet = []

        for clientToCopy in routeToCopy.trajet:
            self.appendClient(clientToCopy)

    def display(self, positionInListTimeSlot=""):
        print("\tRoute {i} :".format(i=positionInListTimeSlot))
        print("\t\t- Total Quantity = {q}".format(q=self.totalQuantity))
        print("\t\t- Duration = {d}".format(d=round(self.duration, 2)))
        if len(self.trajet) == 0:
            return
        route = "{i}".format(i=self.trajet[0].getIndice())
        for client in self.trajet[1:]:
            route += " -> {i}".format(i=client.getIndice())
        print("\t\t- Trajet : {route}".format(route=route))
