"""
Source from project ALNS 2022, ALEXI OMAR DJAMA
"""
from Instance import Instance
from Route import Route
from TimeSlot import TimeSlot
from Solution import Solution
from datetime import datetime
from Client import Client
import methods
import destroyMethods
import repairsMethods

import time
import random
import pandas as pd
import copy
import math

class ALNS :

    def __init__(self, instance, dureeMax = None) :
        #Initialisation de l'instance
        self.instance = instance

        #Initialisation des solutions utilisées
        self.bestSolution = Solution(self.instance)
        self.currentSolution = Solution(self.instance)
        self.keptinmemory = Solution(self.instance)
        self.testSolution = Solution(self.instance)

        #Fréquence d'affichage des logs de recherche
        self.frequenceAffichage = 500

        #nombre de fois où on accepte une solution moins bonne
        self.onremontelapente = 0

        #nombre de fois où les repair marchent pas et on repart de la solution gardee en memoire
        self.repairdontwork = {}



    def createSolution(self, listClient):
        '''
        FR :
        Méthode de création d'une solution basique
        Ajout de client dans une route dans leur ordre de parsing jusqu'à atteindre soit la capacité max du véhicule
        Soit la durée max du time slot
        Une fois la capacité atteinte on essaie d'ajouter une autre route au time slot
        Sinon on crée un autre time slot

        EN :
        Method of creating a basic solution
        Adding clients in a route in their parsing order until reaching either the max capacity of the vehicle
        or the maximum duration of the time slot
        Once the capacity is reached, we try to add another route to the time slot
        Otherwise we create another time slot
        '''
        #Initialisation des variables
        allClientHasBeenPlaced = False
        clientNotPlaced = False

        #Réinitialisation de la currentSolution
        self.currentSolution = Solution(self.instance)

        while(not allClientHasBeenPlaced and len(self.currentSolution.listTimeSlot) < self.instance.numberTimeSlotMax):
            #Création du timeSlot
            timeSlot = TimeSlot()

            #Variable pour terminer la boucle si aucune nouvelle client ne peut-être ajoutée pour satisfaire la contrainte de durée
            noMoreClientForDuration = False

            #Déclaration que le dépôt est visité
            listClient[0].setVisited()

            #Tant que la durée du time slot n'est pas dépassée et que le nombre de routes est inférieur à la limite
            while(timeSlot.getDuration(
                    self.instance.timeTravel,
                    self.instance.fixedCollectionTime,
                    self.instance.collectionTimePerCrate) <= self.instance.durationTimeSlotMax
                    and len(timeSlot.listRoute) < self.instance.routePerTimeSlotMax
                    and not noMoreClientForDuration):

                #Variable pour vérifier si une client a été ajoutée sur l'itération de durée
                clientHasBeenPlacedForDuration = False

                #Variable pour terminer la boucle si aucune nouvelle client ne peut être ajoutée pour
                #satisfaire la contrainte de durée
                noMoreClientForCapacity = False

                #Création de la route
                route = Route()
                routeAddedToTimeSlot = False

                #Ajout du dépôt de départ et d'arrivée
                route.appendClient(self.instance.listClient[0])
                route.appendClient(self.instance.listClient[0])

                #Tant que de la capacité est disponible sur le véhicule
                while(route.getTotalFillingRate() <= self.instance.vehiculeCapacityMax
                      and not noMoreClientForCapacity):

                    #Variable pour vérifier si une client a été ajoutée sur l'itération de capacité
                    clientHasBeenPlacedForCapacity = False

                    #Boucle sur les clients de l'instance
                    for client in listClient:
                        #Si elle est non visité on l'ajoute
                        if (client.isVisited() == False and client.getIndice() != 0):
                            route.insertClient(len(route.getTrajet()) - 1, client)

                            if(not routeAddedToTimeSlot):
                                    routeAddedToTimeSlot = True
                                    #Ajout de la route au timeSlot en cours
                                    timeSlot.addToListRoute(route)

                            #Test si l'ajout respecte les contraintes de durée du time slot et de capacité
                            #du véhicule pour cette route
                            if(timeSlot.getDuration(
                                    self.instance.timeTravel,
                                    self.instance.fixedCollectionTime,
                                    self.instance.collectionTimePerCrate) <= self.instance.durationTimeSlotMax
                               and route.getTotalFillingRate() <= self.instance.vehiculeCapacityMax):

                                #Si oui alors on valide l'ajout
                                client.setVisited()
                                clientHasBeenPlacedForCapacity = True
                                clientHasBeenPlacedForDuration = True

                            else:
                                #Sinon, on supprime l'ajout
                                route.trajet.pop(len(route.getTrajet()) - 2)

                                #Si on supprime le client et que la route ne contient plus que les dépôts
                                #alors on supprime la route du time slot
                                if(route.getTrajet()[1].getIndice() == 0):
                                    timeSlot.removeFromListRoute(route)
                                    routeAddedToTimeSlot = False

                    #Mise à jour de la variable de fin de boucle while pour la capacité
                    if(not clientHasBeenPlacedForCapacity):
                        noMoreClientForCapacity = True

                #Mise à jour de la variable de fin de boucle while pour la durée
                if(not clientHasBeenPlacedForDuration):
                    noMoreClientForDuration = True

            #Ajout du timeSlot à la solution en cours
            self.currentSolution.addToListTimeSlot(timeSlot)

            #Vérification de toutes les clients pour s'assurer qu'ils ont été visité
            for client in self.instance.listClient:
                if(not client.isVisited()):
                    clientNotPlaced = True
                    break

            #Si un client n'a pas été placé alors on reboucle
            if(clientNotPlaced):
                clientNotPlaced = False
            else:
                allClientHasBeenPlaced = True

        #Réinitialisation des visites des clients
        for client in self.instance.listClient:
            client.setnotVisited()

        if(not self.currentSolution.checkSolution()):
            #Shuffle de la liste sans le dépôt de départ et d'arrivée
            listClientSansDepot = listClient[1:]
            listClientSansDepot = methods.order_ListClient_random(listClientSansDepot)

            #Réassignation de la liste avec le dépôt a la première place
            listClient = [listClient[0]] + listClientSansDepot

            #Création d'une nouvelle solution de départ
            self.createSolution(listClient)



    def acceptance_criteria_greedy(self) :
        """
        FR:
        Retourne True si on accepte la solution et False sinon.

        EN :
        Returns True if the solution is accepted and False otherwise.
        """
        return self.currentSolution.cost < self.testSolution.cost



    def acceptance_criteria_simulated_annealing(self,T0,alpha,step) :
        """
        FR:
        Retourne True si on accepte la solution et False sinon. On a la possibilité ici d'accepter une solution moins bonne avec une probabilité p

        EN :
        Returns True if the solution is accepted and False otherwise. We have the possibility here to accept a worst solution with probability p
        """
        self.currentSolution.calculateCost()
        self.testSolution.calculateCost()
        delta = self.currentSolution.cost - self.testSolution.cost
        if delta <= 0 :
            return True
        else :
            r = random.random()
            p = math.exp( - ( delta /  (T0 * ( alpha ** step )) ) )
            #print(delta,T0,alpha,step)
            if r < p :
                self.onremontelapente+=1
                return True
            else :
                return False



    def modification(self, solution, destroy_method, degres_destruction, repair_method, keptinmemory, alpha, beta, gamma) :
        """
        FR:
        Fonction prenant la solution courante et la transforme suivant la méthode de destruction et la méthode de repair choisies. Cette fonction modifie current_solution. La nouvelle solution est dans current_solution.

        EN :
        Function taking the current solution and transforming it according to the chosen destruction method and repair method. This function modifies current_solution. The new solution is in current_solution.
        """
        if destroy_method == "destroy_worst_clients" :
            destroyMethods.destroy_worst_clients(solution,degres_destruction)
        if destroy_method == "destroy_random" :
            destroyMethods.destroy_random(solution,degres_destruction)
        if destroy_method == "destroy_related_client_by_distance" :
            destroyMethods.destroy_related_client_by_distance(solution, degres_destruction, self.instance.timeTravel)
        if destroy_method == "destroy_related_clients" :
            destroyMethods.destroy_related_clients(solution,degres_destruction,alpha,beta,gamma, self.instance.timeTravel)
        if destroy_method == "destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution" :
            destroyMethods.destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution(solution, degres_destruction)
        if destroy_method == "destroy_Client_with_a_request_placed_at_the_end_of_the_solution" :
            destroyMethods.destroy_Client_with_a_request_placed_at_the_end_of_the_solution(solution, degres_destruction, self.instance.listClient)
        if destroy_method == "destroy_route" :
            destroyMethods.destroy_route(solution, self.instance.listClient[0])

        if repair_method == "repair_2_regret" :
            repairsMethods.repair_2_regret(solution,keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_max_ratio_best_insertion" :
            repairsMethods.repair_max_ratio_best_insertion(solution,keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_FirstPositionAvailable_randomlistClient" :
            repairsMethods.repair_FirstPositionAvailable_randomlistClient(solution,keptinmemory, self.instance,  self.repairdontwork)
        if repair_method == "repair_randomv1" :
            repairsMethods.repair_randomv1(solution,keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_randomV2" :
            repairsMethods.repair_randomV2(solution,keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_FirstPositionAvailable_maxratio_listClient" :
            repairsMethods.repair_FirstPositionAvailable_maxratio_listClient(solution,keptinmemory, self.instance, self.repairdontwork)
        if repair_method == "repair_random_best_insertion" :
            repairsMethods.repair_random_best_insertion(solution,keptinmemory, self.instance, self.repairdontwork)


    def solve(self, N, PU, rho, sigma1, sigma2, sigma3, tolerance, C, alpha, beta, gamma, Nc, theta, Ns, showLog=False):
        """
        FR:
        Fonction principale. Les différentes parties sont representées dans le logigramme ou le pseudo code du rapport. Cette fonction a en argument tous les paramètres de l'algorithme et retourne la meilleure solution.
        current solution correspond à la solution que l'on modifie à chaque iteration.
        testsolution correspond à la solution gardée en mémoire à laquelle on va comparer current solution.

        EN :
        Main function.The different parts are represented in the flowchart or the pseudo code of the report. This function has as argument all the parameters of the algorithm and returns the best solution.
        current solution corresponds to the solution that we modify at each iteration.
        testsolution corresponds to the solution kept in memory to which we will compare current solution.
        """
        # INITIALISATION DU TEMPS
        initialTime = time.perf_counter()

        # INITIALISATION DES SOLUTIONS
        listClient = methods.order_ListClient_random(self.instance.listClient.copy())

        self.createSolution(self.instance.listClient)
        self.bestSolution.copy(self.currentSolution)
        self.testSolution.copy(self.currentSolution)

        # INITIALISATION DES VARIABLES
        T0 = ( tolerance *  self.currentSolution.cost )  /  math.log(2)  # temperature initiale
        nbIteration = 0  # nombre d'iterations
        iterationMaxSinceLastBest = Nc  # nombre d'iterations maximum avant de reinitialiser la solution
        nbIterationSinceLastBest = 0  # nombre d'iterations avant de reinitialiser la solution
        self.onremontelapente = 0 # Nombre de fois que l'on accepte une solution moins bonne
        iterationbest=[0] # iterations où on ameliore la meilleure solution
        TIME=[0] # temps où on ameliore la meilleure solution

        self.bestSolution.calculateCost()
        Cost_best_solution=[round(self.bestSolution.cost,2)] # evolution du cout de la meilleure solution

        #Headers de l'affichage de recherche de solution
        if(showLog):
            print("Nb iteration", "Clock" , "Best solution","nb de solutions moins bonnes acceptées", sep = '\t')

        # Listes des noms des methodes de destruction
        # "destroy_route",
        # "destroy_random",
        # "destroy_worst_clients",
        # "destroy_related_clients",
        # "destroy_related_client_by_distance",
        # "destroy_Client_with_a_request_placed_at_the_end_of_the_solution",
        # "destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution"

        destroy_methods = [ "destroy_route",
                            "destroy_random",
                            "destroy_worst_clients",
                            "destroy_Client_with_a_high_ratio_placed_at_the_end_of_the_solution",
                            "destroy_Client_with_a_request_placed_at_the_end_of_the_solution"        ]

        # Listes des noms des methodes de repair
        #"repair_randomV2",
        #"repair_randomv1",
        #"repair_2_regret",
        #"repair_random_best_insertion" ,
        #"repair_max_ratio_best_insertion" ,      `
        #"repair_FirstPositionAvailable_randomlistClient",
        #"repair_FirstPositionAvailable_maxratio_listClient"

        repair_methods = [ "repair_2_regret",
                           "repair_randomv1",
                           "repair_random_best_insertion",
                           "repair_max_ratio_best_insertion" ,
                           "repair_FirstPositionAvailable_maxratio_listClient"      ]

        self.repairdontwork = {i : 0 for i in repair_methods}

        # INITIALISATION DES POIDS POUR LA "ROULETTE WHEEL SELECTION"
        Weights_destroy = {i : 1/len(destroy_methods) for i in destroy_methods} # poids des methodes de destroy. Initialement tous les poids sont les memes
        Weights_repair ={i : 1/len(repair_methods) for i in repair_methods} # poids des methodes de repair. Initialement tous les poids sont les memes

        Success_destroy = {i : 0 for i in destroy_methods} # dictionnaire avec pour clé le nom de la methode et pour valeur son score de reussite
        Used_destroy_methods = {i : 0 for i in destroy_methods}#=  dictionnaire avec pour clé le nom de la methode et pour valeur son score d'utilisation

        Success_repair = {i : 0 for i in repair_methods}#= dictionnaire avec pour clé le nom de la methode et pour valeur son score de reussite
        Used_repair_methods = {i : 0 for i in repair_methods}#=  dictionnaire avec pour clé le nom de la methode et pour valeur son score d'utilisation


        USED_METHODS = {i : 0 for i in destroy_methods+repair_methods }  # dictionnaire avec pour clé le nom de la methode et pour valeut le Nombre de fois que l'on utilise une methode
        USED_METHODS_UNTIL_LAST_BEST = {}  # dictionnaire avec pour clé le nom de la methode et pour valeur le Nombre de fois que l'on utilise une methode en s'arretant à la derniere meilleure solution

        Sucess_swap = {'swap_inter_route':0, 'swap_intra_route':0} # compteur de reussite des swaps

        # CRITERE D'ARRET : N iterations maximum :
        while nbIteration < N:
            # VERIFICATION QUE L'ON AMELIORE LA BEST SOLUTION
            if(nbIterationSinceLastBest >= iterationMaxSinceLastBest):
                # Si on ameliore pas la best solution, alors on recommence en cherchant avec une nouvelle solution de départ en mélangeant la liste de création de la solution

                #Réinitialisation du compteur
                nbIterationSinceLastBest = 0

                #Shuffle de la liste sans le dépôt
                listClientSansDepot = listClient[1:]
                listClientSansDepot = methods.order_ListClient_random(listClientSansDepot)

                #Réassignation de la liste avec le dépôt à la première place
                listClient = [listClient[0]] + listClientSansDepot

                #Création d'une nouvelle solution de départ
                self.createSolution(listClient)

                #Mise à jour de la solution de test
                if(self.currentSolution.checkSolution()):
                    self.testSolution.copy(self.currentSolution)


            # CHOIX D'UN OPERATEUR DE DESTRUCTION
            degres_destruction = random.randint(math.ceil(0.1*len(self.instance.listClient)),math.ceil(0.2*len(self.instance.listClient))) # degrès de destruction faible pour detruire peu (ameliore le temps de calcul)
            #degres_destruction = random.randint(math.ceil(0.1*len(self.instance.listClient)),math.ceil(0.4*len(self.instance.listClient))) # degrès de destruction plus fort pour detruire plus de clients (allonge le temps de calcul mais permet plus de diversité dans les solutions)

            destroy_method = methods.choose_destroy_method(destroy_methods,Weights_destroy)

            Used_destroy_methods[destroy_method] += 1
            USED_METHODS[destroy_method] += 1

            # CHOIX D'UN OPERATEUR DE RECONSTRUCTION
            repair_method = methods.choose_repair_method(repair_methods,Weights_repair)

            Used_repair_methods[repair_method] += 1
            USED_METHODS[repair_method] += 1

            # MODIFICATION DE LA SOLUTION
            self.keptinmemory.copy(self.currentSolution)  # on garde en memoire la current solution avant qu'elle soit modifiée, car si les fonction ne marchent pas, on repart de cette solution
            #self.keptinmemory.copy(self.bestSolution) # on garde en memoire la best solution avant que la current solution soit modifiée, car si les fonction ne marchent pas, on repart de la best solution

            self.modification(self.currentSolution,destroy_method,degres_destruction,repair_method,self.keptinmemory,alpha,beta,gamma)

            if not self.currentSolution.checkSolution() :
                self.currentSolution.copy(self.keptinmemory)
            else :
                self.keptinmemory.copy(self.currentSolution)

            # ATTEINT-ON LA CONDITION POUR FAIRE LES SWAPS ?
            """
            print("before swap")
            if self.currentSolution.cost < ( 1+ theta ) * self.testSolution.cost :
                print("in swap")
                # ON REALISE Ns SWAPS DE CHAQUE TYPE : 'swap_inter_route' & 'swap_intra_route'
                for k in range(Ns) :
                    print(k)
                    # SWAP de deux clients au sein d'une route
                    methods.swap_inter_route(self.currentSolution)

                    self.currentSolution.calculateCost()
                    self.keptinmemory.calculateCost()

                    if self.currentSolution.cost < self.keptinmemory.cost : # si le swap ameliore la solution on la garde en memoire
                        self.keptinmemory.copy(self.currentSolution)
                        Sucess_swap['swap_inter_route']+=1

                    # SWAP de deux clients au hasard dans la solution
                    methods.swap_intra_route(self.currentSolution)

                    if self.currentSolution.cost > self.keptinmemory.cost : # si le swap deteriore la solution, on repaart de celle juste avant
                        self.currentSolution.copy(self.keptinmemory)
                    else :
                        self.keptinmemory.copy(self.currentSolution) # si le swap ameliore la solution on la garde en memoire
                        Sucess_swap['swap_intra_route']+=1
            print("after swap")
            """

            self.currentSolution.calculateCost()
            self.keptinmemory.calculateCost()

            # VERIFICATION DE LA SOLUTION (CONTRAINTES)
            if not self.currentSolution.checkSolution() :
                self.currentSolution.copy(self.keptinmemory)

            # CRITERE D'ACCEPTATION

            # self.acceptance_criteria_simulated_annealing(T0,alpha,nbIteration)
            # self.acceptance_criteria_greedy()

            if self.acceptance_criteria_simulated_annealing(T0,C,nbIteration) :

                if self.currentSolution.cost < self.bestSolution.cost :
                    # si la solution ameliore la bestsolution, on met a jour testsolution est bestsolution et on recompense les methodes qui ont reussi par la quantite sigma1
                    self.testSolution.copy(self.currentSolution)
                    self.bestSolution.copy(self.currentSolution)

                    Success_destroy[destroy_method] += sigma1
                    Success_repair[repair_method] += sigma1

                    self.bestSolution.calculateCost()

                    # mise a jour des variables d'informations

                    Cost_best_solution.append(round(self.bestSolution.cost,2)   )
                    TIME.append(round(time.perf_counter() - initialTime,3))
                    USED_METHODS_UNTIL_LAST_BEST = copy.deepcopy(USED_METHODS)
                    nbIterationSinceLastBest = 0
                    iterationbest.append(nbIteration+1)

                elif  self.bestSolution.cost < self.currentSolution.cost < self.testSolution.cost :
                    # si la solution ameliore la testsolution (la solution courrante gardée en memoire), on met a jour uniquement testsolution et on recompense les methodes qui ont reussi par la quantite sigma2
                    self.testSolution.copy(self.currentSolution)

                    Success_destroy[destroy_method] += sigma2
                    Success_repair[repair_method] += sigma2

                elif self.currentSolution.cost !=  self.testSolution.cost :
                    # si la solution n'ameliore rien mais qu'elle est acceptée par l'acceptance criteria (cas ou on accepte une solution moins bonne avec le simulated annealing), on met a jour uniquement testsolution et on recompense les methodes par la quantite sigma3
                    self.testSolution.copy(self.currentSolution)

                    Success_destroy[destroy_method] += sigma3
                    Success_repair[repair_method] += sigma3

            # A T ON ATTEINT Pu ITERATIONS ?== 0  : Si oui : changements des probabilités associées a chaque methode
            if (nbIteration+1)%PU == 0 :
                Weights_destroy,Weights_repair = methods.update_weights(rho,Weights_destroy,Weights_repair,Success_destroy,Success_repair,Used_destroy_methods,Used_repair_methods)

                Success_destroy = {i:0 for i in destroy_methods}
                Success_repair = {i:0 for i in repair_methods}

                Used_destroy_methods = {i:0 for i in destroy_methods}
                Used_repair_methods = {i:0 for i in repair_methods}

            # mise à jour du nombre d'iterations
            nbIteration += 1
            nbIterationSinceLastBest += 1

            if(showLog and nbIteration % self.frequenceAffichage == 0):
                print(nbIteration, "           ", round(time.perf_counter()- initialTime, 2), "  ", round(self.bestSolution.cost, 2), "               ",self.onremontelapente)
                self.onremontelapente=0


        if(showLog):
            print()
            print("Nombre de fois ou les repair ne marchent pas et on repart de la solution gardee en memoire:")
            print(self.repairdontwork)
            print()
            print("Iterations où on ameliore la meilleure solution:")
            print(iterationbest)
            print()
            print("Temps où on ameliore la meilleure solution:")
            print(TIME)
            print()
            print("Evolution du cout de la meilleure solution")
            print(Cost_best_solution )
            print()
            print("Utilisation des methodes jusqu'a la derniere meilleure solution : ")
            print(USED_METHODS_UNTIL_LAST_BEST)
            print()
            print("Utilisation des methodes : ")
            print(USED_METHODS)
            print()
            print("poids des methodes de destructions : ")
            print(Weights_destroy)
            print()
            print("poids des methodes de repair: ")
            print(Weights_repair)
            print()
            print("Succes des swaps")
            print(Sucess_swap)
            print()
            print("BEST SOLUTION :")
            self.bestSolution.display()

        return (self.bestSolution, iterationbest, Cost_best_solution, TIME, USED_METHODS_UNTIL_LAST_BEST, USED_METHODS)
