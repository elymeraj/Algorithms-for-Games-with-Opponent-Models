from Adversaire.Adversaire import Adversaire

class AdversaireDernierCoup(Adversaire):
    """Adversaire qui joue toujours le dernier coup possible."""
    
    def __init__(self):
        """Initialise l'adversaire déterministe."""
        super().__init__(aleatoire=False)
    
    def choisir_coup(self, jeu):
        """
        Retourne une distribution avec probabilité 1 pour le dernier coup.
        
        Args:
            jeu: L'état actuel du jeu
            
        Returns:
            Dictionnaire {coup: probabilité} ou None si aucun coup possible
        """
        coups = jeu.coups_possibles()
        if not coups and hasattr(jeu, 'piocher'):
            jeu.piocher()
        if not coups:
            return None
        return self.distribution_probabilites(coups)
    
    def distribution_probabilites(self, coups):
        """
        Crée une distribution avec probabilité 1 pour le dernier coup.
        
        Args:
            coups: Liste des coups possibles
            
        Returns:
            Dictionnaire {coup: probabilité}
        """
        res = {}
        for i, coup in enumerate(coups):
            res[coup] = 1.0 if i == len(coups) - 1 else 0.0
        return res