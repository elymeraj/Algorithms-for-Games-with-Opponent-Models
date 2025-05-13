from Adversaire.Adversaire import Adversaire
import random

class AdversaireRandom(Adversaire):
    
    def __init__(self):
        super().__init__(aleatoire = True)
    
    def choisir_coup(self, jeu):
        coups_possibles = jeu.coups_possibles()
        if not coups_possibles and hasattr(jeu, 'piocher'):
            jeu.piocher()
        if not coups_possibles:
            print("L'adversaire ne peut pas jouer.")
            return None
        res = self.distribution_probabilites(coups_possibles)
        return res
    
    def distribution_probabilites(self, coups):
        res = {}
        for coup in coups:
            res[coup] = 1.0 / len(coups)
        return res
