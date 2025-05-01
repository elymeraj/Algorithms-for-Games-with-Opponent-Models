class Joueur:
    """Classe abstraite représentant un joueur."""
    
    def __init__(self):
        self.modeles_credibles = []  #liste des modeles d'adversaires considérés comme credibles
    
    def choisir_coup(self, jeu):
        """Choisit le prochain coup à jouer."""
        raise NotImplementedError
    
    def informer_coup_adversaire(self, jeu, coup):
        """
        Méthode pour informer le joueur du coup joué par l'adversaire.
        Permet de mettre à jour les modèles d'adversaires crédibles.
        """
        raise NotImplementedError