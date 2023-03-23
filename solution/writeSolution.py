import json
import os.path
from solution.Solution import Solution


def writeVehicle(vehicle):
    dictVehicle = {
        "name": vehicle.getName(),
        "driver": vehicle.getDriver(),
        "capacity": str(vehicle.getCapacity()),
        "speed": str(vehicle.getSpeed()),
        "fixedCollectionTime": str(vehicle.getFixedCollectionTime()),
        "collectionTimePerCrate": str(vehicle.getCollectionTimePerCrate())
    }
    return dictVehicle


def writeClient(client, order):
    dictClient = {
        "id": client.getIndice(),
        "order": order,
        "name": "point",
        "latitude": client.location[0],
        "longitude": client.location[1]
    }
    return dictClient


def writeRoute(route, idRoute):
    dictRoute = {
        "id": idRoute,
        "duration": route.duration,
        "vehicle": [writeVehicle(route.vehicle)],
        "route": []
    }
    for order in range(len(route.getTrajet())):
        client = route.getTrajet()[order]
        dictRoute["route"].append(writeClient(client, order))
    return dictRoute


def writeTimeSlot(timeSlot, idTimeSlot):
    dictTimeSlot = {
        "id": idTimeSlot,
        "duration": timeSlot.duration,
        "timeSlot": []
    }
    for idRoute in range(len(timeSlot.getListRoute())):
        route = timeSlot.getListRoute()[idRoute]
        dictTimeSlot["timeSlot"].append(writeRoute(route, idRoute))
    return dictTimeSlot


def toJson(solution, solutionPath="./result/", fileName=None):
    dictResult = {
        "name": solution.instance.getName(),
        "nIter": solution.nIter,
        "PU": solution.pu,
        "rho": solution.rho,
        "sigma1": solution.sigma1,
        "sigma2": solution.sigma2,
        "sigma3": solution.sigma3,
        "tau": solution.tau,
        "C": solution.c,
        "alpha": solution.alpha,
        "beta": solution.beta,
        "gamma": solution.gamma,
        "Nc": solution.nc,
        "theta": solution.theta,
        "Ns": solution.ns,
        "K1": Solution.facteurZ1,
        "K2": Solution.facteurZ2,
        "K3": Solution.facteurZ3,
        "K4": Solution.facteurZ4,
        "cost": solution.getCost(),
        "time": solution.time,
        "routing": []
    }
    for idTimeSlot in range(len(solution.getListTimeSlot())):
        timeSlot = solution.getListTimeSlot()[idTimeSlot]
        dictResult["routing"].append(writeTimeSlot(timeSlot, idTimeSlot))

    if fileName is None:
        fileName = solution.instance.getName()
    solutionName = solutionPath + fileName + ".json"
    with open(solutionName, "w") as outfile:
        json.dump(dictResult, outfile, indent=4)
    print("Solution is saved in " + solutionName)
    del dictResult


def toCsv(solution, solutionPath="./result/", fileName=None, reset=False):
    if fileName is None:
        fileName = solution.instance.getName()
    solutionName = solutionPath + fileName + ".csv"
    if not os.path.isfile(solutionName) or reset:
        with open(solutionName, "w") as outfile:
            outfile.write("Cost; Time; Duration; Request priority penalty; Inventory priority penalty; "
                          "Number of time slots used; Number of iterations; Pu; Rho; Sigma 1; Sigma 2; Sigma 3; Tau; "
                          "C; Alpha; Beta; Gamma; Nc; Theta; Ns\n")
    with open(solutionName, "a") as outfile:
        line = "{cost}; {time}; {duration}; {request}; {inventory}; " \
               "{timeSlots}; {nIter}; {pu}; {rho}; {sigma1}; {sigma2}; {sigma3}; {tau}; " \
               "{c}; {alpha}; {beta}; {gamma}; {nc}; {theta}; {ns}\n".format(cost=solution.cost,
                                                                             time=solution.time,
                                                                             duration=solution.duration,
                                                                             request=solution.requestPriorityPenalty,
                                                                             inventory=solution.inventoryPriorityPenalty,
                                                                             timeSlots=len(solution.listTimeSlot),
                                                                             nIter=solution.nIter,
                                                                             pu=solution.pu,
                                                                             rho=solution.rho,
                                                                             sigma1=solution.sigma1,
                                                                             sigma2=solution.sigma2,
                                                                             sigma3=solution.sigma3,
                                                                             tau=solution.tau,
                                                                             c=solution.c,
                                                                             alpha=solution.alpha,
                                                                             beta=solution.beta,
                                                                             gamma=solution.gamma,
                                                                             nc=solution.nc,
                                                                             theta=solution.theta,
                                                                             ns=solution.ns
                                                                             )
        outfile.write(line)
    print("Solution is writen in " + solutionName)
