"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
from instance.Route import Route


class TimeSlot:
    INDICE = 1

    def __init__(self):
        self.listRoute = []
        self.duration = 0
        self.indice = TimeSlot.INDICE
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
            if route.getIndice() == routeToRemove.getIndice():
                break
            i += 1
        self.listRoute.pop(i)

    def getDuration(self, distFunction):
        sum = 0
        for route in self.listRoute:
            sum += route.getDuration(distFunction)
        self.duration = sum
        return self.duration

    def copy(self, timeSlotToCopy):
        # Copie des variables
        self.indice = timeSlotToCopy.indice
        self.duration = timeSlotToCopy.duration

        # Copie des routes
        self.listRoute = []
        for routeToCopy in timeSlotToCopy.listRoute:
            route = Route(routeToCopy.vehicle)
            route.copy(routeToCopy)
            self.addToListRoute(route)

    def display(self, positionInList=""):
        i = 1
        print("*** Time slot {i} ***".format(i=positionInList))
        print("\t- Duration = {d}".format(d=round(self.duration, 2)))
        print("\t- Nombre de routes = {r}".format(r=len(self.listRoute)))
        for route in self.listRoute:
            route.display(i)
            if i < len(self.listRoute):
                print()
            i += 1
        print()
