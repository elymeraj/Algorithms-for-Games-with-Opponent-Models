from Adversaire.Adversaire import Adversaire

class AdversaireDominoFort(Adversaire):
    """
    Adversaire qui joue systématiquement la pièce la plus grande de sa main.
    """
    
    def __init__(self):
        super().__init__(aleatoire=False)
    
    def choisir_coup(self, jeu):
        coups = jeu.coups_possibles()
        if not coups and hasattr(jeu, 'piocher'):
            jeu.piocher()        
        if not coups:
            return None
        
        res = {}
        # Trouver le domino avec la plus grande somme
        meilleur_coup = max(coups, key=lambda x: x[0] + x[1])
        
        # Distribution déterministe : probabilité 1 pour le meilleur coup
        for coup in coups:
            if coup == meilleur_coup:
                res[coup] = 1.0
            else:
                res[coup] = 0.0
                
        return res

