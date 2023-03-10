import pandas as pd
from ALNS import ALNS
from Instance import Instance
import time

def getListFileName():
    #Création de la liste des noms d'instance
    listFileName = []
    #listFileName.append("Small1.xlsx")
    listFileName.append("Small2.xlsx")
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
    #listFileName.append("Medium6.xlsx")
    #listFileName.append("Medium7.xlsx")
    #listFileName.append("Medium8.xlsx")

    #listFileName.append("Large1.xlsx")
    #listFileName.append("Large2.xlsx")
    #listFileName.append("Large3.xlsx")
    #listFileName.append("Large4.xlsx")
    return listFileName

def test(iterationMax=1):
    #Création du dataframe de résultat
    dfResult = pd.DataFrame()

    #Initialisation des variables
    listFileName = getListFileName()
    nbIteration = 0
    dureeMax = 3

    #Pour chaque instance on effectue la boucle
    for fileName in listFileName:
        #Variable permettant de ne donner que le nom de l'instance et pas le ".xlsx"
        name = fileName[0:fileName.find('.')]

        #Affichage de l'avancement des instances
        print("Instance courante : ", fileName)
        instance = Instance("./data/" + fileName)
        nbIteration = 0

        #Modification de la durée max en fonction de l'instance
        if(fileName[0] == 'S'):
            ITER  = 3000
        elif(fileName[0] == 'M'):
            ITER = 6000
        else:
            ITER = 10000

        #Tant que le nombre d'itérations est plus faible que le nombre d'itérations max
        while(nbIteration < iterationMax):
            print("Itération : ", nbIteration + 1, "/", iterationMax)

            #Création du LNS
            alns = ALNS(instance)
            #Récupération des valeurs de la meilleure solution
            #                                                                                               ALGO_ALNS(self, N, PU, rho, sigma1,sigma2,sigma3, tau, C,   alpha,beta,gamma, Nc,  theta, Ns, showLog=False)
            (resultat, iterationbest, Cost_best_solution, TIME, USED_METHODS_UNTIL_LAST_BEST, USED_METHODS) =  alns.solve(ITER, 100, 0.3, 130, 70, 25,       0.1, 0.9995, 0.5, 0.25, 0.25, 2000, 0.5, 10, True)

            #Création de la nouvelle ligne du dataframe
            newRow = {'Instance':name,
            'Evolution_cost': Cost_best_solution,
            'Evolution_iter_best': iterationbest ,
            'Evolution_time_best' :TIME,
            'cost_best': Cost_best_solution[-1],
            'iter_best': iterationbest[-1] ,
            'time_best' :TIME[-1],
            'Iterations':ITER }

            for k in USED_METHODS :
                newRow[k] = round(100*USED_METHODS_UNTIL_LAST_BEST[k]/iterationbest[len(iterationbest)-1],1)
            #Ajout de la ligne au dataframe de résultat
            dfResult = dfResult.append(newRow, True)

            #Incrémentation du nombre d'itérations
            nbIteration += 1

    #Transformation du dataframe en excel pour analyser les résultats
    dfResult.to_excel("./result/results.xlsx")




if __name__ == "__main__":
    """
    fileDataPath = "./data/Small2.xlsx"
    fileDistPath = "./data/MatricesDT.xlsx"
    instance = Instance(fileDataPath, fileDistPath)
    instance.display(True)
    """
    test(1)
