"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""

class Instance:
    def __init__(self, listClient, timeTravel, fixedCollectionTime, collectionTimePerCrate, vehiculeVelocityMax, vehiculeCapacityMax, numberTimeSlotMax, routePerTimeSlotMax, durationTimeSlotMax, name="present"):
        self.listClient = listClient
        self.timeTravel = timeTravel
        self.name = name
        self.fixedCollectionTime = fixedCollectionTime
        self.collectionTimePerCrate = collectionTimePerCrate
        self.vehiculeVelocityMax = vehiculeVelocityMax
        self.vehiculeCapacityMax = vehiculeCapacityMax
        self.numberTimeSlotMax = numberTimeSlotMax
        self.routePerTimeSlotMax = routePerTimeSlotMax
        self.durationTimeSlotMax = durationTimeSlotMax

    def getName(self):
        return self.name

    def getClientByClientId(self, clientId):
        for client in self.listClient:
            if(client.getIndice() == clientId):
                return client

    def display(self, showClients=False, showTimeTravel=False):
        # showClients est un booleen correspondant à l'affichage la liste des clients
        # showTimeTravel est un booleen correspondant à l'affichage du temps de trajet
        print("--- Instance {name} ---".format(name=self.name))
        print("Fixed collection time = {fct}".format(fct=self.fixedCollectionTime))
        print("Collection time per crate = {ctc}".format(ctc=self.collectionTimePerCrate))
        print("Vehicule velocity max = {vv}".format(vv=self.vehiculeVelocityMax))
        print("Vehicule capacity max = {vc}".format(vc=self.vehiculeCapacityMax))
        print("Routes per time slot max = {rts}".format(rts=self.routePerTimeSlotMax))
        print("Number time slot max = {nts}".format(nts=self.numberTimeSlotMax))
        print("Duration time slot max = {dts}".format(dts=self.durationTimeSlotMax))

        if(showClients):
            print("* List of client :")
            for client in self.listClient:
                client.display()

        if(showTimeTravel):
            print("* Time travel :")
            for cle, valeur in self.timeTravel.items():
                print("\t-{cle} : {valeur}".format(cle=cle, valeur=valeur))
