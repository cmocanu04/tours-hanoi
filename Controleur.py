from JeuHanoi import JeuHanoi
from Quiz import Quiz
from Vue import Vue
from Tour import Tour 
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime


class Controleur:
    """
    Coordonne la logique du jeu, les entrées utilisateur et l'affichage.

    Attributs:
        jeuhanoi (JeuHanoi): L'objet principal du jeu.
        vue (Vue): L'interface graphique.
        quiz (Quiz): Le gestionnaire de quiz.
    """
    def __init__(self):
        self.jeuhanoi = JeuHanoi()
        self.quiz = Quiz()
        self.vue = Vue(self)
        
        # Charger les questions du quiz
        self.quiz.charger_questions_csv("dico_quizz_tour.csv")
        
        # Variables pour la sélection des tours
        self.tour_selectionnee = None
        self.dernier_coup_correct = False
        
        # Démarrer une partie par défaut
        self.demarrer_partie(3, False)
        



    def demarrer_partie(self, nb_disques, mode_aleatoire):
        """
        Initialise une nouvelle partie.

        Args:
            nb_disques (int): Nombre de disques.
            mode_aleatoire (bool): Active ou non le mode aléatoire.

        Returns:
            None
        """
        self.nb_disques = nb_disques
        self.jeuhanoi = JeuHanoi(nb_disques)
        self.jeuhanoi.initialiser_disques(mode_aleatoire)
        self.jeuhanoi.demarrer_chrono()
        self.tour_selectionnee = None
        self.dernier_coup_correct = False
        self.vue.tour_selectionnee = None
        
        # Mettre à jour l'interface
        self.vue.mettre_a_jour_interface(self.jeuhanoi)
        


    def gerer_deplacement_joueur(self, tour_depart, tour_arrivee, resolution_auto=False):
        """
        Gère un déplacement manuel effectué par le joueur.

        Args:
            tour_depart (Tour): Tour de départ.
            tour_arrivee (Tour): Tour de destination.
            resolution_auto (bool): True si on est en mode résolution automatique, False sinon.

        Returns:
            None
        """
        if self.jeuhanoi.jouer_coup(tour_depart, tour_arrivee):
            # Marquer le coup comme correct
                self.dernier_coup_correct = True

            # Mettre à jour l'interface
                self.vue.mettre_a_jour_interface(self.jeuhanoi)

                # Poser une question de quiz après un coup 'correct' sur la tour 3
                # Ne pas poser de question si on est en mode résolution automatique

                if self.dernier_coup_correct and (tour_arrivee.numero == 3) and (tour_arrivee.disques[-1].taille == self.nb_disques+1) and resolution_auto == False:
                    self.nb_disques-=1
                    question, _ = self.quiz.poser_question()
                    self.vue.afficher_quiz(question)
                    
                # Vérifier si le joueur a gagné
                if self.jeuhanoi.gagner():
                    self.jeuhanoi.arreter_chrono()
                    score_final = max(1000 - self.jeuhanoi.nbr_coups * 10 - int(self.jeuhanoi.chrono) * 5, 0)
                    self.jeuhanoi.ajouter_score(score_final)
                    self.vue.mettre_a_jour_interface(self.jeuhanoi)
                    messagebox.showinfo("Félicitations", 
                                    f"Vous avez gagné en {self.jeuhanoi.nbr_coups} coups et {int(self.jeuhanoi.chrono)} secondes!")
        else:
            self.dernier_coup_correct = False
        
    def traiter_clic_tour(self, numero_tour):
        """
        Gère la logique de sélection/déplacement à partir du clic utilisateur.

        Args:
            numero_tour (int): Indice de la tour cliquée.

        Returns:
            None    
        """
        if not self.jeuhanoi.etat_partie:
            return
            
        tour = self.jeuhanoi.tours[numero_tour]
        
        # Si aucune tour n'est sélectionnée, sélectionner celle-ci
        if self.tour_selectionnee is None:
            if not tour.est_vide():
                self.tour_selectionnee = tour
        else:
            # Si une tour est déjà sélectionnée, tenter un déplacement
            if self.tour_selectionnee != tour:
                self.gerer_deplacement_joueur(self.tour_selectionnee, tour)
            
            # Désélectionner la tour
            self.tour_selectionnee = None
            self.vue.tour_selectionnee = None
            self.vue.afficher_tout(self.jeuhanoi)



    def demarrer_resolution_auto(self):
        """
        Lance la résolution automatique du problème.

        Returns:
            None
        """
        # Réinitialiser le jeu
        nb_disques = self.jeuhanoi.nombre_disques

        
        # Obtenir la séquence de mouvements
        mouvements = self.jeuhanoi.resoudre_automatiquement()
        
        # Exécuter les mouvements avec un délai
        def executer_mouvement(index):
            if index < len(mouvements):
                depart, arrivee = mouvements[index]
                self.gerer_deplacement_joueur(
                    self.jeuhanoi.tours[depart-1], 
                    self.jeuhanoi.tours[arrivee-1], True
                )
            
                self.vue.fenetre.after(500, lambda: executer_mouvement(index + 1))
        
        # Démarrer l'exécution automatique
        self.vue.fenetre.after(500, lambda: executer_mouvement(0))
        
    def activer_ordre_aleatoire(self):
        """
        Active le mode où les disques sont placés dans un ordre illégal au départ.

        Returns:
            None
        """
        nb_disques = self.jeuhanoi.nombre_disques
        self.demarrer_partie(nb_disques, True)




    def config_nbr_disque(self, nombre_disques):
        """
        Configure le nombre de disques au début du jeu.

        Args:
            nombre_disques (int): Nombre de disques choisis par l'utilisateur.

        Returns:
            None    
        """
        try:
            nb = int(nombre_disques)
            if 3 <= nb <= 8:  # Limiter entre 3 et 8 disques
                self.demarrer_partie(nb, False)
        except ValueError:
            pass
        

    def gerer_reponse_quiz(self, reponse):
        """
        Vérifie la réponse du joueur au quiz et applique bonus ou malus.

        Args:
            reponse (str): Réponse donnée par le joueur.
            
        Returns:
            None
        """
        if not self.jeuhanoi.etat_partie:
            return
            
        if self.quiz.verifier_reponse(reponse):
            # Bonne réponse: bonus de temps
            bonus = self.quiz.attribuer_bonus_temps()
            self.jeuhanoi.temps_debut = max(0, self.jeuhanoi.temps_debut + bonus)
            messagebox.showinfo("Correct!", f"Bonne réponse! -{bonus} secondes.")
        else:
            # Mauvaise réponse: malus de temps
            malus = self.quiz.attribuer_malus_temps()
            self.jeuhanoi.temps_debut -= malus
            messagebox.showinfo("Incorrect", 
                               f"Mauvaise réponse. La réponse correcte était: {self.quiz.reponse_attendue}. "
                               f" +{malus} secondes")
        
        # Mettre à jour l'interface
        self.vue.mettre_a_jour_interface(self.jeuhanoi)

