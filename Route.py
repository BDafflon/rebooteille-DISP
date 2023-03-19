"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""

class Route:
    INDICE = 1

    def __init__(self):
        self.indice = Route.INDICE
        self.trajet = []
        self.totalFillingRate = 0
        self.duration = 0
        Route.INDICE += 1

    def getIndice(self):
        return self.indice

    def getTrajet(self):
        return self.trajet

    def getTotalFillingRate(self):
        return self.totalFillingRate

    def appendClient(self, client):
        self.trajet.append(client)
        self.totalFillingRate += client.getFillingRate()

    def insertClient(self, indice, client):
        self.trajet.insert(indice, client)
        self.totalFillingRate += client.getFillingRate()

    def removeClient(self, clientToRemove):
        i = 0
        for client in self.trajet:
            if (clientToRemove.getIndice() == client.getIndice()):
                break
            i = i + 1
        client = self.trajet.pop(i)
        self.totalFillingRate -= client.getFillingRate()

    def getIdClientByIndice(self, indice):
        return self.trajet[indice].getIndice()

    def getClientFromIndice(self, indice):
        return self.trajet[indice]

    def getDuration(self, timeTravel, fixedCollectionTime, collectionTimePerCrate):
        self.duration = 0
        self.totalFillingRate = 0

        if(len(self.trajet) > 1):
            for i in range(len(self.trajet) -1):
                clientDepart = self.trajet[i]
                clientArrivee = self.trajet[i + 1]

                self.duration += timeTravel[(clientDepart.getIndice(), clientArrivee.getIndice())]
                self.duration += fixedCollectionTime
                self.duration += collectionTimePerCrate * clientArrivee.getFillingRate()

                self.totalFillingRate += clientArrivee.getFillingRate()

            #self.duration += timeTravel[(clientArrivee.getIndice(), self.trajet[0].getIndice())]
            #self.duration += fixedCollectionTime
            #self.duration += collectionTimePerCrate * clientArrivee.getFillingRate()

        return self.duration

    def copy(self, routeToCopy):
        #Copie des variables
        self.indice = routeToCopy.indice
        self.duration = routeToCopy.duration

        #Copie des clients
        self.trajet = []

        for clientToCopy in routeToCopy.trajet:
            self.appendClient(clientToCopy)

    def display(self, positionInListTimeSlot=""):
        print("\tRoute {i} :".format(i=positionInListTimeSlot))
        print("\t\t- TotalFillingRate = {r}".format(r=self.totalFillingRate))
        print("\t\t- Duration = {d}".format(d=round(self.duration, 2)))
        if(len(self.trajet) == 0):
            return
        route = "{i}".format(i=self.trajet[0].getIndice())
        for client in self.trajet[1:]:
            route += " -> {i}".format(i=client.getIndice())
        print("\t\t- Trajet : {route}".format(route=route))
