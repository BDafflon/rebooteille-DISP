import pandas as pd
from ALNS import ALNS
from Instance import Instance
import time
import writeSolution
import writeALNS

def getListFileName():
    #Création de la liste des noms d'instance
    listFileName = []
    #listFileName.append("Small1.xlsx")
    #listFileName.append("Small2.xlsx")
    #listFileName.append("Small3.xlsx")
    #listFileName.append("Small4.xlsx")
    #listFileName.append("Small5.xlsx")
    #listFileName.append("Small6.xlsx")
    #listFileName.append("Small7.xlsx")
    #listFileName.append("Small8.xlsx")

    #listFileName.append("Medium1.xlsx")
    #listFileName.append("Medium2.xlsx")
    #listFileName.append("Medium3.xlsx")
    #listFileName.append("Medium4.xlsx")
    #listFileName.append("Medium5.xlsx")
    listFileName.append("Medium6.xlsx")
    #listFileName.append("Medium7.xlsx")
    #listFileName.append("Medium8.xlsx")

    #listFileName.append("Large1.xlsx")
    #listFileName.append("Large2.xlsx")
    #listFileName.append("Large3.xlsx")
    #listFileName.append("Large4.xlsx")
    return listFileName


if __name__ == "__main__":
    fileDataPath = "./data/Medium6.xlsx"
    fileDistPath = "./data/MatricesDT.xlsx"
    instance = Instance(fileDataPath, fileDistPath)
    #instance.display(True)
    alns = ALNS(instance)
    solution = alns.solve(100, 0.3, 130, 70, 25, 0.1, 0.9995, 0.5, 0.25, 0.25, 2000, 0.5, 10, False)
    print("Cost = {cost}".format(cost=alns.evolution_cost[-1]))
    print(solution.getCost())
    print("Time = {time}".format(time=alns.evolution_time_best[-1]))
    print(solution.time)
    #writeSolution.toCsv(solution, reset=True)
    #writeALNS.toCsv(alns, reset=True)
    #writeALNS.toXlsx(alns, reset=True)
