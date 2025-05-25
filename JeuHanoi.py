from Disque import Disque
from Tour import Tour
import random
import time
import copy

import heapq


class JeuHanoi:
    """
    Gère la logique complète du jeu des tours de Hanoï.

    Attributs:
        nombre_disques (int): Nombre total de disques dans le jeu.
        mode_jeu (str): 'manuel' ou 'auto'.
        score (int): Score actuel du joueur.
        chrono (float): Temps écoulé.
        nbr_coups (int): Nombre de coups effectués.
        etat_partie (bool): True si la partie est en cours, False sinon.
        ordre_disques_initiaux (list[Disque]): Ordre de départ des disques.
    """
    def __init__(self, nombre_disques=3, mode_jeu='manuel'):
        self.nombre_disques = nombre_disques
        self.mode_jeu = mode_jeu
        self.score = 0
        self.chrono = 0
        self.temps_debut = 0 
        self.nbr_coups = 0
        self.etat_partie = False
        self.ordre_disques_initiaux = []
        self.mode_aleatoire = False
        
        # Initialiser les tours
        self.tours = [Tour(i+1) for i in range(3)]
        
        # Initialiser les disques dans l'ordre standard
        self.initialiser_disques()
    
    def initialiser_disques(self, mode_aleatoire=False):
        """
        Initialise les disques sur la première tour.
        
        Args:
            mode_aleatoire (bool): Si True, place les disques dans un ordre aléatoire.
        """
        # Vider toutes les tours
        for tour in self.tours:
            tour.disques = []
            
        # Créer les disques
        disques = [Disque(i+1) for i in range(self.nombre_disques, 0, -1)]
        
        if mode_aleatoire:
            random.shuffle(disques)
            self.mode_aleatoire = True

        self.ordre_disques_initiaux = disques.copy()
        
        # Placer les disques sur la première tour
        for disque in disques:
            self.tours[0].empiler(disque)

    def deplacement_valide(self, tour_depart, tour_arrivee):
        """
        Vérifie si le déplacement entre deux tours est valide.

        Args:
            tour_depart (Tour): La tour de départ.
            tour_arrivee (Tour): La tour de destination.

        Returns:
            bool: True si le déplacement est autorisé, False sinon.
        """
        # Vérifier si la tour de départ est vide
        if tour_depart.est_vide():
            return False
            
        # Si la tour d'arrivée est vide, le déplacement est valide
        if tour_arrivee.est_vide():
            return True
            
        # Vérifier si le disque du dessus de la tour de départ est plus petit
        # que celui du dessus de la tour d'arrivée
        return tour_depart.top_disque().taille < tour_arrivee.top_disque().taille
        
    def jouer_coup(self, tour_depart, tour_arrivee):
        """
        Effectue un coup si le déplacement est valide.

        Args:
            tour_depart (Tour): La tour de départ.
            tour_arrivee (Tour): La tour de destination.

        Returns:
            bool: True si le coup a été joué, False sinon.
        """
        if self.deplacement_valide(tour_depart, tour_arrivee):
            disque = tour_depart.depiler()
            tour_arrivee.empiler(disque)
            self.nbr_coups += 1
            return True
        return False

    def ajouter_score(self, points):
        """
        Ajoute des points au score du joueur.

        Args:
            points (int): Nombre de points à ajouter.
        """
        self.score += points
  
    def gagner(self):
        """
        Vérifie si tous les disques sont bien empilés sur la dernière tour.

        Returns:
            bool: True si le joueur a gagné, False sinon.
        """
        # Vérifier si la dernière tour contient tous les disques
        return len(self.tours[2].disques) == self.nombre_disques and \
               all(self.tours[2].disques[i].taille > self.tours[2].disques[i+1].taille 
                   for i in range(len(self.tours[2].disques)-1))

    def demarrer_chrono(self):
        """
        Lance le chronomètre de la partie.
        """
        self.temps_debut = time.time()
        self.chrono = 0
        self.etat_partie = True


    def arreter_chrono(self):
        """
        Arrête le chronomètre et retourne le temps écoulé.

        Returns:
            float: Le temps écoulé en secondes.
        """
        if self.etat_partie:
            self.chrono = time.time() - self.temps_debut
            self.etat_partie = False
        return self.chrono


    def generer_ordre_aleatoire(self, nb):
        """
        Génère un ordre aléatoire de disques non trié.

        Args:
            nb (int): Nombre de disques.

        Returns:
            list[Disque]: Liste de disques dans un ordre aléatoire.
        """
        disques = [Disque(i+1) for i in range(nb)]
        random.shuffle(disques)
        return disques
    
    
    ###############################

    def _calculate_heuristic(self, current_state_tuple, all_disk_sizes_sorted_asc_list, target_peg_idx):
        """
        Calcule l'heuristique h(n) pour l'état actuel.
        Heuristique : Pour chaque disque i, si non sur la tour cible, +1.
                    Si sur la tour cible mais un disque j < i est en dessous, +2.
        """
        h = 0
        # Parcourt chaque disque du plus petit au plus grand
        for disk_to_check_size in all_disk_sizes_sorted_asc_list: # Itère du plus petit au plus grand
            disk_found_at_peg = -1
            disk_found_at_index_on_peg = -1 # Index dans le tuple de la tour (0 = fond)

            # Recherche sur quelle tour se trouve le disque
            for peg_idx, peg_content_tuple in enumerate(current_state_tuple):
                try:
                    # Trouve l'index du disque sur cette tour.
                    # Rappel: le tuple de la tour est (fond, ..., sommet)
                    disk_found_at_index_on_peg = peg_content_tuple.index(disk_to_check_size)
                    disk_found_at_peg = peg_idx
                    break 
                except ValueError:
                    continue # Disque non trouvé sur cette tour
            
            if disk_found_at_peg == -1:
                # Cela ne devrait pas arriver dans un état valide de Hanoï si tous les disques sont suivis
                # print(f"Avertissement : Disque {disk_to_check_size} non trouvé dans l'état {current_state_tuple}")
                continue 

            if disk_found_at_peg != target_peg_idx:
                h += 1  # Le disque n'est pas sur la bonne tour
            else:
                # Le disque est sur la tour cible. Vérifier s'il est bloqué par un plus petit en dessous.
                target_peg_content = current_state_tuple[target_peg_idx]
                # Les disques en dessous sont ceux avec un index plus petit sur la tour cible
                for i in range(disk_found_at_index_on_peg):
                    disk_underneath_size = target_peg_content[i]
                    if disk_underneath_size < disk_to_check_size:
                        h += 2  # Doit être déplacé puis remis
                        break 
        return h

    def _generate_neighbors(self, current_state_tuple, num_pegs):
        """
        Génère tous les états voisins valides à partir de l'état actuel.
        Retourne une liste de (etat_voisin_tuple, mouvement_tuple).
        mouvement_tuple est (index_tour_source, index_tour_destination).
        """
        neighbors = []
        # Convertit l'état en listes de listes pour modification facile
        list_of_peg_lists = [list(p) for p in current_state_tuple]
        
        # Parcourt chaque tour comme source potentielle
        for s_idx in range(num_pegs): # Index de la tour source
            if not list_of_peg_lists[s_idx]: # Tour source vide
                continue
            
            # Le disque à déplacer est le dernier de la liste (sommet de la tour)
            disk_to_move = list_of_peg_lists[s_idx][-1]

            # Parcourt chaque tour comme destination potentielle
            for d_idx in range(num_pegs): # Index de la tour destination
                if s_idx == d_idx: # Ne peut pas déplacer sur la même tour
                    continue

                # Vérifie la validité du mouvement
                # Mouvement valide si la destination est vide ou si le disque au sommet de la destination est plus grand
                if not list_of_peg_lists[d_idx] or disk_to_move < list_of_peg_lists[d_idx][-1]:
                    # Mouvement valide: destination vide ou disque au sommet plus grand
                    
                    # Crée une nouvelle copie de l'état pour ce voisin
                    new_peg_lists = [list(p) for p in list_of_peg_lists] 
                    moved_disk_val = new_peg_lists[s_idx].pop() # Enlève de la source
                    new_peg_lists[d_idx].append(moved_disk_val) # Ajoute à la destination
                    
                    # Transforme la nouvelle configuration en tuple de tuples pour l'immuabilité
                    neighbor_state_tuple = tuple(tuple(p) for p in new_peg_lists)
                    # Ajoute le voisin et le mouvement effectué à la liste
                    neighbors.append((neighbor_state_tuple, (s_idx, d_idx)))
        return neighbors
    
##########################################################



    def resoudre_automatiquement(self):
        """
        Résout le jeu automatiquement en utilisant l'algorithme récursif (pour l'ordre standard)
        ou l'algorithme A* (pour l'ordre aléatoire).

        Returns:
            list[tuple[int, int]]: Liste des mouvements (tour départ, tour arrivée).
        """
        mouvements = []

        # Cas classique : résolution récursive pour l'ordre standard
        if self.mode_aleatoire == False:
            
            def hanoi_recursif(n, source, destination, auxiliaire):
                # Si il reste des disques à déplacer
                if n > 0:
                    # Déplacer n-1 disques de source vers auxiliaire en utilisant destination comme intermédiaire
                    hanoi_recursif(n-1, source, auxiliaire, destination)
                    
                    # Déplacer le disque n de source vers destination
                    mouvements.append((source.numero, destination.numero))
                    
                    # Déplacer n-1 disques de auxiliaire vers destination en utilisant source comme intermédiaire
                    hanoi_recursif(n-1, auxiliaire, destination, source)
            
            # Appel initial de la fonction récursive avec toutes les tours
            hanoi_recursif(self.nombre_disques, self.tours[0], self.tours[2], self.tours[1])

            return mouvements
        
        else :
            # --- Partie pour la résolution A* (mode_aleatoire = True) ---
            num_pegs = len(self.tours)
            if num_pegs == 0: # Pas de tours définies
                return []

            # L'index 0-basé de la tour cible pour la logique interne de A* (ici la 3ème tour)
            internal_target_peg_0_idx = 2 
            # Vérification de sécurité :
            if internal_target_peg_0_idx >= num_pegs:
                # print(f"Erreur: internal_target_peg_0_idx ({internal_target_peg_0_idx}) est hors limites pour num_pegs ({num_pegs})")
                return [] # Ou lever une exception

            # Représente l'état initial sous forme de tuple de tuples (pour chaque tour, du fond au sommet)
            initial_state_tuple = tuple(tuple(d.taille for d in tour.disques) for tour in self.tours)
            
            # Liste des tailles de disques du plus petit au plus grand (pour l'heuristique)
            all_disk_sizes_s_asc = list(range(2, self.nombre_disques + 2))
            
            if not all_disk_sizes_s_asc: # Pas de disques
                return []

            # Pré-calcul des disques pour la tour cible (du plus grand au plus petit)
            disks_for_target_peg = tuple(reversed(all_disk_sizes_s_asc))
            # Construction de l'état objectif (goal) : tous les disques sur la tour cible
            goal_state_tuple = tuple(disks_for_target_peg if i == internal_target_peg_0_idx else () for i in range(num_pegs))
            
            # Initialisation de la file de priorité (open_set) pour A*
            open_set = [] 
            # Calcul de l'heuristique initiale
            h_initial = self._calculate_heuristic(initial_state_tuple, all_disk_sizes_s_asc, internal_target_peg_0_idx)
            heapq.heappush(open_set, (h_initial, initial_state_tuple))

            # Dictionnaire pour retrouver le chemin (état précédent et mouvement)
            came_from = {} 
            # Dictionnaire des coûts g(n) pour chaque état
            g_score = {initial_state_tuple: 0}

            # Liste pour stocker les mouvements (index 0-basé)
            path_0_indexed_moves = []

            # Boucle principale de l'algorithme A*
            while open_set:
                current_f_score, current_state = heapq.heappop(open_set)
                
                # Vérifie que le score f(n) est cohérent (sécurité)
                if current_f_score > g_score[current_state] + self._calculate_heuristic(current_state, all_disk_sizes_s_asc, internal_target_peg_0_idx):
                    continue

                # Si l'état objectif est atteint, on reconstitue le chemin
                if current_state == goal_state_tuple:
                    temp_trace_state = current_state
                    while temp_trace_state in came_from:
                        prev_trace_state, move_0_indexed_tuple = came_from[temp_trace_state]
                        path_0_indexed_moves.append(move_0_indexed_tuple) # move_0_indexed_tuple est (s_idx, d_idx)
                        temp_trace_state = prev_trace_state
                    break 
                
                # Génère tous les voisins valides de l'état courant
                for neighbor_s_tuple, move_m_tuple in self._generate_neighbors(current_state, num_pegs):
                    tentative_g = g_score[current_state] + 1

                    # Si ce chemin vers le voisin est meilleur que tout chemin précédent
                    if tentative_g < g_score.get(neighbor_s_tuple, float('inf')):
                        came_from[neighbor_s_tuple] = (current_state, move_m_tuple)
                        g_score[neighbor_s_tuple] = tentative_g
                        # Calcul de l'heuristique pour le voisin
                        h_val_neighbor = self._calculate_heuristic(neighbor_s_tuple, all_disk_sizes_s_asc, internal_target_peg_0_idx)
                        f_val_neighbor = tentative_g + h_val_neighbor
                        heapq.heappush(open_set, (f_val_neighbor, neighbor_s_tuple))
            
            # Convertit les mouvements 0-indexés en mouvements utilisant Tour.numero
            if path_0_indexed_moves: # Si une solution a été trouvée
                for s_0_idx, d_0_idx in reversed(path_0_indexed_moves): # Inverser pour l'ordre correct
                    # Vérifie la validité des index avant d'accéder à self.tours
                    if 0 <= s_0_idx < len(self.tours) and 0 <= d_0_idx < len(self.tours):
                        source_numero = self.tours[s_0_idx].numero
                        dest_numero = self.tours[d_0_idx].numero
                        mouvements.append((source_numero, dest_numero))
                    else:
                        # Gérer l'erreur : index invalide pour self.tours
                        # print(f"Erreur: index de tour invalide ({s_0_idx}, {d_0_idx}) lors de la conversion des mouvements.")
                        return [] # Solution invalide ou incomplète
            
            return mouvements


