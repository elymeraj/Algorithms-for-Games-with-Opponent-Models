from Adversaire.Adversaire import Adversaire

class AdversairePremierCoup(Adversaire):
    
    def __init__(self):
        super().__init__(aleatoire = False)
    
    def choisir_coup(self, jeu):
        coups = jeu.coups_possibles()
        if not coups:
            return None
        res = self.distribution_probabilites(coups)
        return res
    
    def distribution_probabilites(self, coups):
        res = {}
        for x in range(len(coups)):
            if x == 0:
                res[coups[x]] = 1.0
            else:
                res[coups[x]] = 0.0
        return res
