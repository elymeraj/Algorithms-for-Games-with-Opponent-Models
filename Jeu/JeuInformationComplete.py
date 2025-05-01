from Jeu.Jeu import Jeu

class JeuInformationComplete(Jeu):
    def __init__(self):
        super().__init__()

    def afficher_plateau(self):
        raise NotImplementedError
