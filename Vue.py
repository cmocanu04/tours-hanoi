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
        self.fenetre.geometry("1000x800")

        
        
        self.etiquettes = {}
        self.boutons = {}
        self.champs_texte = {}
        self.champs_chrono = None
        self.champs_quiz = None
        self.tour_selectionnee = None
        
        self.canvas = tk.Canvas(self.fenetre, width=1000, height=600, bg="lightgray")
        self.canvas.pack(pady=20)
        
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
        frame_controles = tk.Frame(self.fenetre)
        frame_controles.pack(fill=tk.X, padx=10, pady=10)
        frame_controles.pack_propagate(False)
        frame_controles.configure(height=50)
        
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

        # Bouton Quitter
        self.boutons["quitter"] = tk.Button(frame_controles, text="Quitter", command=self.fenetre.destroy)
        self.boutons["quitter"].pack(side=tk.RIGHT, padx=20)

        

        # Nombre de disques
        tk.Label(frame_controles, text="Nombre de disques:").pack(side=tk.LEFT, padx=5)
        
        self.var_nb_disques = tk.IntVar(value=3)
        
        disques_spinbox = tk.Spinbox(frame_controles, from_=3, to=8, width=2, 
                                     textvariable=self.var_nb_disques,
                                     command=lambda: self.controleur.config_nbr_disque(self.var_nb_disques.get()))
        disques_spinbox.pack(side=tk.LEFT)
        
        # Frame pour les informations
        frame_info = tk.Frame(self.fenetre)
        frame_info.pack(fill=tk.X, padx=10, pady=10)
        frame_info.pack_propagate(False)
        frame_info.configure(height=50)
        
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
        
        # Centrage et dimensions adaptés
        largeur_base = 250
        hauteur_base = 30
        espacement = 320
        x_depart = 180
        y_base = 550
        y_haut_tige = 240
        for i in range(3):
            x_base = x_depart + i * espacement
            # Base horizontale
            self.canvas.create_rectangle(x_base - largeur_base/2, y_base, 
                                        x_base + largeur_base/2, y_base + hauteur_base, 
                                        fill="brown")
            # Tige verticale
            self.canvas.create_rectangle(x_base - 7, y_haut_tige, x_base + 7, y_base, fill="brown")
            # Numéro de la tour
            self.canvas.create_text(x_base, y_base + 40, text=f"Tour {i+1}", font=("Arial", 16))
            # Ajouter un contour si la tour est sélectionnée
            if self.tour_selectionnee == i:
                self.canvas.create_rectangle(
                    x_base - largeur_base/2 - 7, y_haut_tige - 7,
                    x_base + largeur_base/2 + 7, y_base + hauteur_base + 7,
                    outline="black", width=4
                )
        
        # Dessiner les disques
        for i, tour in enumerate(jeu.tours):
            x_centre = x_depart + i * espacement
            for j, disque in enumerate(tour.disques):
                largeur_disque = 28 + disque.taille * 25
                epaisseur_disque = 24  # plus épais
                y_pos = y_base - (j + 1) * (epaisseur_disque + 2)
                self.canvas.create_rectangle(
                    x_centre - largeur_disque/2, y_pos,
                    x_centre + largeur_disque/2, y_pos + epaisseur_disque,
                    fill=disque.couleur, outline="black"
                )
        
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
        espacement = 320
        x_depart = 180
        for i in range(3):
            x_centre = x_depart + i * espacement
            if x_centre - 125 <= x <= x_centre + 125 and y <= 550:
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

