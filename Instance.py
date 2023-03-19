"""
Code from project ALNS 2022, ALEXI OMAR DJAMA
"""
import pandas as pd
from Client import Client

def parsingDistance(filePath, sheetName):
    #Méthode pour parser les distances du fichier Time Travel
    timeTravel = {}

    #Lecture du fichier
    dfTimeTravel = pd.read_excel(filePath, sheet_name=sheetName)

    #Récupération du nombre de ligne et de colonnes
    (nbLigne, nbColumn) = dfTimeTravel.shape

    #Peuplement des valeurs du dictionnaire timeTravel
    for ligne in range(nbLigne):
        for column in range(nbColumn - 1):
            timeTravel[(ligne, column)] = dfTimeTravel[column][ligne]

    return timeTravel

class Instance:
    def __init__(self, fileDataPath, fileDistPath="./data/MatricesDT.xlsx", dataSheetName="Data", distSheetName="Tps30kmh"):
        #Initialisation
        self.listClient = []
        self.timeTravel = parsingDistance(fileDistPath, distSheetName)
        start = fileDataPath.rfind('/') + 1
        end = fileDataPath.rfind('.')
        self.name = fileDataPath[start:end]

        #Récupération du dataframe à partir de l'excel situé à l'emplacement fileDataPath
        dfInstance = pd.read_excel(fileDataPath, sheet_name=dataSheetName)

        #Récupération du nombre de client à traiter
        numberClient = dfInstance[0][0].astype(int)

        #Création des clients entre 0 et numberClient
        for i in range(0,numberClient):
            if(dfInstance[i][1].astype(int) == 1):
                #Creation du client
                fillingRate = dfInstance[i][3]
                capacity = dfInstance[i][2]
                request = (dfInstance[i][12].astype(int) == 1)
                client = Client(i, fillingRate=fillingRate, capacity=capacity, request=request)
                #Ajout du client à la liste de client
                self.listClient.append(client)

        #Affectation des valeurs du dataframe qui seront utiles pour la suite du programme
        self.fixedCollectionTime = dfInstance[0][4].astype(int)
        self.collectionTimePerCrate = dfInstance[0][5].astype(float)
        self.vehiculeVelocityMax = dfInstance[0][6].astype(int)
        self.vehiculeCapacityMax = dfInstance[0][7].astype(int)
        self.numberTimeSlotMax = dfInstance[0][8].astype(int)
        self.routePerTimeSlotMax = dfInstance[0][9].astype(int)
        self.durationTimeSlotMax = dfInstance[0][11].astype(int)

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
