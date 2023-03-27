"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
import random
import time


def destroy_random(solution, degres_destruction):
    """
    Named 'random removal' in the report
    FR :
    Opérateur de destruction aléatoire d'un nombre de clients donné par le degré de destruction

    EN :
    Operator of random destruction of a number of clients given by the degree of destruction
    """
    initialTime = time.perf_counter()

    # Calcul du nombre de clients à détruire
    nbClientToDestroy = degres_destruction

    nbIteration = 0
    # Boucle de destruction des clients
    while nbIteration < nbClientToDestroy:
        # Identification du client à détruire
        if len(solution.listTimeSlot) > 1:
            timeSlot = solution.listTimeSlot[random.randint(0, len(solution.listTimeSlot) - 1)]
        else:
            timeSlot = solution.listTimeSlot[0]

        if len(timeSlot.listRoute) > 1:
            route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
        else:
            route = timeSlot.listRoute[0]

        if len(route.trajet) >= 3:
            position = random.randint(1, len(route.trajet) - 2)

            # Destruction du client
            route.trajet.pop(position)

            # Incrémentation du compteur d'itérations
            nbIteration += 1

    # Calcul du coût de la solution
    solution.calculateCost()


def destroy_Client_with_a_request_placed_at_the_end_of_the_solution(solution, degres_destruction, listClient):
    """
    Named 'destroy client with a request' in the report

    FR :
    Opérateur de destruction basé sur le request des clients.
    Si le client est en fin de solution et qu'elle est requested alors on peut la supprimer

    EN :
    Destruction operator based on client request.
    If the client is at the end of the solution and it is requested then it can be deleted
    """
    # Calcul du nombre de clients à détruire
    nbClientRequested = 0
    divideClientBy = 3

    for client in listClient:
        if client.getIsRequested():
            nbClientRequested += 1

    numberOfClientToDestroy = degres_destruction
    if nbClientRequested == 0:
        nbClientRequested = 1

    if nbClientRequested < degres_destruction:
        numberOfClientToDestroy = nbClientRequested

    # Initialisation des variables
    allClientDestroyed = False
    nbClientDestroyed = 0
    indiceClient = 0

    if len(solution.listTimeSlot) >= 2:
        for indiceTimeSlot in range(len(solution.listTimeSlot) - 1, 0, -1):
            timeSlot = solution.listTimeSlot[indiceTimeSlot]
            for route in timeSlot.listRoute:
                indiceClient = 0
                for client in route.trajet:
                    if client.getIsRequested():
                        route.totalQuantity -= route.trajet[indiceClient].getQuantity()
                        route.trajet.pop(indiceClient)
                        nbClientDestroyed += 1
                        if nbClientDestroyed >= numberOfClientToDestroy:
                            allClientDestroyed = True
                            break
                    indiceClient += 1
                if allClientDestroyed:
                    break
            if allClientDestroyed:
                break


def destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution(solution, degres_destruction):
    """
    Named 'Destroy client High ratio' in the report

    FR:
    Opérateur de destruction visant à détruire les clients ayant un ratio élevé en fin de solution
    Ratio = filling rate / capacity (+1 si le client est requested)

    EN :
    Destruction operator to destroy customers with a high ratio at the end of the solution
    Ratio = filling rate / capacity (+1 if the customer is requested)
    """
    # Initialisation des variables
    numberOfClientToDestroy = degres_destruction
    nbRouteDestroyed = 0
    clientDestroyed = False
    ratioMax = 2

    # Tant qu'on n'a pas détruit tous les clients demandés on recommence
    while nbRouteDestroyed < numberOfClientToDestroy and ratioMax >= 0:
        clientDestroyed = False
        for indiceTimeSlot in range(len(solution.listTimeSlot) - 1, 0, -1):
            timeSlot = solution.listTimeSlot[indiceTimeSlot]
            for route in timeSlot.listRoute:
                for indiceClient in range(1, len(route.trajet) - 1):
                    client = route.trajet[indiceClient]

                    # Calcul du ratio fillingRate / capacity
                    ratio = client.getQuantity() / client.getCapacity()

                    # Si le client est requested alors on ajoute 1
                    if client.getIsRequested():
                        ratio += 1

                    # Si le ratio est supérieur à la borne max, alors on supprime le client
                    if ratio >= ratioMax:
                        # Suppression du client
                        route.totalQuantity -= route.trajet[indiceClient].getQuantity()
                        route.trajet.pop(indiceClient)

                        # Update des variables de boucles
                        nbRouteDestroyed += 1
                        clientDestroyed = True

                        # Sort de la boucle de client
                        break
                # Sort de la boucle de route
                if clientDestroyed:
                    break
            # Sort de la boucle de time slot
            if clientDestroyed:
                break
        if not clientDestroyed:
            ratioMax -= 0.1


def destroy_worst_clients(solution, degres_destruction):
    """
    Named 'worst removal' in the report

    FR :
    detruit les clients qui sont très lourds en terme de cout de la fonction objective

    EN :
    destroys customers who are very heavy in terms of cost of the objective function
    """
    nbClientToDestroy = degres_destruction
    nbIteration = 0

    # Boucle de destruction des clients
    while nbIteration < nbClientToDestroy:
        # for each client we initialize these variables
        gain = 0
        indice_worst_timeslot = 0
        indice_worst_route = 0
        indice_worst_client = 0

        for timeSlot in range(len(solution.listTimeSlot)):
            for route in range(len(solution.listTimeSlot[timeSlot].listRoute)):
                for indiceClient in range(1, len(solution.listTimeSlot[timeSlot].listRoute[route].trajet) - 1):
                    solution.calculateCost()
                    before = solution.cost
                    client = solution.listTimeSlot[timeSlot].listRoute[route].trajet.pop(indiceClient)
                    solution.calculateCost()
                    after = solution.cost
                    new_gain = before - after
                    #  the objective is to find the maximum "gain" for each client
                    if new_gain > gain:
                        gain = new_gain
                        indice_worst_timeslot = timeSlot
                        indice_worst_route = route
                        indice_worst_client = indiceClient
                    solution.listTimeSlot[timeSlot].listRoute[route].trajet.insert(indiceClient, client)
        value = solution.listTimeSlot[indice_worst_timeslot].listRoute[indice_worst_route].trajet[
            indice_worst_client].getQuantity()
        solution.listTimeSlot[indice_worst_timeslot].listRoute[indice_worst_route].totalQuantity -= value
        solution.listTimeSlot[indice_worst_timeslot].listRoute[indice_worst_route].trajet.pop(indice_worst_client)
        nbIteration += 1


def destroy_related_client_by_distance(solution, degres_destruction):
    """
    Named 'related removal' in the report but with alpha = 1, beta = 0, gamma = 0.

    FR :
    mesure de la relativite entre clients qui correspond aux distances/temps pour l'instant.
    On choisit à chaque étape un client et on enlève son plus proche voisin.

    EN :
    measure of relativity between customers in terms of distance between customers
    At each step, we choose a client and remove its nearest neighbor.
    """
    # Destruction aleatoire du premier client
    if len(solution.listTimeSlot) > 1:
        timeSlot = solution.listTimeSlot[random.randint(0, len(solution.listTimeSlot) - 1)]
    else:
        timeSlot = solution.listTimeSlot[0]

    if len(timeSlot.listRoute) > 1:
        route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
        while len(route.trajet) < 3:
            route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
    else:
        route = timeSlot.listRoute[0]

    if len(route.trajet) >= 3:
        # Destruction du client
        position = random.randint(1, len(route.trajet) - 2)
        route.totalQuantity -= route.trajet[position].getQuantity()
        first_client = route.trajet.pop(position)

    removed_clients = [first_client.indice]

    nbIteration = 0
    nbClientToDestroy = degres_destruction

    liste = [p.indice for p in solution.instance.listClient]
    liste.remove(0)

    while nbIteration < nbClientToDestroy - 1:
        choosed_client = random.choices(removed_clients)[0]
        client_plus_proche = 0
        temps_min = 100
        for i in liste:  # taille de la matrice des distances
            if i not in removed_clients:
                if solution.instance.getDistance(choosed_client, i) < temps_min:
                    temps_min = solution.instance.getDistance(choosed_client, i)
                    client_plus_proche = i
        removed_clients.append(client_plus_proche)
        for T in solution.listTimeSlot:
            for R in T.listRoute:
                for C in R.trajet:
                    if C.indice == client_plus_proche:
                        R.totalQuantity -= C.getQuantity()
                        R.trajet.remove(C)
        nbIteration += 1


def destroy_related_clients(solution, degres_destruction, alpha, beta, gamma):
    """
    Named 'related removal' in the report but with alpha < 1, beta != 0, gamma != 0.

    FR :
    mesure de la relativite entre clients qui correspond a une ponderation entre distance, ratio et request

    EN :
    measure of relativity between clients that corresponds to a weighting between distance, ratio and request
    """
    # Destruction aleatoire du premier client
    if len(solution.listTimeSlot) > 1:
        timeSlot = solution.listTimeSlot[random.randint(0, len(solution.listTimeSlot) - 1)]
    else:
        timeSlot = solution.listTimeSlot[0]

    if len(timeSlot.listRoute) > 1:
        route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
        while len(route.trajet) < 3:
            route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]
    else:
        route = timeSlot.listRoute[0]

    if len(route.trajet) >= 3:
        # Destruction du client
        position = random.randint(1, len(route.trajet) - 2)
        route.totalQuantity -= route.trajet[position].getQuantity()
        first_client = route.trajet.pop(position)

    removed_clients = [first_client]
    nbIteration = 0
    nbClientToDestroy = degres_destruction

    liste = [p for p in solution.instance.listClient]
    liste.pop(0)

    while nbIteration < nbClientToDestroy - 1:
        choosed_client = random.choices(removed_clients)[0]
        client_plus_proche = 0
        Related_min = 200
        for i in liste:  # taille de la matrice des distances
            if i not in removed_clients:
                Related = alpha * solution.instance.getDistance(choosed_client.indice, i.indice) + beta * abs(
                    int(choosed_client.request) - int(i.request)) + gamma * abs(
                    (choosed_client.getQuantity() / choosed_client.getCapacity()) - (i.getQuantity() / i.getCapacity()))
                if Related < Related_min:
                    Related_min = Related
                    client_plus_proche = i
        removed_clients.append(client_plus_proche)

        for T in solution.listTimeSlot:
            for R in T.listRoute:
                for C in R.trajet:
                    if C.indice == client_plus_proche.indice:
                        R.totalQuantity -= C.getQuantity()
                        R.trajet.remove(C)
        nbIteration += 1


def destroy_route(solution, depot):
    """
    Named 'destroyroute' in the report

    FR :
    Detruit une route aleatoire dans la solution. Le nb de clients detruits ne depend pas du degrès de destruction
    mais du nombre de clients de la route detruite.

    EN :
    Destroys a random route in the solution. The number of customers destroyed does not depend on the degree of
    destruction but on the number of customers on the destroyed route.
    """
    timeSlot = solution.listTimeSlot[random.randint(0, len(solution.listTimeSlot) - 1)]
    route = timeSlot.listRoute[random.randint(0, len(timeSlot.listRoute) - 1)]

    route.trajet = []
    route.appendClient(depot)
    route.appendClient(depot)
    route.totalQuantity = 0
    route.duration = 0
