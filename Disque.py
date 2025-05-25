import random



class Disque:
    """
    Représente un disque du jeu.

    Attributs:
        taille (int): Le diamètre du disque.
        couleur (str): La couleur utilisée pour représenter graphiquement le disque.
    """
    def __init__(self, taille, couleur=None):
        #random.seed(taille+10)

        self.taille = taille
        # Générer une couleur aléatoire si aucune n'est fournie
        self.couleur = couleur or "#{:06x}".format(random.randint(0, 0xFFFFFF))

