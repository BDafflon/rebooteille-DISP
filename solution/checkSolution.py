def check(solution, showLog=False, notSommetVisited=False):
    # Calcul du coût de la solution
    solution.calculateCost()

    # Méthode permettant de vérifier que l'on satisfait toutes les contraintes du problème
    '''Contrainte du nombre de time slot utilisés'''
    if len(solution.listTimeSlot) > solution.instance.numberTimeSlotMax:
        if showLog:
            print("Solution non valide - Nombre de time slots")
        return False

    for timeSlot in solution.listTimeSlot:
        # Si le time slot ne contient pas de routes
        if len(timeSlot.listRoute) == 0:
            # On peut le supprimer
            solution.removeFromListTimeSlot(timeSlot)
            # On lance un check de la solution modifiée
            return solution.checkSolution()

        '''Contrainte du nombre de routes par time slot'''
        if len(timeSlot.listRoute) > solution.instance.routePerTimeSlotMax:
            if showLog:
                print("Solution non valide - Nombre de routes par time slot")
            return False

        for route in timeSlot.getListRoute():
            # Si la route courante n'a que 2 clients alors elle ne passe par aucun point de collecte
            # Elle fait 0 → 0
            if len(route.trajet) <= 2:
                # On peut donc la supprimer
                timeSlot.removeFromListRoute(route)
                # On lance un check de la solution modifiée
                return solution.checkSolution()

            '''Contrainte de démarrer du dépôt'''
            if route.getTrajet()[0].getIndice() != 0:
                if showLog:
                    print("Solution non valide - Début d'une route sans dépôt")
                return False

            '''Contrainte de capacité du véhicule'''
            if route.getTotalQuantity() > route.vehicle.getCapacity():
                if showLog:
                    print("Solution non valide - Capacité max du véhicule")
                return False

            '''Contrainte de finir par le dépôt'''
            if route.getTrajet()[-1].getIndice() != 0:
                if showLog:
                    print("Solution non valide - Fin d'une route sans dépôt")
                return False

            '''Contrainte des horaires'''
            """vehicle = route.vehicle
            previousClient = route.getTrajet()[0]
            firstStart = [previousClient.morningOpening]
            lastStart = [previousClient.morningClosing]
            for i in range(1, len(route.getTrajet())):
                client = route.getTrajet()[i]
                departTime = firstStart[i-1]
                if previousClient.getIndice() != 0:
                    departTime += vehicle.getFixedCollectionTime()
                    departTime += vehicle.getCollectionTimePerCrate() * previousClient.getQuantity()
                arrivalTime = departTime + solution.instance.getDistance(previousClient.getIndice(), client.getIndice())
                firstStart.append(max(arrivalTime, client.morningOpening))
                print(firstStart[i])
                previousClient = client
            """
            # Sauf si on spécifie de ne pas vérifier les sommets visités pour les opérateurs de réparation
            if not notSommetVisited:
                # Validation du passage par le sommet
                if len(route.getTrajet()) > 1:
                    for client in route.getTrajet():
                        client.setVisited()

        '''Contrainte de durée du time slot'''
        durationTimeSlot = timeSlot.getDuration(solution.instance.getDistance)
        if durationTimeSlot > solution.instance.durationTimeSlotMax:
            if showLog:
                print("Solution non valide - Durée du time slot dépassée {v} > {u}"
                      .format(v=durationTimeSlot, u=solution.instance.durationTimeSlotMax))
            return False

    # Sauf si on spécifie de ne pas vérifier les sommets visités pour les opérateurs de réparation
    if not notSommetVisited:
        '''Contrainte de visite de tous les sommets'''
        for client in solution.instance.listClient:
            if not client.isVisited():
                if showLog:
                    print("Solution non valide - Client {i} non visité".format(i=client.getIndice()))

                # Réinitialisation complète de la liste avant de retourner False
                for clientVisited in solution.instance.listClient:
                    clientVisited.setNotVisited()
                return False
            else:
                # S'il a bien été visité on le réinitialise
                client.setNotVisited()
    return True
