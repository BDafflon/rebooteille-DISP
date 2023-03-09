"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
import random
import time
import methods
from Route import Route
from TimeSlot import TimeSlot
from Solution import Solution

def repair_randomV2(solution, keptinmemory, instance, repairdontwork):
    """
    Named 'repair random' in the report

    FR :
    On choisit de mettre le client au hasard parmi les time slot existant et un nouveau time slot.
    Lorsque l'on a choisit le time slot, on choisit au hasard une route entre les routes existantes et une nouvelle route.
    on met ensuite le client au hasard dans la route choisie.
    On recommence jusqu'a avoir inserer tous les clients de listClientMissing

    EN :
    We choose to put the client at random among the existing time slot and a new time slot.
    When the time slot has been chosen, a route is chosen at random between the existing routes and a new route.
    Then we put the client at random in the chosen route.
    We start again until we have inserted all the clients of listClientMissing
    """
    initialTime = time.perf_counter()

    # 1 - Recherche des client manquants
    listClientMissing = []
    for timeSlot in solution.listTimeSlot:
        for route in timeSlot.listRoute:
            for client in route.trajet:
                client.setVisited()

    #Réinitialisation des attributs visited des clients
    for client in instance.listClient:
        if (not client.isVisited()):
            listClientMissing.append(client)
        client.setnotVisited()

    #Mélange des positions manquantes dans un ordre aleatoire
    listClientMissing = methods.order_ListClient_random(listClientMissing)

    for clientMissing in listClientMissing:
        positionFound = False
        nbIterations = 0
        nbIterationMax = 30
        while(not positionFound and nbIterations < nbIterationMax):
            solution.checkSolution(False,False)
            if solution.listTimeSlot == [] :
                newTimeSlot = TimeSlot()

                #Création de la nouvelle route
                newRoute = Route()

                #La route fait donc 0 => clientMissing => 0
                newRoute.appendClient(instance.listClient[0])
                newRoute.appendClient(clientMissing)
                newRoute.appendClient(instance.listClient[0])

                newRoute.duration = newRoute.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)

                #Ajout de la route au time slot
                newTimeSlot.addToListRoute(newRoute)
                newTimeSlot.duration=newTimeSlot.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)

                #Ajout du time slot à la solution
                solution.addToListTimeSlot(newTimeSlot)
                positionFound = True
                break

            else :
                if len(solution.listTimeSlot) + 1 > solution.instance.numberTimeSlotMax :
                    timeSlot = solution.listTimeSlot[random.randint(0, len(solution.listTimeSlot) - 1)]
                else :
                    solution.listTimeSlot+=["new"]
                    timeSlot = solution.listTimeSlot[random.randint(0, len(solution.listTimeSlot) - 1)]
                    solution.listTimeSlot.pop(len(solution.listTimeSlot)-1)
                if timeSlot == "new" :
                    newTimeSlot = TimeSlot()
                    #Création de la nouvelle route
                    newRoute = Route()
                    #La route fait donc 0 => clientMissing => 0
                    newRoute.appendClient(instance.listClient[0])
                    newRoute.appendClient(clientMissing)
                    newRoute.appendClient(instance.listClient[0])
                    newRoute.duration = newRoute.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)

                    #Ajout de la route au time slot
                    newTimeSlot.addToListRoute(newRoute)
                    newTimeSlot.duration=newTimeSlot.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)

                    #Ajout du time slot à la solution
                    solution.addToListTimeSlot(newTimeSlot)

                    if(solution.checkSolution(False,True)):
                        #On passe la variable à True et on sort de la boucle
                        positionFound = True
                    else :
                        solution.removeFromListTimeSlot(newTimeSlot)
                        nbIterations += 1
                else :
                    for i in timeSlot.listRoute :
                        if len(i.trajet) <=2 :
                            timeSlot.removeFromListRoute(i)
                    if len(timeSlot.listRoute) + 1 > solution.instance.routePerTimeSlotMax :
                        route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
                        position = random.randint(1, len(route.trajet) - 2)
                        if(route.getTotalFillingRate() + clientMissing.getFillingRate() < instance.vehiculeCapacityMax):
                            #Ajout du client
                            route.insertClient(position, clientMissing)

                            #Si la solution n'est pas compatible on enlève le client
                            if(not solution.checkSolution(False, True)):
                                route.totalFillingRate -= route.trajet[position].getFillingRate()
                                route.trajet.pop(position)
                                nbIterations += 1
                            else:
                                positionFound = True
                    else :
                        timeSlot.listRoute+=["new"]
                        route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
                        timeSlot.listRoute.pop(len(timeSlot.listRoute)-1)
                        if route == "new" :
                            newRoute = Route()

                            #La route fait donc 0 => ckientMissing => 0
                            newRoute.appendClient(instance.listClient[0])
                            newRoute.appendClient(clientMissing)
                            newRoute.appendClient(instance.listClient[0])

                            newRoute.duration = newRoute.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)

                            #Ajout au timeSlot courant
                            timeSlot.addToListRoute(newRoute)

                            if(not solution.checkSolution(False, True)):
                                timeSlot.removeFromListRoute(newRoute)
                                nbIterations += 1
                            else:
                                positionFound = True
                        else :
                            position = random.randint(1, len(route.trajet) - 2)
                            if(route.getTotalFillingRate() + clientMissing.getFillingRate() < instance.vehiculeCapacityMax):
                                #Ajout du client
                                route.insertClient(position, clientMissing)

                                #3 - Vérification de la solution trouvée
                                #Si la solution n'est pas compatible on enlève le client
                                if(not solution.checkSolution(False, True)):
                                    route.totalFillingRate -= route.trajet[position].getFillingRate()
                                    route.trajet.pop(position)
                                    nbIterations += 1
                                else:
                                    positionFound = True
        if nbIterations ==  nbIterationMax :
            solution.copy(keptinmemory)
            repairdontwork["repair_randomV2"] +=1
            break


def repair_randomv1(solution, keptinmemory, instance, repairdontwork):
    '''
    Named 'repair random' in the report

    FR :
    Méthode de réparation aléatoire d'une solution
    1 - Recherche d'un client manquant
    2 - Ajout aléatoire du client
    3 - Vérification de la solution trouvée
    4 - Si la solution ne correspond pas, on supprime le client et on recommence à l'étape 2

    Ici on ne prend pas en compte le fait de mettre un client dans un nouveua time slot tout seul ou dans une route vide d'un time slot existant.

    EN :
    Random repair method of a solution
    1 - Search for a missing client
    2 - Randomly add the client
    3 - Check the solution found
    4 - If the solution doesn't match, we delete the client and start again at step 2

    Here we do not take into account the fact of putting a client in a new time slot or in an empty route of an existing time slot.
    '''
    # 1 - Recherche des client manquants
    listClientMissing = []
    for timeSlot in solution.listTimeSlot:
        for route in timeSlot.listRoute:
            for client in route.trajet:
                client.setVisited()

    #Réinitialisation des attributs visited des clients
    for client in instance.listClient:
        if (not client.isVisited()):
            listClientMissing.append(client)
        client.setnotVisited()

    #Mélange des positions manquantes aleatoirement
    listClientMissing = methods.order_ListClient_random(listClientMissing)

    if solution.listTimeSlot == [] :
        newTimeSlot = TimeSlot()

        #Création de la nouvelle route
        newRoute = Route()

        #La route fait donc 0 => clientMissing => 0
        newRoute.appendClient(instance.listClient[0])
        newRoute.appendClient(instance.listClient[0])

        #Ajout de la route au time slot
        newTimeSlot.addToListRoute(newRoute)

        #Ajout du time slot à la solution
        solution.addToListTimeSlot(newTimeSlot)

    cantinsert=False

    # 2 - Ajout du client à un emplacement random
    positionFound = False

    for clientMissing in listClientMissing:
        positionFound = False
        nbIterations = 0
        nbIterationMax = 50
        while(not positionFound and nbIterations < nbIterationMax):
            #Recherche de l'endroit où l'ajouter
            if (len(solution.listTimeSlot) >= 1):
                timeSlot = solution.listTimeSlot[random.randint(0, len(solution.listTimeSlot) - 1)]
            else:
                timeSlot = solution.listTimeSlot[0]
            if timeSlot.listRoute == [] :
                newRoute = Route()

                #La route fait donc 0 => ckientMissing => 0
                newRoute.appendClient(instance.listClient[0])
                newRoute.appendClient(clientMissing)
                newRoute.appendClient(instance.listClient[0])

                newRoute.duration = newRoute.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)

                #Ajout au timeSlot courant
                timeSlot.addToListRoute(newRoute)

                if(solution.checkSolution(False,True)):
                    #On sort de la boucle et on passe la variable positionFound à True
                    positionFound = True
                    break
                else:
                    #Sinon on supprime la route de la liste du time slot
                    timeSlot.removeFromListRoute(newRoute)
                    cantinsert=True
                    break
            if cantinsert :
                solution.copy(keptinmemory)
                break
            else :
                if(len(timeSlot.listRoute) >= 1):
                    route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
                else:
                    route = timeSlot.listRoute[0]
                if(len(route.trajet) >= 3):
                    position = random.randint(1, len(route.trajet) - 2)
                else:
                    position = 1

                #Si la client est ajoutable d'un point de vue capacité
                if(route.getTotalFillingRate() + clientMissing.getFillingRate() < instance.vehiculeCapacityMax):
                    #Ajout du client
                    route.insertClient(position, clientMissing)

                    #3 - Vérification de la solution trouvée
                    #Si la solution n'est pas compatible on enlève le client
                    if(not solution.checkSolution(False, True)):
                        route.totalFillingRate -= route.trajet[position].getFillingRate()
                        route.trajet.pop(position)
                    else:
                        positionFound = True

            #Mise à jour du nombre d'itérations
            nbIterations += 1

        if cantinsert :
            solution.copy(keptinmemory)
            break
        if nbIterations ==  nbIterationMax  :
            solution.copy(keptinmemory)
            repairdontwork["repair_randomv1"] +=1
            break


def repair_2_regret(solution, keptinmemory, instance, repairdontwork):
    """
    Named 'Repair Regret 2 heuristic' in the report

    FR :
    Ici on cherche pour chaque client sont emplacement qui minimise l'augmentation du cout de la fonction objective lors de son insertion. ON garde aussi la deuxième meilleure place d'insertion de ce client. Ensuite on insere le client qui la difference la plus grande entre sa meilleure place et sa seconde meilleure place.

    EN :
    Here we look for each client to find the location that minimizes the increase in the cost of the objective function when it is inserted. We also keep the second best place of insertion of this client. Then we insert the client that has the biggest difference between its best place and its second best place.
    """
    initialTime = time.perf_counter()
    solutionInitiale = Solution()
    solutionInitiale.copy(solution)

    # 1 - Recherche des clients manquants
    listClientMissing = []
    for timeSlot in solution.listTimeSlot:
        for route in timeSlot.listRoute:
            for client in route.trajet:
                client.setVisited()

    #Réinitialisation des visites des clients
    for client in instance.listClient:
        if (not client.isVisited()) and client.indice != 0 :
            #print(client.indice)
            listClientMissing.append(client)
        client.setnotVisited()
    solution.calculateCost()
    nbclientinserted = 0

    # si la solution est vide
    if solution.listTimeSlot == [] :
        newTimeSlot = TimeSlot()
        #Création de la nouvelle route
        newRoute = Route()

        #La route fait donc 0 => clientMissing => 0
        newRoute.appendClient(instance.listClient[0])
        newRoute.appendClient(instance.listClient[0])

        #Ajout de la route au time slot
        newTimeSlot.addToListRoute(newRoute)

        #Ajout du time slot à la solution
        solution.addToListTimeSlot(newTimeSlot)

    #Boucle de calcul du cout de la fonction objective si on met le client
    while listClientMissing != [] :
        Data_best_client=[]
        Data_second_best_client=[]
        best_client = listClientMissing[0]
        second_best_client = listClientMissing[0]

        for Client in  listClientMissing :
            min_cost = 10000
            min_cost_2 = 10000

            indice_best_timeslot,indice_best_route,indice_best_client=0,0,0
            indice_second_best_timeslot,indice_second_best_route,indice_second_best_client=0,0,0

            for timeSlot in range(len(solution.listTimeSlot)):
                for route in range(len(solution.listTimeSlot[timeSlot].listRoute)):
                    for indiceClient in range(1, len(solution.listTimeSlot[timeSlot].listRoute[route].trajet)):
                        solution.listTimeSlot[timeSlot].listRoute[route].trajet.insert(indiceClient, Client)
                        solution.listTimeSlot[timeSlot].listRoute[route].totalFillingRate  +=  solution.listTimeSlot[timeSlot].listRoute[route].trajet[indiceClient].getFillingRate()
                        solution.calculateCost()
                        cost =  solution.cost
                        if cost < min_cost :
                            min_cost_2 = min_cost
                            min_cost = cost

                            indice_second_best_timeslot = indice_best_timeslot
                            indice_second_best_route = indice_best_route
                            indice_second_best_client = indice_best_client
                            second_best_client = best_client

                            indice_best_timeslot = timeSlot
                            indice_best_route = route
                            indice_best_client = indiceClient
                            best_client = Client

                        solution.listTimeSlot[timeSlot].listRoute[route].totalFillingRate  -=  solution.listTimeSlot[timeSlot].listRoute[route].trajet[indiceClient].getFillingRate()
                        solution.listTimeSlot[timeSlot].listRoute[route].trajet.pop(indiceClient)
                        solution.calculateCost()

            Data_best_client.append([min_cost,indice_best_timeslot,indice_best_route,indice_best_client, best_client])
            Data_second_best_client.append([min_cost_2,indice_second_best_timeslot,indice_second_best_route,indice_second_best_client, second_best_client])

        minimum_cost = 0
        for i in range(len(Data_best_client)):
            difference  = Data_second_best_client[i][0] - Data_best_client[i][0]
            if difference > minimum_cost :
                minimum_cost = difference
                client_to_insert = Data_best_client[i][1:]

        solution.listTimeSlot[client_to_insert[0]].listRoute[client_to_insert[1]].trajet.insert(client_to_insert[2], client_to_insert[3])
        solution.listTimeSlot[client_to_insert[0]].listRoute[client_to_insert[1]].totalFillingRate += solution.listTimeSlot[client_to_insert[0]].listRoute[client_to_insert[1]].trajet[client_to_insert[2]].getFillingRate()

        listClientMissing.remove(client_to_insert[3])

    if not solution.checkSolution() :
        repairdontwork["repair_2_regret"] +=1
        solution.copy(keptinmemory)


def repair_FirstPositionAvailable_maxratio_listClient(solution, keptinmemory, instance, repairdontwork):
    """
    Named 'First position available max ratio' in the report

    FR :
    Méthode de réparation de la solution
    1 - Recherche des clients manquants
    2 - Ajout de la position à la première place disponible dans le premier time slot
    3 - Si aucune place trouvée alors on cherche à créer une nouvelle route dans le même time slot
    4 - Si aucune place n'est trouvée alors on passe au time slot suivant
    5 - Si aucune place n'est trouvée, on essaie d'ajouter un time slot

    EN :
    Method of repairing the solution
    1 - Search for missing clients and sort this list randomly
    2 - Add the position to the first available place in the first time slot
    3 - If no place is found then we try to create a new route in the same time slot
    4 - If no place is found then we go to the next time slot
    5 - If no place is found, we try to add a time slot
    """
    initialTime = time.perf_counter()
    solutionInitiale = Solution()
    solutionInitiale.copy(solution)

    # 1 - Recherche des clients manquants
    listClientMissing = []
    for timeSlot in solution.listTimeSlot:
        for route in timeSlot.listRoute:
            for client in route.trajet:
                client.setVisited()

    #Réinitialisation des visites des clients
    for client in instance.listClient:
        if (not client.isVisited()) and client.indice != 0 :
            #print(client.indice)
            listClientMissing.append(client)
        client.setnotVisited()

    #Tri de la liste selon un critère de la méthode orderListOperator
    listClientMissing = methods.order_ListClient_by_ratio(listClientMissing)

    #Initialisation des variables
    positionFound = False
    NMAX = 10
    n=0
    while not positionFound and n < NMAX and listClientMissing != []:
        for clientMissing in listClientMissing:
            positionFound = False
            for timeSlot in solution.listTimeSlot:
                for route in timeSlot.listRoute:
                    #S'il est possible d'ajouter le clientMissing d'un point de vue de la capacité alors on essaie aux différentes positions
                    if(clientMissing.getFillingRate() + route.getTotalFillingRate() <= instance.vehiculeCapacityMax):
                        # si la route est vide :
                        if len(route.trajet) == 2 :
                            route.trajet.insert(1, clientMissing)
                            route.totalFillingRate += clientMissing.getFillingRate()

                            #Si la solution est compatible alors on sort de la boucle de client
                            if (solution.checkSolution(False,True)):
                                positionFound = True
                                break
                            else:
                                #Sinon on supprime l'ajout
                                route.totalFillingRate -= clientMissing.getFillingRate()
                                route.trajet.pop(1)

                        # si la route a au moins un client
                        for indiceClient in range(1, len(route.trajet) - 1):
                            route.trajet.insert(indiceClient, clientMissing)
                            route.totalFillingRate += clientMissing.getFillingRate()
                            #Si la solution est compatible alors on sort de la boucle de client
                            if (solution.checkSolution(False,True)):
                                positionFound = True
                                break
                            else:
                                #Sinon on supprime l'ajout
                                route.totalFillingRate -= clientMissing.getFillingRate()
                                route.trajet.pop(indiceClient)
                    #Si on a trouvé une position on sort de la boucle de route
                    if(positionFound):
                        break
                if(positionFound):
                    break
                if not positionFound :
                    #Sinon on essaie d'ajouter une route au time slot avec la position manquante
                    #S'il est possible d'ajouter une route au time slot
                    if(len(timeSlot.listRoute) < instance.routePerTimeSlotMax):
                        #Création de la route
                        newRoute = Route()

                        #La route fait donc 0 => ckientMissing => 0
                        newRoute.appendClient(instance.listClient[0])
                        newRoute.appendClient(clientMissing)
                        newRoute.appendClient(instance.listClient[0])

                        newRoute.duration = newRoute.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)
                        #Ajout au timeSlot courant
                        timeSlot.addToListRoute(newRoute)

                        #Si la solution est compatible
                        if(solution.checkSolution(False,True)):
                            #On sort de la boucle et on passe la variable positionFound à True
                            positionFound = True
                            break
                        else:
                            #Sinon on supprime la route de la liste du time slot
                            timeSlot.removeFromListRoute(newRoute)

                #Si on a trouvé une solution, on sort de la liste de time slot
                if(positionFound):
                    break
                if not positionFound :
                    #Sinon on essaie d'ajouter un time slot si c'est possible
                    if(len(solution.listTimeSlot) < instance.numberTimeSlotMax):
                        #Création d'un time slot
                        newTimeSlot = TimeSlot()

                        #Création de la nouvelle route
                        newRoute = Route()

                        #La route fait donc 0 => clientMissing => 0
                        newRoute.appendClient(instance.listClient[0])
                        newRoute.appendClient(clientMissing)
                        newRoute.appendClient(instance.listClient[0])

                        #Ajout de la route au time slot
                        newTimeSlot.addToListRoute(newRoute)

                        #Ajout du time slot à la solution
                        solution.addToListTimeSlot(newTimeSlot)

                        #Si la solution est compatible
                        if(solution.checkSolution(False,True)):
                            #On passe la variable à True et on sort de la boucle
                            positionFound = True
                            break
                        else:
                            #Sinon on supprime le time slot de la solution
                            solution.removeFromListTimeSlot(newTimeSlot)

            #Si on a pu ajouter aucun client à aucune route, créer aucune route et créer aucun time slot alors on s'arrête pour cet opérateur et on sort de la méthode
            if (not positionFound) :
                solution.copy(solutionInitiale)
                listClientMissing = methods.order_ListClient_by_ratio(listClientMissing)
                n+=1
                break

    if n ==NMAX :
        solution.copy(keptinmemory)
        repairdontwork["repair_FirstPositionAvailable_maxratio_listClient"] +=1


def repair_FirstPositionAvailable_randomlistClient(solution, keptinmemory, instance, repairdontwork):
    """
    Named 'First position available random' in the report

    FR :
    Méthode de réparation de la solution
    1 - Recherche des clients manquants et tri de cette liste aleatoirement
    2 - Ajout de la position à la première place disponible dans le premier time slot
    3 - Si aucune place trouvée alors on cherche à créer une nouvelle route dans le même time slot
    4 - Si aucune place n'est trouvée alors on passe au time slot suivant
    5 - Si aucune place n'est trouvée, on essaie d'ajouter un time slot

    EN :
    Method of repairing the solution
    1 - Search for missing clients and sort this list randomly
    2 - Add the position to the first available place in the first time slot
    3 - If no place is found then we try to create a new route in the same time slot
    4 - If no place is found then we go to the next time slot
    5 - If no place is found, we try to add a time slot
    """
    initialTime = time.perf_counter()
    solutionInitiale = Solution()
    solutionInitiale.copy(solution)

    # 1 - Recherche des clients manquants
    listClientMissing = []
    for timeSlot in solution.listTimeSlot:
        for route in timeSlot.listRoute:
            for client in route.trajet:
                client.setVisited()

    #Réinitialisation des visites des clients
    for client in instance.listClient:
        if (not client.isVisited()) and client.indice != 0 :
            #print(client.indice)
            listClientMissing.append(client)
        client.setnotVisited()

    #Tri de la liste selon un critère de la méthode orderListOperator
    listClientMissing = methods.order_ListClient_random(listClientMissing)

    #Initialisation des variables
    positionFound = False
    NMAX = 10
    n=0
    while not positionFound and n < NMAX and listClientMissing != []:
        for clientMissing in listClientMissing:
            positionFound = False
            for timeSlot in solution.listTimeSlot:
                for route in timeSlot.listRoute:
                    #S'il est possible d'ajouter le clientMissing d'un point de vue de la capacité alors on essaie aux différentes positions
                    if(clientMissing.getFillingRate() + route.getTotalFillingRate() <= instance.vehiculeCapacityMax):
                        # si la route est vide :
                        if len(route.trajet) == 2 :
                            route.trajet.insert(1, clientMissing)
                            route.totalFillingRate += clientMissing.getFillingRate()

                            #Si la solution est compatible alors on sort de la boucle de client
                            if (solution.checkSolution(False,True)):
                                positionFound = True
                                break
                            else:
                                #Sinon on supprime l'ajout
                                route.totalFillingRate -= clientMissing.getFillingRate()
                                route.trajet.pop(1)

                        # si la route a au moins un client
                        for indiceClient in range(1, len(route.trajet) - 1):
                            route.trajet.insert(indiceClient, clientMissing)
                            route.totalFillingRate += clientMissing.getFillingRate()
                            #Si la solution est compatible alors on sort de la boucle de client
                            if (solution.checkSolution(False,True)):
                                positionFound = True
                                break
                            else:
                                #Sinon on supprime l'ajout
                                route.totalFillingRate -= clientMissing.getFillingRate()
                                route.trajet.pop(indiceClient)

                    #Si on a trouvé une position on sort de la boucle de route
                    if(positionFound):
                        break
                if(positionFound):
                    break
                if not positionFound :
                    #Sinon on essaie d'ajouter une route au time slot avec la position manquante
                    #S'il est possible d'ajouter une route au time slot
                    if(len(timeSlot.listRoute) < instance.routePerTimeSlotMax):
                        #Création de la route
                        newRoute = Route()

                        #La route fait donc 0 => ckientMissing => 0
                        newRoute.appendClient(instance.listClient[0])
                        newRoute.appendClient(clientMissing)
                        newRoute.appendClient(instance.listClient[0])

                        newRoute.duration = newRoute.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)

                        #Ajout au timeSlot courant
                        timeSlot.addToListRoute(newRoute)

                        #Si la solution est compatible
                        if(solution.checkSolution(False,True)):
                            #On sort de la boucle et on passe la variable positionFound à True
                            positionFound = True
                            break
                        else:
                            #Sinon on supprime la route de la liste du time slot
                            timeSlot.removeFromListRoute(newRoute)

                #Si on a trouvé une solution, on sort de la liste de time slot
                if(positionFound):
                    break
                if not positionFound :
                    #Sinon on essaie d'ajouter un time slot si c'est possible
                    if(len(solution.listTimeSlot) < instance.numberTimeSlotMax):
                        #Création d'un time slot
                        newTimeSlot = TimeSlot()

                        #Création de la nouvelle route
                        newRoute = Route()

                        #La route fait donc 0 => clientMissing => 0
                        newRoute.appendClient(instance.listClient[0])
                        newRoute.appendClient(clientMissing)
                        newRoute.appendClient(instance.listClient[0])

                        #Ajout de la route au time slot
                        newTimeSlot.addToListRoute(newRoute)

                        #Ajout du time slot à la solution
                        solution.addToListTimeSlot(newTimeSlot)

                        #Si la solution est compatible
                        if(solution.checkSolution(False,True)):
                            #On passe la variable à True et on sort de la boucle
                            positionFound = True
                            break
                        else:
                            #Sinon on supprime le time slot de la solution
                            solution.removeFromListTimeSlot(newTimeSlot)

            #Si on a pu ajouter aucun client à aucune route, créer aucune route et créer aucun time slot alors
            #on s'arrête pour cet opérateur et on sort de la méthode
            if (not positionFound) :
                solution.copy(solutionInitiale)
                listClientMissing = methods.order_ListClient_random(listClientMissing)
                n+=1
                break

    if n ==NMAX :
        solution.copy(keptinmemory)
        repairdontwork["repair_FirstPositionAvailable_randomlistClient"] +=1


def repair_random_best_insertion(solution, keptinmemory, instance, repairdontwork) :
    """
    Named 'Best insertion random' in the report

    FR :
    Pour chaque client, on cherche l'endroit qui minimise l'augmentation du cout de la fonction objective lors de son insertion dans la solution. La liste des clients à inserer est construite de manière aléatoire.

    EN :
    For each client, we look for the place that minimizes the increase of the cost of the objective function when it is inserted in the solution. The list of clients to be inserted is built randomly.
    """
    initialTime = time.perf_counter()
    solutionInitiale = Solution()
    solutionInitiale.copy(solution)

    # 1 - Recherche des clients manquants
    listClientMissing = []
    for timeSlot in solution.listTimeSlot:
        for route in timeSlot.listRoute:
            for client in route.trajet:
                client.setVisited()

    #Réinitialisation des visites des clients
    for client in instance.listClient:
        if (not client.isVisited()) and client.indice != 0 :
            #print(client.indice)
            listClientMissing.append(client)
        client.setnotVisited()

    #Tri de la liste selon un critère de la méthode orderListOperator
    listClientMissing = methods.order_ListClient_random(listClientMissing)

    if solution.listTimeSlot == [] :
        newTimeSlot = TimeSlot()

        #Création de la nouvelle route
        newRoute = Route()

        #La route fait donc 0 => clientMissing => 0
        newRoute.appendClient(instance.listClient[0])
        newRoute.appendClient(instance.listClient[0])

        #Ajout de la route au time slot
        newTimeSlot.addToListRoute(newRoute)

        #Ajout du time slot à la solution
        solution.addToListTimeSlot(newTimeSlot)
    solution.calculateCost()

    #Boucle de calcul du cout de la fonction objective si on met le client
    for Client in  listClientMissing :
        min_cost = 100000
        indice_best_timeslot, indice_best_route, indice_best_client = 0, 0, 0

        if len(solution.listTimeSlot)+1 <= solution.instance.numberTimeSlotMax :
            newTimeSlot = TimeSlot()

            #Ajout du time slot à la solution
            solution.addToListTimeSlot(newTimeSlot)

        for timeSlot in range(len(solution.listTimeSlot)):
            if len(solution.listTimeSlot[timeSlot].listRoute) + 1 <= solution.instance.routePerTimeSlotMax :
                newRoute = Route()
                newRoute.appendClient(instance.listClient[0])
                newRoute.appendClient(instance.listClient[0])

                newRoute.duration = newRoute.getDuration(instance.timeTravel,instance.fixedCollectionTime,instance.collectionTimePerCrate)
                #Ajout au timeSlot courant
                solution.listTimeSlot[timeSlot].addToListRoute(newRoute)

            for route in range(len(solution.listTimeSlot[timeSlot].listRoute)):
                for indiceClient in range(1, len(solution.listTimeSlot[timeSlot].listRoute[route].trajet)):

                    solution.listTimeSlot[timeSlot].listRoute[route].trajet.insert(indiceClient, Client)
                    solution.listTimeSlot[timeSlot].listRoute[route].totalFillingRate  +=  solution.listTimeSlot[timeSlot].listRoute[route].trajet[indiceClient].getFillingRate()
                    solution.calculateCost()
                    cost =  solution.cost
                    if cost < min_cost :
                        min_cost = cost
                        indice_best_timeslot = timeSlot
                        indice_best_route = route
                        indice_best_client = indiceClient

                    solution.listTimeSlot[timeSlot].listRoute[route].totalFillingRate  -=  solution.listTimeSlot[timeSlot].listRoute[route].trajet[indiceClient].getFillingRate()
                    solution.listTimeSlot[timeSlot].listRoute[route].trajet.pop(indiceClient)
                    solution.calculateCost()

        solution.listTimeSlot[indice_best_timeslot].listRoute[indice_best_route].trajet.insert(indice_best_client, Client)
        solution.listTimeSlot[indice_best_timeslot].listRoute[indice_best_route].totalFillingRate += solution.listTimeSlot[indice_best_timeslot].listRoute[indice_best_route].trajet[indice_best_client].getFillingRate()

    if not solution.checkSolution(False,True) :
        repairdontwork["repair_random_best_insertion"] +=1
        solution.copy(keptinmemory)


def repair_max_ratio_best_insertion(solution, keptinmemory, instance, repairdontwork) :
    """
    Named 'Best insertion max ratio' in the report

    FR :
    Pour chaque client, on cherche l'endroit qui minimise l'augmentation du cout de la fonction objective lors de son insertion dans la solution. La liste des clients à inserer est construite de manière decroissante du ratio.

    EN :
    For each client, we look for the place that minimizes the increase of the cost of the objective function when it is inserted in the solution. The list of clients to be inserted is built in the decreasing order of the ratio
    """
    initialTime = time.perf_counter()
    solutionInitiale = Solution()
    solutionInitiale.copy(solution)

    # 1 - Recherche des clients manquants
    listClientMissing = []
    for timeSlot in solution.listTimeSlot:
        for route in timeSlot.listRoute:
            for client in route.trajet:
                client.setVisited()

    #Réinitialisation des visites des clients
    for client in instance.listClient:
        if (not client.isVisited()) and client.indice != 0 :
            listClientMissing.append(client)
        client.setnotVisited()

    #Tri de la liste selon un critère de la méthode orderListOperator
    listClientMissing = methods.order_ListClient_by_ratio(listClientMissing)
    if solution.listTimeSlot == [] :
        newTimeSlot = TimeSlot()

        #Création de la nouvelle route
        newRoute = Route()

        #La route fait donc 0 => clientMissing => 0
        newRoute.appendClient(instance.listClient[0])
        newRoute.appendClient(instance.listClient[0])

        #Ajout de la route au time slot
        newTimeSlot.addToListRoute(newRoute)

        #Ajout du time slot à la solution
        solution.addToListTimeSlot(newTimeSlot)
    solution.calculateCost()

    #Boucle de calcul du cout de la fonction objective si on met le client
    for Client in  listClientMissing :
        min_cost = 100000
        indice_best_timeslot,indice_best_route,indice_best_client=0,0,0
        for timeSlot in range(len(solution.listTimeSlot)):
            for route in range(len(solution.listTimeSlot[timeSlot].listRoute)):
                for indiceClient in range(1, len(solution.listTimeSlot[timeSlot].listRoute[route].trajet)):
                    solution.listTimeSlot[timeSlot].listRoute[route].trajet.insert(indiceClient, Client)
                    solution.listTimeSlot[timeSlot].listRoute[route].totalFillingRate  +=  solution.listTimeSlot[timeSlot].listRoute[route].trajet[indiceClient].getFillingRate()
                    solution.calculateCost()
                    cost =  solution.cost
                    if cost < min_cost :
                        min_cost = cost
                        indice_best_timeslot = timeSlot
                        indice_best_route = route
                        indice_best_client = indiceClient

                    solution.listTimeSlot[timeSlot].listRoute[route].totalFillingRate  -=  solution.listTimeSlot[timeSlot].listRoute[route].trajet[indiceClient].getFillingRate()
                    solution.listTimeSlot[timeSlot].listRoute[route].trajet.pop(indiceClient)
                    solution.calculateCost()

        solution.listTimeSlot[indice_best_timeslot].listRoute[indice_best_route].trajet.insert(indice_best_client, Client)
        solution.listTimeSlot[indice_best_timeslot].listRoute[indice_best_route].totalFillingRate += solution.listTimeSlot[indice_best_timeslot].listRoute[indice_best_route].trajet[indice_best_client].getFillingRate()

    if not solution.checkSolution(False,True) :
        repairdontwork["repair_random_best_insertion"] +=1
        solution.copy(keptinmemory)
