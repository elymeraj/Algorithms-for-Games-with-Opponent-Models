from Jeu.Jeu import Jeu

class JeuInformationIncomplete(Jeu):
    def __init__(self):
        super().__init__()

    def informations_incompletes(self):
        """
        Retourne les informations partielles disponibles pour les joueurs.
        """
        raise NotImplementedError
