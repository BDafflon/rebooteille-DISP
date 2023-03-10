import json
import sys
from ALNS import ALNS
from Instance import Instance
from Solution import Solution

if __name__ == "__main__":
    if (len(sys.argv) < 2 or len(sys.argv) > 4):
        print("Usage : python3 writeInJSON.py {Instance} (Solution folder)")
        exit()

    #INITIALISATION
    fileDataPath = sys.argv[1]
    fileDistPath = "./data/MatricesDT.xlsx"
    solutionPath = "./result/"
    if(len(sys.argv) > 3):
        solutionPath = sys.argv[3]

    pu = 100
    rho = 0.3
    sigma1 = 130
    sigma2 = 70
    sigma3 = 25
    tau = 0.1
    c = 0.9995
    alpha = 0.5
    beta = 0.25
    gamma = 0.25
    nc = 2000
    theta = 0.5
    ns = 10

    #INSTANCIATION
    instance = Instance(fileDataPath, fileDistPath)
    name = instance.getName()
    if(name[0] == 'S'):
        nIter = 3000
    elif(name[0] == 'M'):
        nIter = 6000
    else:
        nIter = 10000

    dictResult = {
        "name": name,
        "N": nIter,
        "PU": pu,
        "rho": rho,
        "sigma1": sigma1,
        "sigma2": sigma2,
        "sigma3": sigma3,
        "tau": tau,
        "C": c,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "Nc": nc,
        "theta": theta,
        "Ns": ns,
        "Z1": Solution.facteurZ1,
        "Z2": Solution.facteurZ2,
        "Z3": Solution.facteurZ3,
        "Z4": Solution.facteurZ4,
        "routing": []
    }
    alns = ALNS(instance)

    #EXECUTION
    print("Solving " + name)
    (solution, iterationbest, Cost_best_solution, TIME, USED_METHODS_UNTIL_LAST_BEST, USED_METHODS) =  alns.solve(nIter, pu, rho, sigma1, sigma2, sigma3, tau, c, alpha, beta, gamma, nc, theta, ns)

    #AFFICHAGE
    #instance.display(True)
    #solution.display()

    #SAUVEGARDE
    dictResult["cost"] = solution.getCost()
    idTimeSlot = 0
    for timeSlot in solution.getListTimeSlot():
        idTimeSlot += 1
        dictTimeSlot = {
            "id": idTimeSlot,
            "duration": timeSlot.duration,
            "timeSlot": []
        }
        idRoute = 0
        for route in timeSlot.getListRoute():
            idRoute += 1
            dictRoute = {
                "id": idRoute,
                "duration": route.duration,
                "route": []
            }
            for client in route.getTrajet():
                dictRoute["route"].append(client.getIndice())
                """ WITH NEW INSTANCE
                dictClient = {
                    "id": client.getIndice(),
                    "order": 0,
                    "name": "client",
                    "latitude": 0,
                    "longitute": 0
                }
                dictRoute["route"].append(dictClient)
                """
            dictTimeSlot["timeSlot"].append(dictRoute)
        dictResult["routing"].append(dictTimeSlot)

    solutionName = solutionPath + name + ".json"
    with open(solutionName, "w") as outfile:
        json.dump(dictResult, outfile, indent=4)
    print("Solution is saved in " + solutionName)

    del dictRoute
    del dictTimeSlot
    del dictResult
