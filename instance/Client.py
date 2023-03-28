"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""


class Client:
    def __init__(self, indice=0, quantity=0, capacity=0, request=0, location=(0, 0), morningOpening=0,
                 morningClosing=0, afternoonOpening=12, afternoonClosing=12, name="point"):
        self.indice = indice
        self.name = name
        self.location = location
        self.quantity = quantity
        self.capacity = capacity
        self.request = request
        self.morningOpening = morningOpening * 60 # min
        self.morningClosing = morningClosing * 60 # min
        self.afternoonOpening = afternoonOpening * 60 # min
        self.afternoonClosing = afternoonClosing * 60 # min
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
        print("- Client = {c} : {name}".format(c=self.indice, name=self.name))
        print("\tCapacity = {c}".format(c=self.capacity))
        print("\tQuantity = {q}".format(q=self.quantity))
        print("\tRequested = {r}".format(r=self.request))
        print("\tOpen from {mo} to {mc} and from {ao} to {ac}".format(mo=self.morningOpening, mc=self.morningClosing, ao=self.afternoonOpening, ac=self.afternoonClosing))
        print("\tVisited = {v}".format(v=self.visited))