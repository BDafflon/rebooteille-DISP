import time
from alns.ALNS import ALNS
from instance.parser import parseForALNS, parse
import solution.writeSolution as writeSolution
from solution.checkSolution import check
from solution.parser import parseSolution
import alns.writeALNS as writeALNS


def testBase():
    # Instance avec distances entre les points données
    # instance = parseForALNS("./data/Medium6.xlsx")

    # Instance utilisant les coordonnées gps pour les distances
    instance = parse("./data/Medium6/")
    # instance.display(True, False)

    alns = ALNS(instance)
    begin = time.perf_counter()
    # Sans swaps
    solution = alns.solve(100, 0.3, 130, 70, 25, 0.1, 0.9995, 0.5, 0.25, 0.25, 2000)
    # Avec swaps
    # solution = alns.solve(100, 0.3, 130, 70, 25, 0.1, 0.9995, 0.5, 0.25, 0.25, 2000, 0.5, 10, True)
    end = time.perf_counter() - begin
    print("Cost = {cost}".format(cost=alns.evolution_cost[-1]))
    print("Time = {time}/{total}".format(time=alns.evolution_time_best[-1], total=end))
    print(alns.sucess_swap)
    writeSolution.toJson(solution)


if __name__ == "__main__":
    # testBase()

    solution = parseSolution("./data/Medium6/", "./result/Medium6.json")
    solution.display()
    # solution.getListTimeSlot()[0].getListRoute()[0].display(showTimeTable=True)
    # writeSolution.toJson(solution)
    # writeSolution.toCsv(solution, reset=True)
    # writeALNS.toCsv(alns, reset=True)
    # writeALNS.toXlsx(alns, reset=True)
