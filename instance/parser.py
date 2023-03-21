import pandas as pd
from instance.Instance import Instance
from instance.Client import Client
from instance.Vehicle import Vehicle

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

def parseForALNS(fileDataPath, dataSheetName="Data", fileDistPath="./data/MatricesDT.xlsx", distSheetName="Distance"):
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
            quantity = dfInstance[i][3]
            capacity = dfInstance[i][2]
            request = (dfInstance[i][12].astype(int) == 1)
            client = Client(i, quantity, capacity, request)
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

    listVehicle = [Vehicle(vehiculeCapacityMax, vehiculeVelocityMax, fixedCollectionTime, collectionTimePerCrate)]

    return Instance(listClient, listVehicle, numberTimeSlotMax, routePerTimeSlotMax, durationTimeSlotMax, timeTravel, name)

def readVehicles(fileName):
    listVehicle = []
    dfVehicles = pd.read_json(fileName, orient='records')
    for i in range(len(dfVehicles)):
        capacity = dfVehicles['capacity'][i]
        speed = dfVehicles['speed'][i]
        fct = dfVehicles['fixedCollectionTime'][i]
        ctc = dfVehicles['collectionTimePerCrate'][i]
        cost = dfVehicles['cost'][i]
        name = dfVehicles['name'][i]
        drivers = dfVehicles['driver'][i]
        listVehicle.append(Vehicle(capacity, speed, fct, ctc, cost, name, drivers))
    return listVehicle

def readClients(fileName):
    listClient = []
    dfClient = pd.read_excel(fileName)
    for i in range(len(dfClient)):
        id = i + 1
        quantity = dfClient['Quantité'][i]
        capacity = dfClient['Nb Casiers'][i]
        request = dfClient['Requête'][i]
        location = (dfClient['latitude'][i], dfClient['longitude'][i])
        listClient.append(Client(id, quantity, capacity, request, location))
    return listClient

def readContext(fileName):
    dfContext = pd.read_json(fileName, orient='index').transpose()
    name = dfContext['name'][0]
    id = 0
    location = (dfContext['depotLatitude'][0], dfContext['depotLongitude'][0])
    depot = Client(indice=id, location=location, capacity=1)
    ntm = dfContext['numberTimeSlotMax'][0]
    rpt = dfContext['routePerTimeSlotMax'][0]
    dtm = dfContext['durationTimeSlotMax'][0]
    return name, depot, ntm, rpt, dtm

def parse(filePath):
    listVehicle = readVehicles(filePath+"vehicle.json")
    listClient = readClients(filePath+"points.xlsx")
    name, depot, ntm, rpt, dtm = readContext(filePath+"context.json")
    listClient = [depot] + listClient
    return Instance(listClient, listVehicle, ntm, rpt, dtm, name=name)
