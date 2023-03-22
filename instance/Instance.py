"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
import geopy.distance as gd


class Instance:
    def __init__(self, listClient, listVehicle, numberTimeSlotMax, routePerTimeSlotMax, durationTimeSlotMax, distTravel={}, name="present"):
        self.listClient = listClient
        self.listVehicle = listVehicle
        if len(distTravel) == 0:
            self.distTravel = {(i.getIndice(), j.getIndice()): gd.geodesic(i.location, j.location).km for i in listClient for j in listClient}
        else:
            self.distTravel = distTravel
        self.name = name
        self.numberTimeSlotMax = numberTimeSlotMax
        self.routePerTimeSlotMax = routePerTimeSlotMax
        self.durationTimeSlotMax = durationTimeSlotMax

    def getName(self):
        return self.name

    def getDistance(self, firstClientId, secondClientId):
        return self.distTravel[(firstClientId, secondClientId)]

    def display(self, showClients=False, showDistTravel=False):
        # showClients est un boolean correspondant à l'affichage la liste des clients
        # showDistTravel est un boolean correspondant à l'affichage de la distance entre chaque client
        print("--- Instance {name} ---".format(name=self.name))
        print("Routes per time slot max = {rts}".format(rts=self.routePerTimeSlotMax))
        print("Number time slot max = {nts}".format(nts=self.numberTimeSlotMax))
        print("Duration time slot max = {dts}".format(dts=self.durationTimeSlotMax))

        if showClients:
            print("* List of clients :")
            for client in self.listClient:
                client.display()

        print("* List of vehicles :")
        for vehicle in self.listVehicle:
            vehicle.display()

        if showDistTravel:
            print("* Distance travel :")
            for cle, valeur in self.distTravel.items():
                print("\t-{cle} : {valeur}".format(cle=cle, valeur=valeur))
