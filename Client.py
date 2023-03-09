"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""

class Client:
    def __init__(self, indice=0, fillingRate=0, capacity=0, request=0):
        self.indice = indice
        self.fillingRate = fillingRate
        self.capacity = capacity
        self.request = request
        self.visited = False

    def getIndice(self):
        return self.indice

    def getFillingRate(self):
        return self.fillingRate

    def getCapacity(self):
        return self.capacity

    def getIsRequested(self):
        return self.request

    def isVisited(self):
        return self.visited

    def setIndice(self, indice):
        self.indice = indice

    def setFillingRate(self, fillingRate):
        self.fillingRate = fillingRate

    def setCapacity(self, capacity):
        self.capacity = capacity

    def setRequest(self, requested):
        self.request = requested

    def setVisited(self):
        self.visited = True

    def setnotVisited(self):
        self.visited = False

    def toString(self):
        result = "\t- Client = " + str(self.indice) + "\n"
        result += "\t\tCapacity = " + str(self.capacity) + "\n"
        result += "\t\tFilling rate = " + str(self.fillingRate) + "\n"
        result += "\t\tRequested = " + str(self.request) + "\n"
        result += "\t\tVisited = " + str(self.visited)
        return result

    def display(self):
        print(self.toString())
