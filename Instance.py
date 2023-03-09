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


    def getClientByClientId(self, clientId):
        for client in self.listClient:
            if(client.getIndice() == clientId):
                return client

    def toString(self, showClients=False, showTimeTravel=False):
        # showClients est un booleen correspondant à l'affichage la liste des clients
        # showTimeTravel est un booleen correspondant à l'affichage du temps de trajet
        res = "--- Instance ---" + "\n"
        res += "Fixed collection time = " + str(self.fixedCollectionTime) + "\n"
        res += "Collection time per crate = " + str(self.collectionTimePerCrate) + "\n"
        res += "Vehicule velocity max = " + str(self.vehiculeVelocityMax) + "\n"
        res += "Vehicule capacity max = " + str(self.vehiculeCapacityMax) + "\n"
        res += "Routes per time slot max = " + str(self.routePerTimeSlotMax) + "\n"
        res += "Number time slot max = " + str(self.numberTimeSlotMax) + "\n"
        res += "Duration time slot max = " + str(self.durationTimeSlotMax)

        if(showClients):
            res +="\nList of client :\n"
            for client in self.listClient:
                res += client.toString() + "\n"

        if(showTimeTravel):
            res += "\nTime travel :\n"
            for cle, valeur in self.timeTravel.items():
                res += "\t- " + str(cle) + " : " + str(valeur) + "\n"
        return res

    def display(self, showClients=False, showTimeTravel=False):
        # showClients est un booleen correspondant à l'affichage la liste des clients
        # showTimeTravel est un booleen correspondant à l'affichage du temps de trajet
        print(self.toString(showClients, showTimeTravel))
