"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
import random
import time

def order_ListClient_random(listClient):
        """
        FR :
        Méthode visant à trier la liste des clients détruits de manière aléatoire

        EN :
        Method to sort the list of destroyed clients randomly
        """
        isDepotToAdd = False
        if(len(listClient) > 0):
            if(listClient[0].getIndice() == 0):
                clientDepot = listClient[0]
                listClient = listClient[1:]
                isDepotToAdd = True

            random.shuffle(listClient)     #Mélange de la liste donnée

            if(isDepotToAdd):
                listClient = [clientDepot] + listClient

        #On retourne la liste initiale mélangée
        return listClient

def order_ListClient_by_ratio(listClient):
        """
        FR :
        Methode visant à trier la liste des clients détruits dans l'ordre decroissant des rapports fillingRate/capacity

        EN :
        Method to sort the list of destroyed clients in descending order of fillingRate/capacity ratios

        """
        isDepotToAdd = False

        if(len(listClient) > 0):
            if(listClient[0].getIndice() == 0):
                clientDepot = listClient[0]
                listClient = listClient[1:]
                isDepotToAdd = True

            #Calcul du ratio filling rate / capacity pour tous les clients
            ratio = {client : client.getFillingRate() / client.getCapacity() for client in listClient}
            listClient=[]
            for k, v in sorted(ratio.items(), key=lambda x: x[1],reverse=True):
                listClient.append(k)

        if(isDepotToAdd):
            listClient = [clientDepot] + listClient

        return listClient

def swap_intra_route(solution) :
    '''
    Named "swap intra route" in the report

    FR :
    Méthode d'échange de deux clients au sein d'une meme route

    EN :
    Method for exchanging two clients within the same route
    '''
    #Copie de la solution initiale
    solutionInitiale = Solution()
    solutionInitiale.copy(solution)

    #initialisation des variables
    nbIteration = 0
    nbIterationMax = 10
    solutionInitaleAssigned = True

    #Tant qu'on a pas fait 10 itérations et (que la solution est incompatible ou que la solution
    #initiale a été réassignée)
    while (nbIteration < nbIterationMax and (not solution.checkSolution() or solutionInitaleAssigned)):
        solutionInitaleAssigned = False
        #Récupération des time slots à switcher
        route_assez_longue = False
        while not route_assez_longue :
            timeSlot= solution.listTimeSlot[random.randint(0,len(solution.listTimeSlot) - 1)]
            for i in timeSlot.listRoute :
                if len(i.trajet) >=4 :
                    route_assez_longue = True

        route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]

        while len(route.trajet) <= 3  :
            route= timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]

        #Récupération des positions dans les trajets
        positionA = random.randint(1,len(route.trajet) - 2)
        positionB = random.randint(1,len(route.trajet) - 2)

        #Assignation des valeurs de client A et B
        clientA = route.trajet[positionA]
        clientB = route.trajet[positionB]

        #Assignation du client B à la route A
        route.trajet.insert(positionA, clientB)
        #Suppression du client A de la route A
        route.trajet.pop(positionA + 1)

        #Assignation du client A à la route B
        route.trajet.insert(positionB, clientA)
        #Suppression du client B de la route B
        route.trajet.pop(positionB + 1)

        #Vérification de la solution
        if(not solution.checkSolution()):
            #Si la solution n'est pas compatible alors on réaffecte la solution de départ
            solutionInitaleAssigned = True
            solution.copy(solutionInitiale)
        nbIteration += 1

    #Vérification de la solution
    if(not solution.checkSolution()):
        #Si la solution n'est pas compatible alors on réaffecte la solution de départ
        solution.copy(solutionInitiale)


def swap_inter_route(solution) :
    '''
    Named "swap inter route" in the report

    FR :
    Méthode d'échange de deux clients au sein de deux routes strictement differentes

    EN :
    Method for exchanging two clients within two strictly different routes
    '''
    #Copie de la solution initiale
    solutionInitiale = Solution()
    solutionInitiale.copy(solution)

    #initialisation des variables
    nbIteration = 0
    nbIterationMax = 10
    solutionInitaleAssigned = True
    routes_vides = 0
    for i in solution.listTimeSlot:
        for j in i.listRoute :
            if len(j.trajet) < 3 :
                routes_vides+=1

    Nbroutes = sum([len(i.listRoute)  for i in solution.listTimeSlot] )
    if Nbroutes <= 2 and routes_vides != 0:
        return

    #Tant qu'on a pas fait 10 itérations et (que la solution est incompatible ou que la solution
    #initiale a été réassignée)
    while (nbIteration < nbIterationMax and (not solution.checkSolution() or solutionInitaleAssigned)):
        solutionInitaleAssigned = False

        #Récupération des time slots à switcher
        timeSlotA = solution.listTimeSlot[random.randint(0,len(solution.listTimeSlot) - 1)]
        timeSlotB = solution.listTimeSlot[random.randint(0,len(solution.listTimeSlot) - 1)]

        while  timeSlotB == timeSlotA and len(timeSlotA.listRoute) < 2  :
            timeSlotA = solution.listTimeSlot[random.randint(0,len(solution.listTimeSlot) - 1)]

        #Récupération des routes dans les time slots
        routeA = timeSlotA.listRoute[random.randint(0, len(timeSlotA.listRoute) - 1)]
        routeB = timeSlotB.listRoute[random.randint(0, len(timeSlotB.listRoute) - 1)]
        while routeB == routeA :
            routeB = timeSlotB.listRoute[random.randint(0, len(timeSlotB.listRoute) - 1)]

        #Récupération des positions dans les trajets
        positionA = random.randint(1,len(routeA.trajet) - 2)
        positionB = random.randint(1,len(routeB.trajet) - 2)

        #Assignation des valeurs de client A et B
        clientA = routeA.trajet[positionA]
        clientB = routeB.trajet[positionB]

        #Assignation du client B à la route A
        routeA.trajet.insert(positionA, clientB)
        #Suppression du client A de la route A
        routeA.trajet.pop(positionA + 1)

        #Assignation du client A à la route B
        routeB.trajet.insert(positionB, clientA)
        #Suppression du client B de la route B
        routeB.trajet.pop(positionB + 1)

        #Vérification de la solution
        if(not solution.checkSolution()):
            #Si la solution n'est pas compatible alors on réaffecte la solution de départ
            solutionInitaleAssigned = True
            solution.copy(solutionInitiale)
        nbIteration += 1

    #Vérification de la solution
    if(not solution.checkSolution()):
        #Si la solution n'est pas compatible alors on réaffecte la solution de départ
        solution.copy(solutionInitiale)


def choose_destroy_method(destroy_methods, Weights_destroy):
    """
    FR:
    Fonction choisissant une méthode de destruction suivant les probabilités associées

    EN:
    Function choosing a destruction method according to the associated probabilities
    """
    s = sum(Weights_destroy.values())
    PROBAS = [Weights_destroy[i]/s for i in Weights_destroy]
    destroy = random.choices(destroy_methods,PROBAS)
    return destroy[0]


def choose_repair_method(repair_methods, Weights_repair):
    """
    FR:
    Fonction choisissant une méthode de reconstruction suivant les probabilités associées

    EN:
    Function choosing a repair method according to the associated probabilities
    """
    s=sum(Weights_repair.values())
    PROBAS = [Weights_repair[i]/s for i in Weights_repair]
    repair = random.choices(repair_methods,PROBAS)
    return repair[0]

def update_weights(rho,Weights_destroy,Weights_repair,Success_destroy,Success_repair,Used_destroy_methods,Used_repair_methods):
    """
    FR:
    Mise à jour des poids des methodes de destruction et de repair suivant les formules expliquées dans le rapport

    EN:
    Updating the weights of the destruction and repair methods according to the formulas explained in the report
    """
    for i in Weights_destroy:
        if Used_destroy_methods[i] !=0 :
            Weights_destroy[i] = (( 1 - rho ) * Weights_destroy[i]) + (rho * (Success_destroy[i]/Used_destroy_methods[i]))
        else :
            Weights_destroy[i] = ( 1 - rho ) * Weights_destroy[i]

    for i in Weights_repair:
        if Used_repair_methods[i] !=0 :
            Weights_repair[i] = (( 1 - rho ) * Weights_repair[i]) + (rho * (Success_repair[i]/Used_repair_methods[i]))
        else :
            Weights_repair[i] = ( 1 - rho ) * Weights_repair[i]

    return Weights_destroy, Weights_repair
