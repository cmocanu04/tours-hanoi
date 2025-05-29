
import tkinter as tk

from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo

import time

class Vue:
    """
    Gère l'interface graphique du jeu.

    Attributs:
        etiquettes (dict): Éléments d'étiquettes affichés à l'écran.
        boutons (dict): Boutons interactifs de l'interface.
        champs_texte (dict): Champs de saisie de texte.
        champs_chrono (widget): Affichage du chronomètre.
        champs_quiz (widget): Zone d'affichage des questions.
    """
    def __init__(self, controleur):
        self.controleur = controleur
        self.fenetre = tk.Tk()
        self.fenetre.title("Tours de Hanoï")
        self.fenetre.geometry("800x600")

        
        
        self.etiquettes = {}
        self.boutons = {}
        self.champs_texte = {}
        self.tour_selectionnee = None
        
        self.canvas = tk.Canvas(self.fenetre, width=800, height=400, bg="lightgray")
        self.canvas.pack(pady=10)
        
        self.canvas.bind("<Button-1>", self.gerer_clic)
        
        self.initialiser_interface()
        self.update_chrono()  # Ajout de l'appel initial
        


    def initialiser_interface(self):
        """
        Initialise tous les éléments de l'interface graphique.

        Returns:
            None
        """
        # Frame pour les contrôles
        # On utilise frame - widget conteneur de tkinter

        frame_controles = tk.Frame(self.fenetre)
        frame_controles.pack(fill=tk.X, padx=10, pady=5)
        
        # Boutons de contrôle
        self.boutons["nouvelle_partie"] = tk.Button(frame_controles, text="Nouvelle Partie", 
                                                   command=lambda: self.controleur.demarrer_partie(3, False))
        self.boutons["nouvelle_partie"].pack(side=tk.LEFT, padx=5)
        
        self.boutons["mode_aleatoire"] = tk.Button(frame_controles, text="Mode Aléatoire", 
                                                  command=self.controleur.activer_ordre_aleatoire)
        self.boutons["mode_aleatoire"].pack(side=tk.LEFT, padx=5)
        
        self.boutons["resolution_auto"] = tk.Button(frame_controles, text="Résolution Auto", 
                                                   command=self.controleur.demarrer_resolution_auto)
        self.boutons["resolution_auto"].pack(side=tk.LEFT, padx=5)
        
        self.boutons["aide_moi"] = tk.Button(frame_controles, text="Aide-moi",
                                                    command=self.controleur.demander_aide)
        self.boutons["aide_moi"].pack(side=tk.LEFT, padx=5)



        # Nombre de disques
        tk.Label(frame_controles, text="Nombre de disques:").pack(side=tk.LEFT, padx=5)
        
        self.var_nb_disques = tk.IntVar(value=3)
        
        disques_spinbox = tk.Spinbox(frame_controles, from_=3, to=8, width=2, 
                                     textvariable=self.var_nb_disques,
                                     command=lambda: self.controleur.config_nbr_disque(self.var_nb_disques.get()))
        disques_spinbox.pack(side=tk.LEFT)
        
        # Frame pour les informations
        frame_info = tk.Frame(self.fenetre)
        frame_info.pack(fill=tk.X, padx=10, pady=5)
        
        # Chronomètre, score et nombre de coups
        self.etiquettes["chrono"] = tk.Label(frame_info, text="Temps: 0s")
        self.etiquettes["chrono"].pack(side=tk.LEFT, padx=10)
        
        self.etiquettes["score"] = tk.Label(frame_info, text="Score: 0")
        self.etiquettes["score"].pack(side=tk.LEFT, padx=10)
        
        self.etiquettes["coups"] = tk.Label(frame_info, text="Coups: 0")
        self.etiquettes["coups"].pack(side=tk.LEFT, padx=10)
        
       
    def afficher_tout(self, jeu):
        """
        Met à jour toute l'interface graphique :
        - Affiche les disques empilés sur chaque tour
        - Met à jour le chrono, score, quiz et autres infos

        Args:
            jeu (JeuHanoi): L'état actuel du jeu (tours, disques, chrono...).
        """
        self.canvas.delete("all")
        
        # Dessiner les bases des tours
        largeur_base = 200
        hauteur_base = 20
        espacement = 250
        
        for i in range(3):
            x_base = 150 + i * espacement
            y_base = 350
            
            # Base horizontale
            self.canvas.create_rectangle(x_base - largeur_base/2, y_base, 
                                        x_base + largeur_base/2, y_base + hauteur_base, 
                                        fill="brown")
            
            # Tige verticale
            self.canvas.create_rectangle(x_base - 5, 100, x_base + 5, y_base, fill="brown")
            
            # Numéro de la tour
            self.canvas.create_text(x_base, y_base + 30, text=f"Tour {i+1}", font=("Arial", 12))
            
            # Ajouter un contour si la tour est sélectionnée
            if self.tour_selectionnee == i:
                self.canvas.create_rectangle(
                    x_base - largeur_base/2 - 5, 100 - 5,
                    x_base + largeur_base/2 + 5, y_base + hauteur_base + 5,
                    outline="black", width=3
                )
        
        # Dessiner les disques
        for i, tour in enumerate(jeu.tours):
            x_centre = 150 + i * espacement
            y_base = 350
            
            for j, disque in enumerate(tour.disques):
                # Calculer la largeur du disque proportionnellement à sa taille
                largeur_disque = 30 + disque.taille * 20
                
                # Position verticale (empilé du bas vers le haut)
                y_pos = y_base - (j + 1) * 20
                
                self.canvas.create_rectangle(
                    x_centre - largeur_disque/2, y_pos,
                    x_centre + largeur_disque/2, y_pos + 15,
                    fill=disque.couleur, outline="black"
                )
                
                # Ne pas afficher la taille du disque (supprimé selon les instructions)
        
        # Mettre à jour les informations
        self.etiquettes["chrono"].config(text=f"Temps: {int(jeu.chrono)}s")
        self.etiquettes["score"].config(text=f"Score: {jeu.score}")
        self.etiquettes["coups"].config(text=f"Coups: {jeu.nbr_coups}")

    def afficher_quiz(self, question):
        """
        Affiche une question de quiz.

        Args:
            question (str): Texte de la question.
        """

        q =  f'Où se trouve la tour : {question}?'
        question1 = askstring('...Question...', q)
        
        self.champs_texte["reponse_quiz"] = question1 

        self.boutons['valider_quiz']= self.controleur.gerer_reponse_quiz(self.champs_texte["reponse_quiz"])


    def mettre_a_jour_interface(self, jeu):
        """
        Met à jour l'ensemble de l'affichage en fonction de l'état du jeu.

        Args:
            jeu (JeuHanoi): L'objet représentant la partie en cours.
        """
        self.afficher_tout(jeu)
        
    def gerer_clic(self, event):
        """
        Gère le clic de l'utilisateur sur le canvas et identifie la tour sélectionnée.

        Args:
            event (tkinter.Event): Objet événement contenant les coordonnées du clic.
        """
        x, y = event.x, event.y
        
        # Déterminer quelle tour a été cliquée
        espacement = 250
        for i in range(3):
            x_centre = 150 + i * espacement
            if x_centre - 100 <= x <= x_centre + 100 and y <= 350:
                self.tour_selectionnee = i
                self.controleur.traiter_clic_tour(i)
                self.afficher_tout(self.controleur.jeuhanoi)
                break

    def update_chrono(self):
        """Met à jour le chronomètre toutes les 100ms"""
        
        if self.controleur.jeuhanoi.etat_partie:
            temps_ecoule = time.time() - self.controleur.jeuhanoi.temps_debut
            self.controleur.jeuhanoi.chrono = temps_ecoule 
            self.etiquettes["chrono"].config(text=f"Temps: {int(temps_ecoule)}s")
        self.fenetre.after(100, self.update_chrono)  # Rappel toutes les 100ms

