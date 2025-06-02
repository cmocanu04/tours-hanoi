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
        Returns:
            None
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
        
        Returns:
            None
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
    
    

    def calculer_heuristique(self, etat_actuel_tuple, liste_tailles_disques_asc, idx_tour_cible):
        """
        Calcule l'heuristique h(n) pour l'état actuel.
        Heuristique : Pour chaque disque i, si non sur la tour cible, +1.
        Args:
            etat_actuel_tuple (tuple): L'état courant sous forme de tuple de tuples.
            liste_tailles_disques_asc (list): Liste des tailles de disques du plus petit au plus grand.
            idx_tour_cible (int): Index de la tour cible.

        Returns:
            int: Valeur heuristique pour l'état courant.
        """
        h = 0
        # Parcourt chaque disque du plus petit au plus grand
        for taille_disque in liste_tailles_disques_asc:  # Itère du plus petit au plus grand
            tour_trouvee = -1
            index_disque_sur_tour = -1  # Index dans le tuple de la tour (0 = fond)

            # Recherche sur quelle tour se trouve le disque
            for idx_tour, contenu_tour_tuple in enumerate(etat_actuel_tuple):
                try:
                    # Trouve l'index du disque sur cette tour.
                    # Rappel: le tuple de la tour est (fond, ..., sommet)
                    index_disque_sur_tour = contenu_tour_tuple.index(taille_disque)
                    tour_trouvee = idx_tour
                    break
                except ValueError:
                    continue  # Disque non trouvé sur cette tour

            if tour_trouvee == -1:
                # Cela ne devrait pas arriver dans un état valide de Hanoï si tous les disques sont suivis
                continue

            if tour_trouvee != idx_tour_cible:
                h += 1  # Le disque n'est pas sur la bonne tour 
            
        return h

    def generer_voisins(self, etat_actuel_tuple, nb_tours):
        """
        Génère tous les états voisins valides à partir de l'état actuel.
        Retourne une liste de (etat_voisin_tuple, mouvement_tuple).
        mouvement_tuple est (index_tour_source, index_tour_destination).
        Args:
            etat_actuel_tuple (tuple): L'état courant sous forme de tuple de tuples.
            nb_tours (int): Nombre de tours.
        Returns:
            list: Liste de tuples (état voisin, mouvement effectué).
        """
        voisins = []
        # Convertit l'état en listes de listes pour modification facile
        liste_tours = [list(t) for t in etat_actuel_tuple]
        #ex. [[4,2,3],[],[]]

        # Parcourt chaque tour comme source potentielle
        for idx_source in range(nb_tours):  # Index de la tour source
            if not liste_tours[idx_source]:  # Tour source vide
                continue

            # Le disque à déplacer est le dernier de la liste (sommet de la tour source)
            disque_a_deplacer = liste_tours[idx_source][-1]
            

            # Parcourt chaque tour comme destination potentielle
            for idx_dest in range(nb_tours):  # Index de la tour destination
                if idx_source == idx_dest:  # Ne peut pas déplacer sur la même tour
                    continue

                # Vérifie la validité du mouvement idx_source -> idx_dest
                # Mouvement valide si la destination est vide ou si le disque au sommet de la destination est plus grand
                if not liste_tours[idx_dest] or disque_a_deplacer < liste_tours[idx_dest][-1]:
                    # Mouvement valide: destination vide ou disque au sommet plus grand

                    # Crée une nouvelle copie de l'état pour ce voisin
                    nouvelles_tours = [list(t) for t in liste_tours]
                    val_deplacee = nouvelles_tours[idx_source].pop()  # Enlève de la source
                    nouvelles_tours[idx_dest].append(val_deplacee)  # Ajoute à la destination

                    # Transforme la nouvelle configuration en tuple de tuples pour l'immuabilité
                    voisin_tuple = tuple(tuple(t) for t in nouvelles_tours)
                    # Ajoute le voisin et le mouvement effectué à la liste
                    voisins.append((voisin_tuple, (idx_source, idx_dest)))

        return voisins




############################################################################################################

    def resoudre_automatiquement(self):
        """
        ####################### Utilisation d'outils IA - GEMINI #################################
        ### Adaptation de l'algorithme de recherche du meilleur chemin A* pour le cas de notre jeu. ###

        
        La fonction résout le jeu automatiquement en utilisant l'algorithme l'algorithme de recherche
        A* (pour l'ordre Normal et Aléatoire).

        Returns:
            list[tuple[int, int]]: Liste des mouvements (tour départ, tour arrivée).
        """
        mouvements = []
        self.mode_jeu = 'auto'

        # --- Partie pour la résolution A* (mode_aleatoire = True) ---
        nb_tours = len(self.tours)
        if nb_tours == 0:  # Pas de tours définies
            return []

        # L'index 0-basé de la tour cible pour la logique interne de A* (ici la 3ème tour)
        idx_tour_cible = 2
        # Vérification de sécurité :
        if idx_tour_cible >= nb_tours:
            return []  # Erreur d'index

        # Représente l'état initial sous forme de tuple de tuples (pour chaque tour, du fond au sommet)
        etat_initial_tuple = tuple(tuple(d.taille for d in tour.disques) for tour in self.tours)
        # ex. ((4, 2, 3), (), ())

        # Liste des tailles de disques du plus petit au plus grand (pour l'heuristique)
        liste_tailles_disques_asc = list(range(2, self.nombre_disques + 2))

        if not liste_tailles_disques_asc:  # Pas de disques
            return []

        # Pré-calcul des disques pour la tour cible (du plus grand au plus petit)
        disques_tour_cible = tuple(reversed(liste_tailles_disques_asc))
        # Construction de l'état objectif (goal) : tous les disques sur la tour cible
        etat_objectif_tuple = tuple(disques_tour_cible if i == idx_tour_cible else () for i in range(nb_tours))
        #ex. ((), (), (4, 3, 2))
        

        # Initialisation de la file de priorité (open_set) pour A*
        file_priorite = []
        # Calcul de l'heuristique initiale
        h_initiale = self.calculer_heuristique(etat_initial_tuple, liste_tailles_disques_asc, idx_tour_cible)
        
        heapq.heappush(file_priorite, (h_initiale, etat_initial_tuple))
        
        # Dictionnaire pour retrouver le chemin (état précédent et mouvement)
        provenance = {}
        # Dictionnaire des coûts g(n) pour chaque état
        cout_g = {etat_initial_tuple: 0}

        # Liste pour stocker les mouvements (index 0-basé)
        chemin_mouvements_0_index = []

        # Boucle principale de l'algorithme A*
        while file_priorite:
            score_f_courant, etat_courant = heapq.heappop(file_priorite)
            
            # Vérifie que le score f(n) est cohérent (sécurité)
            if score_f_courant > cout_g[etat_courant] + self.calculer_heuristique(etat_courant, liste_tailles_disques_asc, idx_tour_cible):
                continue

            # Si l'état objectif est atteint, on reconstitue le chemin
            if etat_courant == etat_objectif_tuple:
                etat_trace = etat_courant
                while etat_trace in provenance:
                    etat_precedent, mouvement_0_index = provenance[etat_trace]
                    chemin_mouvements_0_index.append(mouvement_0_index)  # (source, destination)
                    etat_trace = etat_precedent
                break

            # Génère tous les voisins valides de l'état courant
            for voisin_tuple, mouvement_tuple in self.generer_voisins(etat_courant, nb_tours):
                cout_tentatif = cout_g[etat_courant] + 1

                # Si ce chemin vers le voisin est meilleur que tout chemin précédent
                if cout_tentatif < cout_g.get(voisin_tuple, float('inf')):
                    provenance[voisin_tuple] = (etat_courant, mouvement_tuple)
                    cout_g[voisin_tuple] = cout_tentatif
                    # Calcul de l'heuristique pour le voisin
                    h_voisin = self.calculer_heuristique(voisin_tuple, liste_tailles_disques_asc, idx_tour_cible)
                    f_voisin = cout_tentatif + h_voisin
                    heapq.heappush(file_priorite, (f_voisin, voisin_tuple))

        # Convertit les mouvements 0-indexés en mouvements utilisant Tour.numero
        if chemin_mouvements_0_index:  # Si une solution a été trouvée
            for idx_source, idx_dest in reversed(chemin_mouvements_0_index):  # Inverser pour l'ordre correct
                # Vérifie la validité des index avant d'accéder à self.tours
                if 0 <= idx_source < len(self.tours) and 0 <= idx_dest < len(self.tours):
                    numero_source = self.tours[idx_source].numero
                    numero_dest = self.tours[idx_dest].numero
                    mouvements.append((numero_source, numero_dest))
                else:
                    # Gérer l'erreur : index invalide pour self.tours
                    return []  # Solution invalide ou incomplète

        return mouvements


############################################################################################################