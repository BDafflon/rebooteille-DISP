"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
from instance.TimeSlot import TimeSlot
from instance.Route import Route
from solution.Solution import Solution
import alns.methods as methods
import alns.destroyMethods as destroyMethods
import alns.repairsMethods as repairsMethods

import time
import random
import copy
import math


class ALNS:

    def __init__(self, instance):
        # Initialisation de l'instance
        self.instance = instance
        self.nIter = (len(instance.listClient) - 1) / 2 * 1000

        # Initialisation des solutions utilisées
        self.bestSolution = Solution(self.instance)
        self.currentSolution = Solution(self.instance)
        self.keptinmemory = Solution(self.instance)
        self.testSolution = Solution(self.instance)

        # fréquence d'affichage des logs de recherche
        self.displayFrequency = 500

        # nombre de fois où on accepte une solution moins bonne
        self.onremontelapente = 0

        # nombre de fois où les repair ne marchent pas et on repart de la solution gardée en mémoire
        self.repairdontwork = {}

        # Listes des noms des méthodes de destruction
        # "destroy_route",
        # "destroy_random",
        # "destroy_worst_clients",
        # "destroy_related_clients",
        # "destroy_related_client_by_distance",
        # "destroy_Client_with_a_request_placed_at_the_end_of_the_solution",
        # "destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution"
        self.destroy_methods = ["destroy_route",
                                "destroy_random",
                                "destroy_worst_clients",
                                "destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution",
                                "destroy_Client_with_a_request_placed_at_the_end_of_the_solution"]

        # Listes des noms des méthodes de repair
        # "repair_randomV2",
        # "repair_randomv1",
        # "repair_2_regret",
        # "repair_random_best_insertion",
        # "repair_max_ratio_best_insertion",
        # "repair_FirstPositionAvailable_randomlistClient",
        # "repair_FirstPositionAvailable_maxratio_listClient"
        self.repair_methods = ["repair_2_regret",
                               "repair_randomv1",
                               "repair_random_best_insertion",
                               "repair_max_ratio_best_insertion",
                               "repair_FirstPositionAvailable_maxratio_listClient"]

        self.repairdontwork = {}
        self.weights_destroy = {}
        self.weights_repair = {}
        self.USED_METHODS = {}
        self.USED_METHODS_UNTIL_LAST_BEST = {}
        self.sucess_swap = {}
        self.evolution_iter_best = None
        self.evolution_time_best = None
        self.evolution_cost = None

    def createSolution(self):
        """
        FR :
        Méthode de création d'une solution basique
        Ajout de client dans une route dans leur ordre de parsing jusqu'à atteindre
        soit la capacité max du véhicule soit la durée max du time slot
        Une fois la capacité atteinte on essaie d'ajouter une autre route au time slot
        Sinon on crée un autre time slot

        EN :
        Method of creating a basic solution
        Adding clients in a route in their parsing order until reaching either the max capacity of the vehicle
        or the maximum duration of the time slot
        Once the capacity is reached, we try to add another route to the time slot
        Otherwise we create another time slot
        """
        # Initialisation des variables
        listClient = methods.order_ListClient_random(self.instance.listClient.copy())
        clientNotPlaced = True

        # Réinitialisation de la currentSolution
        self.currentSolution = Solution(self.instance)

        while clientNotPlaced and len(self.currentSolution.listTimeSlot) < self.instance.numberTimeSlotMax:
            # Si tous les clients sont placés alors on met fin à la boucle
            clientNotPlaced = False

            # Création du timeSlot
            timeSlot = TimeSlot()

            # Boolean pour mettre fin à la boucle si aucun client ne peut être ajouté sans violer la contrainte de durée
            noMoreClientForDuration = False

            # Déclaration que le dépôt est visité
            listClient[0].setVisited()

            # Tant que la durée du time slot n'est pas dépassée et que le nombre de routes est inférieur à la limite
            while (timeSlot.getDuration(self.instance.getDistance) <= self.instance.durationTimeSlotMax
                   and len(timeSlot.listRoute) < self.instance.routePerTimeSlotMax
                   and not noMoreClientForDuration):

                # Variable pour vérifier si un client a été ajouté sur l'itération de durée
                clientHasBeenPlacedForDuration = False

                # Variable pour vérifier si aucun client ne peut être ajouté sans violer la contrainte de capacité
                noMoreClientForCapacity = False

                # Création de la route
                route = Route(self.instance.listVehicle[0])
                routeAddedToTimeSlot = False

                # Ajout du dépôt de départ et d'arrivée
                route.appendClient(self.instance.listClient[0])
                route.appendClient(self.instance.listClient[0])

                # Tant que la capacité du véhicule n'est pas atteinte
                while route.getTotalQuantity() <= route.vehicle.getCapacity() and not noMoreClientForCapacity:

                    # Variable pour vérifier si un client a été ajouté sur l'itération de capacité
                    clientHasBeenPlacedForCapacity = False

                    # Boucle sur les clients de l'instance
                    for client in listClient:
                        # S'il est non visité on l'ajoute
                        if not client.isVisited() and client.getIndice() != 0:
                            route.insertClient(len(route.getTrajet()) - 1, client)

                            if not routeAddedToTimeSlot:
                                routeAddedToTimeSlot = True
                                # Ajout de la route au timeSlot en cours
                                timeSlot.addToListRoute(route)

                            # Vérification des contraintes de durée du time slot et de capacité du véhicule
                            if (timeSlot.getDuration(self.instance.getDistance) <= self.instance.durationTimeSlotMax
                                    and route.getTotalQuantity() <= route.vehicle.getCapacity()):

                                # Si oui alors on valide l'ajout
                                client.setVisited()
                                clientHasBeenPlacedForCapacity = True
                                clientHasBeenPlacedForDuration = True

                            else:
                                # Sinon, on supprime l'ajout
                                route.trajet.pop(len(route.getTrajet()) - 2)

                                # Si la route ne contient plus que le dépôt alors on la supprime
                                if route.getTrajet()[1].getIndice() == 0:
                                    timeSlot.removeFromListRoute(route)
                                    routeAddedToTimeSlot = False

                    # Mise à jour de la variable de fin de boucle while pour la capacité
                    noMoreClientForCapacity = not clientHasBeenPlacedForCapacity

                # Mise à jour de la variable de fin de boucle while pour la durée
                noMoreClientForDuration = not clientHasBeenPlacedForDuration

            # Ajout du timeSlot à la solution en cours
            self.currentSolution.addToListTimeSlot(timeSlot)

            # Vérification que tous les clients ont été visités
            for client in self.instance.listClient:
                if not client.isVisited():
                    clientNotPlaced = True
                    break

        # Réinitialisation des visites des clients
        for client in self.instance.listClient:
            client.setNotVisited()

        if not self.currentSolution.checkSolution():
            # Création d'une nouvelle solution de départ
            self.createSolution()

    def acceptance_criteria_greedy(self):
        """
        FR:
        Retourne True si on accepte la solution et False sinon.

        EN :
        Returns True if the solution is accepted and False otherwise.
        """
        return self.currentSolution.getCost() < self.testSolution.getCost()

    def acceptance_criteria_simulated_annealing(self, T0, alpha, step):
        """
        FR:
        Retourne True si on accepte la solution et False sinon. On a la possibilité ici d'accepter une solution moins bonne avec une probabilité p

        EN :
        Returns True if the solution is accepted and False otherwise. We have the possibility here to accept a worst solution with probability p
        """
        self.currentSolution.calculateCost()
        self.testSolution.calculateCost()
        delta = self.currentSolution.getCost() - self.testSolution.getCost()
        if delta <= 0:
            return True
        else:
            r = random.random()
            cst = T0 * (alpha ** step)
            if cst != 0:
                p = math.exp(- (delta / cst))
            else:
                p = 1.1
            # print(delta,T0,alpha,step)
            if r < p:
                self.onremontelapente += 1
                return True
            else:
                return False

    def modification(self, solution, destroy_method, degree_destruction, repair_method, alpha, beta, gamma):
        """
        FR:
        Fonction prenant la solution courante et la transforme suivant la méthode de destruction et la méthode
        de repair choisies. Cette fonction modifie current_solution. La nouvelle solution est dans current_solution.

        EN :
        Function taking the current solution and transforming it according to the chosen destruction method and
        repair method. This function modifies current_solution. The new solution is in current_solution.
        """
        if destroy_method == "destroy_worst_clients":
            destroyMethods.destroy_worst_clients(solution, degree_destruction)
        if destroy_method == "destroy_random":
            destroyMethods.destroy_random(solution, degree_destruction)
        if destroy_method == "destroy_related_client_by_distance":
            destroyMethods.destroy_related_client_by_distance(solution, degree_destruction)
        if destroy_method == "destroy_related_clients":
            destroyMethods.destroy_related_clients(solution, degree_destruction, alpha, beta, gamma)
        if destroy_method == "destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution":
            destroyMethods.destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution(solution,
                                                                                              degree_destruction)
        if destroy_method == "destroy_Client_with_a_request_placed_at_the_end_of_the_solution":
            destroyMethods.destroy_Client_with_a_request_placed_at_the_end_of_the_solution(solution, degree_destruction,
                                                                                           self.instance.listClient)
        if destroy_method == "destroy_route":
            destroyMethods.destroy_route(solution, self.instance.listClient[0])

        if repair_method == "repair_2_regret":
            repairsMethods.repair_2_regret(solution, self.keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_max_ratio_best_insertion":
            repairsMethods.repair_max_ratio_best_insertion(solution, self.keptinmemory, self.instance,
                                                           self.repairdontwork)
        if repair_method == "repair_FirstPositionAvailable_randomlistClient":
            repairsMethods.repair_FirstPositionAvailable_randomlistClient(solution, self.keptinmemory, self.instance,
                                                                          self.repairdontwork)
        if repair_method == "repair_randomv1":
            repairsMethods.repair_randomv1(solution, self.keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_randomV2":
            repairsMethods.repair_randomV2(solution, self.keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_FirstPositionAvailable_maxratio_listClient":
            repairsMethods.repair_FirstPositionAvailable_maxratio_listClient(solution, self.keptinmemory, self.instance,
                                                                             self.repairdontwork)
        if repair_method == "repair_random_best_insertion":
            repairsMethods.repair_random_best_insertion(solution, self.keptinmemory, self.instance, self.repairdontwork)

    def solve(self, PU, rho, sigma1, sigma2, sigma3, tolerance, C, alpha, beta, gamma, Nc, theta=0.5, Ns=10,
              withSwap=False, showLog=False):
        """
        FR:
        Fonction principale. Les différentes parties sont représentées dans le logigramme ou le pseudo code du rapport.
        Cette fonction a en argument tous les paramètres de l'algorithme et retourne la meilleure solution.
        currentSolution correspond à la solution que l'on modifie à chaque iteration.
        testSolution correspond à la solution gardée en mémoire à laquelle on va comparer current solution.

        EN :
        Main function.The different parts are represented in the flowchart or the pseudo code of the report.
        This function has as argument all the parameters of the algorithm and returns the best solution.
        currentSolution corresponds to the solution that we modify at each iteration.
        testSolution corresponds to the solution kept in memory to which we will compare current solution.
        """
        print("Solving " + self.instance.getName())
        # INITIALISATION DU TEMPS
        initialTime = time.perf_counter()

        # INITIALISATION DES SOLUTIONS
        self.createSolution()
        self.bestSolution.copy(self.currentSolution)
        self.testSolution.copy(self.currentSolution)

        # INITIALISATION DES VARIABLES
        T0 = (tolerance * self.currentSolution.getCost()) / math.log(2)  # temperature initiale
        nbIteration = 0  # nombre d'itérations
        iterationMaxSinceLastBest = Nc  # nombre d'itérations maximum avant de réinitialiser la solution
        nbIterationSinceLastBest = 0  # nombre d'itérations avant de réinitialiser la solution
        self.onremontelapente = 0  # nombre de fois que l'on accepte une solution moins bonne
        self.evolution_iter_best = [nbIteration]  # iterations où on améliore la meilleure solution
        self.evolution_time_best = [nbIteration]  # temps où on améliore la meilleure solution
        self.bestSolution.calculateCost()
        self.evolution_cost = [round(self.bestSolution.getCost(), 2)]  # évolution du cout de la meilleure solution

        self.repairdontwork = {i: 0 for i in self.repair_methods}

        # INITIALISATION DES POIDS POUR LA "ROULETTE WHEEL SELECTION"
        # initialement même poids pour toutes les méthodes
        self.weights_destroy = {i: 1 / len(self.destroy_methods) for i in self.destroy_methods}
        self.weights_repair = {i: 1 / len(self.repair_methods) for i in self.repair_methods}

        Success_destroy = {i: 0 for i in self.destroy_methods}
        Used_destroy_methods = {i: 0 for i in self.destroy_methods}

        Success_repair = {i: 0 for i in self.repair_methods}
        Used_repair_methods = {i: 0 for i in self.repair_methods}

        # dictionnaires avec pour clé le nom de la methode et
        # pour valeur le nombre de fois que l'on utilise une methode en s'arrêtant à la dernière meilleure solution
        self.USED_METHODS = {i: 0 for i in self.destroy_methods + self.repair_methods}
        self.USED_METHODS_UNTIL_LAST_BEST = {}

        self.sucess_swap = {'swap_inter_route': 0, 'swap_intra_route': 0}

        # Headers de l'affichage de recherche de solution
        if showLog:
            print("Nb iteration", "Clock", "Best solution", "Nb de solutions moins bonnes acceptées", sep='\t')

        # CRITÈRE D'ARRÊT : nIter iterations maximum :
        while nbIteration < self.nIter:
            # VÉRIFICATION DE L'AMÉLIORATION DE LA SOLUTION
            if nbIterationSinceLastBest >= iterationMaxSinceLastBest:
                # Si on n'améliore pas la best solution, alors on recommence en cherchant avec
                # une nouvelle solution de départ en mélangeant la liste de création de la solution

                # Réinitialisation du compteur
                nbIterationSinceLastBest = 0

                # Création d'une nouvelle solution de départ
                self.createSolution()

                # Mise à jour de la solution de test
                if self.currentSolution.checkSolution():
                    self.testSolution.copy(self.currentSolution)

            # CHOIX D'UN OPÉRATEUR DE DESTRUCTION
            # Degré de destruction faible pour détruire peu → améliore le temps de calcul
            degree_destruction = random.randint(math.ceil(0.1 * len(self.instance.listClient)),
                                                math.ceil(0.2 * len(self.instance.listClient)))
            # Degré de destruction fort pour détruire plus de clients
            # → allonge le temps de calcul mais diversifie les solutions
            # degree_destruction = random.randint(math.ceil(0.1*len(self.instance.listClient)),
            #                                     math.ceil(0.4*len(self.instance.listClient)))

            destroy_method = methods.choose_destroy_method(self.destroy_methods, self.weights_destroy)

            Used_destroy_methods[destroy_method] += 1
            self.USED_METHODS[destroy_method] += 1

            # CHOIX D'UN OPÉRATEUR DE RECONSTRUCTION
            repair_method = methods.choose_repair_method(self.repair_methods, self.weights_repair)

            Used_repair_methods[repair_method] += 1
            self.USED_METHODS[repair_method] += 1

            # MODIFICATION DE LA SOLUTION
            # on sauvegarde en memoire la solution courante pour pouvoir repartir de cette solution
            self.keptinmemory.copy(self.currentSolution)
            # on sauvegarde en memoire la meilleure solution courante pour pouvoir repartir de cette solution
            # self.keptinmemory.copy(self.bestSolution)

            self.modification(self.currentSolution, destroy_method, degree_destruction, repair_method,
                              alpha, beta, gamma)

            if not self.currentSolution.checkSolution():
                self.currentSolution.copy(self.keptinmemory)
            else:
                self.keptinmemory.copy(self.currentSolution)

            # ATTEINT-ON LA CONDITION POUR FAIRE LES SWAPS ?
            if withSwap and self.currentSolution.getCost() < (1 + theta) * self.testSolution.getCost():
                # ON REALISE Ns SWAPS DE CHAQUE TYPE : 'swap_inter_route' & 'swap_intra_route'
                for k in range(Ns):
                    # SWAP de deux clients au sein d'une route
                    methods.swap_inter_route(self.currentSolution)

                    # si le swap améliore la solution, on la garde en memoire
                    if self.currentSolution.getCost() < self.keptinmemory.getCost():
                        self.keptinmemory.copy(self.currentSolution)
                        self.sucess_swap['swap_inter_route'] += 1

                    # SWAP de deux clients au hasard dans la solution
                    methods.swap_intra_route(self.currentSolution)

                    # si le swap détériore la solution, on repart de celle juste avant
                    if self.currentSolution.getCost() > self.keptinmemory.getCost():
                        self.currentSolution.copy(self.keptinmemory)
                    # si le swap améliore la solution, on la garde en memoire
                    else:
                        self.keptinmemory.copy(self.currentSolution)
                        self.sucess_swap['swap_intra_route'] += 1

            self.currentSolution.calculateCost()
            self.keptinmemory.calculateCost()

            # VERIFICATION DE LA SOLUTION (CONTRAINTES)
            if not self.currentSolution.checkSolution():
                self.currentSolution.copy(self.keptinmemory)

            # CRITÈRE D'ACCEPTATION
            # self.acceptance_criteria_simulated_annealing(T0,alpha,nbIteration)
            # self.acceptance_criteria_greedy()

            if self.acceptance_criteria_simulated_annealing(T0, C, nbIteration):

                if self.currentSolution.getCost() < self.bestSolution.getCost():
                    # si on a une meilleure solution, on met à jour testSolution et bestSolution
                    # et on récompense les méthodes qui ont réussi par la quantité sigma1
                    self.testSolution.copy(self.currentSolution)
                    self.bestSolution.copy(self.currentSolution)

                    Success_destroy[destroy_method] += sigma1
                    Success_repair[repair_method] += sigma1

                    # mise à jour des variables d'informations
                    self.evolution_cost.append(round(self.bestSolution.calculateCost(), 2))
                    currentTime = round(time.perf_counter() - initialTime, 3)
                    self.bestSolution.setTime(currentTime)
                    self.evolution_time_best.append(currentTime)
                    self.USED_METHODS_UNTIL_LAST_BEST = copy.deepcopy(self.USED_METHODS)
                    nbIterationSinceLastBest = 0
                    self.evolution_iter_best.append(nbIteration + 1)

                elif self.currentSolution.getCost() <= self.testSolution.getCost():
                    # si la solution courante améliore celle gardée en mémoire, on la met à jour
                    # et on récompense les méthodes qui ont réussi par la quantité sigma2
                    self.testSolution.copy(self.currentSolution)

                    Success_destroy[destroy_method] += sigma2
                    Success_repair[repair_method] += sigma2

                else:
                    # si la solution n'est pas améliorante, mais qu'elle est acceptée par le critère d'acceptance
                    # on met à jour la solution en mémoire et on récompense les méthodes par la quantité sigma3
                    self.testSolution.copy(self.currentSolution)

                    Success_destroy[destroy_method] += sigma3
                    Success_repair[repair_method] += sigma3

            # mise à jour du nombre d'itérations
            nbIteration += 1
            nbIterationSinceLastBest += 1

            # Si on a atteint Pu itérations → changements des probabilités associées à chaque méthode
            if nbIteration % PU == 0:
                self.weights_destroy, self.weights_repair = methods.update_weights(rho, self.weights_destroy,
                                                                                   self.weights_repair, Success_destroy,
                                                                                   Success_repair, Used_destroy_methods,
                                                                                   Used_repair_methods)

                Success_destroy = {i: 0 for i in self.destroy_methods}
                Success_repair = {i: 0 for i in self.repair_methods}

                Used_destroy_methods = {i: 0 for i in self.destroy_methods}
                Used_repair_methods = {i: 0 for i in self.repair_methods}

            if showLog and nbIteration % self.displayFrequency == 0:
                print("{nIter}\t\t{time}\t{cost}\t\t{nbr}".format(nIter=nbIteration,
                                                                  time=round(time.perf_counter() - initialTime, 2),
                                                                  cost=round(self.bestSolution.getCost(), 2),
                                                                  nbr=self.onremontelapente))
                self.onremontelapente = 0

        return self.bestSolution

    def display(self):
        print("## Nombre de fois ou les repair ne marchent pas et on repart de la solution gardée en memoire :")
        print(self.repairdontwork)
        print("## Iterations où on améliore la meilleure solution :")
        print(self.evolution_iter_best)
        print("## Temps où on améliore la meilleure solution :")
        print(self.evolution_time_best)
        print("## Evolution du cout de la meilleure solution :")
        print(self.evolution_cost)
        print("## Utilisation des méthodes jusqu'a la dernière meilleure solution :")
        print(self.USED_METHODS_UNTIL_LAST_BEST)
        print("## Utilisation des méthodes :")
        print(self.USED_METHODS)
        print("## Poids des méthodes de destructions :")
        print(self.weights_destroy)
        print("## Poids des méthodes de repair :")
        print(self.weights_repair)
        print("## Succès des swaps")
        print(self.sucess_swap)
        print("### BEST SOLUTION :")
        self.bestSolution.display()
