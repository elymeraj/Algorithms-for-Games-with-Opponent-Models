from Joueur.Joueur import Joueur
import random

class JoueurAdversaire(Joueur):
    """
    Classe qui adapte les adversaires existants au nouveau système de joueurs.
    """
    def __init__(self, modele_adversaire):
        super().__init__()
        self.modele = modele_adversaire

    def choisir_coup(self, jeu):
        """
        Utilise le modèle d'adversaire pour choisir un coup.
        """
        distribution = self.modele.choisir_coup(jeu)
        if not distribution:
            return None

        # Pour un adversaire aléatoire, on pioche selon la distribution
        if self.modele.aleatoire:
            coups = list(distribution.keys())
            return random.choice(coups)
        else:
            # Sinon, on prend le coup à probabilité 1
            return max(distribution, key=distribution.get)

    def informer_coup_adversaire(self, jeu, coup):
        # L'adversaire ne se met pas à jour
        pass

