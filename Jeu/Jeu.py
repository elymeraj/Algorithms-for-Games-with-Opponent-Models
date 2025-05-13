class Jeu:
    """Classe abstraite représentant un jeu."""
    
    def __init__(self):
        self.joueur_actuel = None
    
    def est_termine(self):
        """Vérifie si le jeu est terminé."""
        raise NotImplementedError

    def coups_possibles(self):
        """Retourne la liste des coups possibles."""
        raise NotImplementedError

    def jouer(self, coup):
        """Joue un coup et met à jour l'état du jeu."""
        raise NotImplementedError

    def evaluation(self):
        """Évalue la position actuelle du jeu."""
        raise NotImplementedError
        
    def copie(self):
        """Crée une copie indépendante du jeu."""
        raise NotImplementedError
        
    def afficher_etat(self):
        """Affiche l'état actuel du jeu."""
        raise NotImplementedError
        
    def joueur_suivant(self):
        """Passe au joueur suivant."""
        raise NotImplementedError

    def jeu_termine_score(self):
        """Retourne le score de fin de partie."""
        raise NotImplementedError