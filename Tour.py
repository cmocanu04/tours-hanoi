class Tour:
    """
    Représente une tour sur laquelle les disques sont empilés.

    Attributs:
        numero (int): Le numéro de la tour (1, 2 ou 3).
        disques (list[Disque]): Liste de disques empilés dans l'ordre.
    """
    def __init__(self, numero):
        self.numero = numero
        self.disques = []

    def est_vide(self):
        """
        Vérifie si la tour est vide.

        Returns:
            bool: True si la tour ne contient aucun disque, sinon False.
        """
        return len(self.disques) == 0



    def empiler(self, disque):
        """
        Ajoute un disque au sommet de la tour.

        Args:
            disque (Disque): Le disque à ajouter.
        """
        self.disques.append(disque)



    def depiler(self):
        """
        Retire et retourne le disque au sommet de la tour.

        Returns:
            Disque: Le disque retiré du sommet.
        """
        if not self.est_vide():
            return self.disques.pop()
        return None



    def top_disque(self):
        """
        Renvoie le disque au sommet de la tour sans le retirer.

        Returns:
            Disque | None: Le disque au sommet, ou None si la tour est vide.
        """
        if not self.est_vide():
            return self.disques[-1]
        return None

