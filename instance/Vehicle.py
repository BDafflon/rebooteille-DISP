
class Vehicle:
    def __init__(self, capacity, speed, fct, ctc, cost=0, name="truck", drivers=[]):
        self.name = name
        self.listDriver = drivers
        self.capacity = capacity
        self.speed = speed
        self.fixedCollectionTime = fct
        self.collectionTimePerCrate = ctc
        self.cost = cost

    def getCapacity(self):
        return self.capacity

    def getSpeed(self): #km/h
        return self.speed

    def getFixedCollectionTime(self):
        return self.fixedCollectionTime

    def getCollectionTimePerCrate(self):
        return self.collectionTimePerCrate

    def getCost(self):
        return self.cost

    def display(self):
        print("- Vehicle : {v}".format(v=self.name))
        print("\tCapacity = {c}".format(c=self.capacity))
        print("\tSpeed = {s}".format(s=self.speed))
        print("\tFixed collection time = {f}".format(f=self.fixedCollectionTime))
        print("\tCollection time per crate = {c}".format(c=self.collectionTimePerCrate))
