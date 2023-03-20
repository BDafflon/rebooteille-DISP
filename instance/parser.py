import pandas as pd
from instance.Instance import Instance
from instance.Client import Client

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

def parse(fileDataPath, dataSheetName="Data", fileDistPath="./data/MatricesDT.xlsx", distSheetName="Tps30kmh"):
    listClient = []
    timeTravel = parsingDistance(fileDistPath, distSheetName)

    start = fileDataPath.rfind('/') + 1
    end = fileDataPath.rfind('.')
    name = fileDataPath[start:end]

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
            listClient.append(client)

    #Affectation des valeurs du dataframe qui seront utiles pour la suite du programme
    fixedCollectionTime = dfInstance[0][4].astype(int)
    collectionTimePerCrate = dfInstance[0][5].astype(float)
    vehiculeVelocityMax = dfInstance[0][6].astype(int)
    vehiculeCapacityMax = dfInstance[0][7].astype(int)
    numberTimeSlotMax = dfInstance[0][8].astype(int)
    routePerTimeSlotMax = dfInstance[0][9].astype(int)
    durationTimeSlotMax = dfInstance[0][11].astype(int)

    return Instance(listClient, timeTravel, fixedCollectionTime, collectionTimePerCrate, vehiculeVelocityMax, vehiculeCapacityMax, numberTimeSlotMax, routePerTimeSlotMax, durationTimeSlotMax, name)
