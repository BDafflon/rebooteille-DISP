"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
from Route import Route

class TimeSlot:
    INDICE = 1

    def __init__(self):
        self.listRoute = []
        self.indice = TimeSlot.INDICE
        self.duration = 0
        TimeSlot.INDICE += 1

    def getIndice(self):
        return self.indice

    def getListRoute(self):
        return self.listRoute

    def addToListRoute(self, route):
        self.listRoute.append(route)

    def removeFromListRoute(self, routeToRemove):
        i = 0
        for route in self.listRoute:
            if(route.getIndice() == routeToRemove.getIndice()):
                break
            i += 1
        self.listRoute.pop(i)

    def getDuration(self, timeTravel, fixedCollectionTime, collectionTimePerCrate):
        timeSlotDuration = 0
        for route in self.listRoute:
            timeSlotDuration += route.getDuration(timeTravel, fixedCollectionTime, collectionTimePerCrate)
        self.duration = timeSlotDuration
        return self.duration

    def copy(self, timeSlotToCopy):
        #Copie des variables
        self.indice = timeSlotToCopy.indice
        self.duration = timeSlotToCopy.duration

        #Copie des routes
        self.listRoute = []
        for routeToCopy in timeSlotToCopy.listRoute:
            route = Route()
            route.copy(routeToCopy)
            self.addToListRoute(route)

    def toString(self, positionInList = ""):
        i = 1
        res = "*** Time slot " + str(positionInList) + " ***" + "\n"
        res += "\t- Duration = " + str(round(self.duration,2)) + "\n"
        res += "\t- Nombre de routes = " + str(len(self.listRoute)) + "\n"
        for route in self.listRoute:
            res += route.toString(i)
            if (i < len(self.listRoute)):
                res += "\n" + "\n"
            i = i + 1
        res += "\n"
        return res
