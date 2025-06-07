# Les Tours de Hanoi

Ce projet propose une version interactive et éducative du célèbre jeu des Tours de Hanoï, avec une interface graphique en Python (Tkinter) et un système de quiz pour enrichir l’expérience de jeu.

# Fonctionnalités 
### Modes de jeu variés 
Le jeu offre plusieurs manières de joeur et d'apprendre:
-	**Mode manuel**: Déplacez les disques vous-même en respectant les règles du jeu.
-	**Mode aléatoire** : Commencez avec une disposition illégale des disques pour plus de défi.
  (disposition illégale = répartition aléatoire qui ne respecte pas les règles du jeu)
-	**Résolution automatique** : Laissez l’algorithme résoudre le jeu pour vous.

### Assistance
-	**Aide**: Recevez un indice sur le prochain mouvement optimal.

### Quiz interactif
-	**Quiz**: Après avoir placé un bon disque sur la troisième tour, répondez à des questions de culture générale pour gagner des bonus ou subir des malus de temps.

### Interface
-	**Interface graphique**: Visualisez les tours, les disques, le score, le chrono et interagissez facilement.

# Dépendances
- Python 3.7 ou supérieur
- Tkinter 

# Structure des fichiers
- `programme_principal.py` : Point d’entrée du programme.
- `Controleur.py` : Gère la logique du jeu et la communication entre la vue et le modèle.
- `Vue.py` : Interface graphique (Tkinter).
- `JeuHanoi.py` : Logique du jeu des tours de Hanoï.
- `Tour.py` : Classe représentant une tour.
- `Disque.py` : Classe représentant un disque.
- `Quiz.py` : Gestionnaire des questions de quiz.
- `dico_quizz_tour.csv` : Fichier CSV contenant les questions/réponses du quiz.


# Installation et lancement

1. Téléchargez le dépôt sur votre ordinateur.
2. **Placez-vous dans le dossier du projet** (là où se trouve `programme_principal.py`).
3. **Assurez-vous que le fichier `dico_quizz_tour.csv`** (questions du quiz) est bien présent dans le même dossier.
5. **Lancez le jeu** : python programme_principal.py


# Règles du jeu
- **Objectif** : Déplacer tous les disques de la première tour à la troisième, un par un.
- **État final** : Tous les disques doivent être sur la tour d'arrivée, parfaitement empilés du plus grand (à la base) au plus petit (au sommet).
-  **Contraintes**
   * One ne peut déplacer qu'un seul disque à la fois
   * Un dsique ne peut pas être placé sur un disque plus petit que lui.
- Essayez de résoudre le puzzle en un minimum de coups et de temps !
  
## Auteurs
Projet réalisé dans le cadre du cours d’ISN (Informatique et Sciences du Numérique).

