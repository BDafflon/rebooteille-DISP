
def check(solution, showLog = True, notSommetVisited = False):
    #Calcul du coût de la solution
    solution.calculateCost()

    #Méthode permettant de vérifier que l'on satisfait toutes les contraintes du problème
    '''Contrainte du nombre de time slot utilisés'''
    if(len(solution.listTimeSlot) > solution.instance.numberTimeSlotMax):
        if(showLog):
            print("Solution incompatible - Nombre de time slots")
            return False

    durationTimeSlot = 0
    for timeSlot in solution.listTimeSlot:
        #Si le time slot ne contient pas de routes
        if(len(timeSlot.listRoute) == 0):
            #Alors on peut le supprimer
            solution.removeFromListTimeSlot(timeSlot)
            #On relance un check de la solution
            return solution.checkSolution()

        #Calcul de la durée du time slot
        durationTimeSlot = timeSlot.getDuration(solution.instance.getDistance)

        '''Contrainte du nombre de routes par time slot'''
        if(len(timeSlot.listRoute) > solution.instance.routePerTimeSlotMax):
            if(showLog):
                print("Solution incompatible - Nombre de routes par time slot")
            return False

        for route in timeSlot.getListRoute():
            #Si la route courante n'a que 2 clients alors elle ne passe par aucun sommet
            #Elle fait 0 => 0
            if(len(route.trajet) == 2):
                #On peut donc la supprimer
                timeSlot.removeFromListRoute(route)
                #On relance le check de la solution
                return solution.checkSolution()

            '''Contrainte de capacité du véhicule'''
            if(route.getTotalQuantity() > route.vehicle.getCapacity()):
                #print(route.getTotalQuantity())
                #print(route.vehicle.getCapacity())
                if(showLog):
                    print("Solution incompatible - Capacité max du véhicule")
                return False

            '''Contrainte de démarrer du dépôt'''
            if(route.getTrajet()[0].getIndice() != 0):
                if(showLog):
                    print("Solution incompatible - Début d'une route sans dépôt")
                return False

            '''Contrainte de finir par le dépôt'''
            if(route.getTrajet()[len(route.getTrajet()) - 1].getIndice() != 0):
                if(showLog):
                    print("Solution incompatible - Fin d'une route sans dépôt")
                return False

            #Sauf si on spécifie de ne pas vérifier les sommets visités
            #Utiliser dans les opérateurs de réparation
            if(not notSommetVisited):
                #Validation du passage par le sommet
                if (len(route.getTrajet()) > 1):
                    for i in range(0, len(route.getTrajet()) - 1):
                        clientDepart = route.getClientFromIndice(i)
                        clientArrivee = route.getClientFromIndice(i+1)

                        #Mise à jour pour assurer que les sommets sont visités
                        clientDepart.setVisited()
                        clientArrivee.setVisited()

        '''Contrainte de durée du time slot'''
        if (durationTimeSlot > solution.instance.durationTimeSlotMax):

            if(showLog):
                print("Solution incompatible - Durée du time slot " + str(timeSlot.getIndice()) + " dépassée")
            return False

    #Si on spécifie de ne pas vérifier les sommets visités
    #Utilisé dans les opérateurs de réparation
    if (not notSommetVisited):
        '''Contrainte de visite de tous les sommets'''
        for client in solution.instance.listClient:
            if (not client.isVisited()):
                if(showLog):
                    print("Solution incompatible - Client " + str(client.getIndice()) + " non visité ")

                # Réinitialisation complète de la liste avant de return False
                for clientVisited in solution.instance.listClient:
                    clientVisited.setnotVisited()

                return False
            else:
                #S'il a bien été visité on le réinitialise
                client.setnotVisited()
    return True
