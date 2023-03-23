"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""


class Client:
    def __init__(self, indice=0, quantity=0, capacity=0, request=0, location=(0, 0)):
        self.indice = indice
        self.location = location
        self.quantity = quantity
        self.capacity = capacity
        self.request = request
        self.visited = False

    def getIndice(self):
        return self.indice

    def getQuantity(self):
        return self.quantity

    def getCapacity(self):
        return self.capacity

    def getIsRequested(self):
        return self.request

    def isVisited(self):
        return self.visited

    def setRequest(self, requested):
        self.request = requested

    def setVisited(self):
        self.visited = True

    def setNotVisited(self):
        self.visited = False

    def display(self):
        print("- Client = {c}".format(c=self.indice))
        print("\tCapacity = {c}".format(c=self.capacity))
        print("\tQuantity = {q}".format(q=self.quantity))
        print("\tRequested = {r}".format(r=self.request))
        print("\tVisited = {v}".format(v=self.visited))
