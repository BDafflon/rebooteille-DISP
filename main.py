import pandas as pd
from alns.ALNS import ALNS
import time
from instance.parser import parse
import solution.writeSolution as writeSolution
import alns.writeALNS as writeALNS

if __name__ == "__main__":
    fileDataPath = "./data/Medium6.xlsx"
    fileDistPath = "./data/MatricesDT.xlsx"
    instance = parse(fileDataPath)
    #instance.display(True)
    alns = ALNS(instance)
    solution = alns.solve(100, 0.3, 130, 70, 25, 0.1, 0.9995, 0.5, 0.25, 0.25, 2000, 0.5, 10, False)
    #solution.display()
    print("Cost = {cost}".format(cost=alns.evolution_cost[-1]))
    print(solution.getCost())
    print("Time = {time}".format(time=alns.evolution_time_best[-1]))
    print(solution.time)
    writeSolution.toJson(solution)
    #writeSolution.toCsv(solution, reset=True)
    #writeALNS.toCsv(alns, reset=True)
    #writeALNS.toXlsx(alns, reset=True)
