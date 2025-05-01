class Adversaire:
    
    def __init__(self, aleatoire=False):
        self.aleatoire = aleatoire
    
    def distribution_probabilites(coups):
        raise NotImplementedError
    
    def choisir_coup(self, jeu):
        raise NotImplementedError
    