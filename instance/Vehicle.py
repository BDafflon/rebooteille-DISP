
class Vehicle:
    def __init__(self, capacity, speed, fct, ctc, cost=0, name="truck", drivers=[]):
        self.name = name
        self.listDriver = drivers
        self.capacity = capacity
        self.speed = speed
        self.fixedCollectionTime = fct
        self.collectionTimePerCrate = ctc
        self.cost = cost

    def getName(self):
        return self.name

    def getDrivers(self):
        return self.listDriver

    def getDriver(self):
        if not self.listDriver:
            return "unknown"
        return self.listDriver[0]

    def setDriver(self, driverId):
        if driverId < 0 or len(self.listDriver) <= driverId:
            raise Exception("Wrong driver id {i} isn't in the list".format(i=driverId))
        keep = self.listDriver[driverId]
        self.listDriver = [keep]

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
