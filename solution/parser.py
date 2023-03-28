import json
from instance.TimeSlot import TimeSlot
from instance.Route import Route
from instance.Vehicle import Vehicle
from instance.Client import Client
from solution.Solution import Solution
from instance.parser import parse


def readVehicle(dataVehicle):
    name = dataVehicle['name']
    driver = dataVehicle['driver']
    capacity = int(dataVehicle['capacity'])
    speed = float(dataVehicle['speed'])
    fct = float(dataVehicle['fixedCollectionTime'])
    ctc = float(dataVehicle['collectionTimePerCrate'])
    return Vehicle(capacity, speed, fct, ctc, name=name, drivers=[driver])


def readClient(dataClients, listClient):
    clients = [Client() for i in dataClients]
    for dataClient in dataClients:
        id = dataClient['id']
        name = dataClient['name']
        client = listClient[id]
        if client.name != name:
            raise Exception("Wrong id : {id}".format(id=id))
        order = dataClient['order']
        if order < 0 or len(clients) <= order:
            raise Exception("Wrong order : {order}".format(order=order))
        clients[order] = client
    # vérification que tous les clients sont placés ?
    return clients


def readRoute(dataRoute, listClient):
    vehicle = readVehicle(dataRoute['vehicle'][0])
    route = Route(vehicle)
    route.trajet = readClient(dataRoute['route'], listClient)
    return route


def readTimeSlot(dataTimeSlot, listClient, distFunc):
    timeSlot = TimeSlot()
    for dataRoute in dataTimeSlot['timeSlot']:
        route = readRoute(dataRoute, listClient)
        route.getTotalQuantity()
        route.updateTimetables(distFunc)
        timeSlot.addToListRoute(route)
    timeSlot.getDuration(distFunc)
    return timeSlot


def parseSolution(filePath, solutionPath):
    data = json.load(open(solutionPath))
    instance = parse(filePath)
    # instance = parse(data['name'])
    solution = Solution(instance)
    nIter = data['nIter']
    pu = data['PU']
    rho = data['rho']
    sigma1 = data['sigma1']
    sigma2 = data['sigma2']
    sigma3 = data['sigma3']
    tau = data['tau']
    c = data['C']
    alpha = data['alpha']
    beta = data['beta']
    gamma = data['gamma']
    nc = data['Nc']
    theta = data['theta']
    ns = data['Ns']
    solution.setParameters(nIter, pu, rho, sigma1, sigma2, sigma3, tau, c, alpha, beta, gamma, nc, theta, ns)
    foundTime = data['found time']
    totalTime = data['total time']
    solution.setTime(foundTime, totalTime)

    for dataTimeSlot in data['routing']:
        timeSlot = readTimeSlot(dataTimeSlot, instance.listClient, instance.getDistance)
        solution.addToListTimeSlot(timeSlot)
    solution.calculateCost()
    return solution
