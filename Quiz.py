import random 

import csv

class Quiz:
    """
    Gère les questions de quiz liées au jeu.

    Attributs:
        dico_quiz (dict[str, str]): Questions et réponses du quiz.
    """
    def __init__(self):
        self.dico_quiz = {}
        self.question_actuelle = None
        self.reponse_attendue = None

    def charger_questions_csv(self, fichier_csv):
        """
        Charge les questions depuis un fichier CSV.

        Args:
            fichier_csv (str): Chemin vers le fichier CSV.
        """
        with open(fichier_csv, 'r', encoding='utf-8') as fichier:
            lecteur = csv.reader(fichier)
            lecteur.__next__()

            for ligne in lecteur:
                if len(ligne) >= 2:
                    question, reponse = ligne[0], ligne[1]
                    self.dico_quiz[question] = reponse
        
        
    def poser_question(self):
        """
        Sélectionne et retourne une question aléatoire.

        Returns:
            tuple[str, str]: (question, reponse_attendue)
        """
        if not self.dico_quiz:
            return "Aucune question disponible", ""
            
        self.question_actuelle = random.choice(list(self.dico_quiz.keys()))
        self.reponse_attendue = self.dico_quiz[self.question_actuelle]
        
        return self.question_actuelle, self.reponse_attendue
        


    def verifier_reponse(self, reponse_joueur):
        """
        Vérifie si la réponse du joueur est correcte (sans majuscule, accent, etc.).

        Args:
            reponse_joueur (str): Réponse donnée par le joueur.

        Returns:
            bool: True si la réponse est correcte, sinon False.
        """

        if not self.reponse_attendue:
            return False
        elif reponse_joueur==None:
            return False
            
        # Normaliser les réponses pour la comparaison
        reponse_joueur_norm = reponse_joueur.lower().strip()
        reponse_attendue_norm = self.reponse_attendue.lower().strip()
        
        return reponse_joueur_norm == reponse_attendue_norm
        

    def attribuer_bonus_temps(self):
        """
        Calcule le bonus de temps en cas de bonne réponse.

        Returns:
            int: Temps à retirer (en secondes).
        """
        return 10  # 10 secondes de bonus
        

        
    def attribuer_malus_temps(self):
        """
        Calcule le malus de temps en cas de mauvaise réponse.

        Returns:
            int: Temps à ajouter (en secondes).
        """
        return 5  # 5 secondes de malus

