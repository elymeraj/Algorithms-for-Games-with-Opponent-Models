from Joueur.Joueur import Joueur
from Adversaire.AdversaireRandom import AdversaireRandom


class JoueurMinMax(Joueur):
    def __init__(self, profondeur=3):
        super().__init__()
        self.profondeur = profondeur
        self.modeles_credibles = []  # Liste des modèles d'adversaires considérés comme crédibles
    
    def choisir_coup(self, jeu):
        """
        MinMax avec plusieurs modèles d'adversaires, l'approche Max-Min-Expectimax.
        """
        coups = jeu.coups_possibles()
        if not coups:
            return None

        meilleur_coup = None
        meilleure_eval = float('-inf')

        for coup in coups:
            copie_jeu = jeu.copie()
            copie_jeu.jouer(coup)
            
            #pour chaque modele d'adversaire credible, calculer l'évaluationminimale
            eval_min = float('inf')
            for modele in self.modeles_credibles:
                eval = self._minimax(copie_jeu, self.profondeur - 1, False, modele)
                eval_min = min(eval_min, eval)
            
            if eval_min > meilleure_eval:
                meilleure_eval = eval_min
                meilleur_coup = coup

        return meilleur_coup

    def _minimax(self, jeu, profondeur, maximisant, modele_adversaire):
        if jeu.est_termine() or profondeur == 0:
            return jeu.evaluation()

        coups = jeu.coups_possibles()
        if not coups:
            return jeu.evaluation()

        if maximisant: # on a le meme probleme ici comme en minmax2, la meme correction
            meilleure_eval = float('-inf')
            for coup in coups:
                copie_jeu = jeu.copie()
                copie_jeu.jouer(coup)
                eval = self._minimax(copie_jeu, profondeur - 1, False, modele_adversaire)
                meilleure_eval = max(meilleure_eval, eval)
            return meilleure_eval
        else:
            distribution_proba = modele_adversaire.choisir_coup(jeu)
            if not distribution_proba:
                return jeu.evaluation()

            if modele_adversaire.aleatoire:
                # Expectimax
                evaluation_ponderee = 0
                total_proba = sum(distribution_proba.values())

                for coup, proba in distribution_proba.items():
                    if proba > 0:
                        copie_jeu = jeu.copie()
                        copie_jeu.jouer(coup)
                        eval = self._minimax(copie_jeu, profondeur - 1, True, modele_adversaire)
                        evaluation_ponderee += (proba / total_proba) * eval
                
                return evaluation_ponderee
            else:
                #le MinMax classique pour les modeles déterministes
                coup_predit = max(distribution_proba, key=distribution_proba.get)
                copie_jeu = jeu.copie()
                copie_jeu.jouer(coup_predit)
                return self._minimax(copie_jeu, profondeur - 1, True, modele_adversaire)

    def informer_coup_adversaire(self, jeu, coup):
        """
        met à jour la liste des modeles credibles en fonction du coup joué par l'adversaire
        """
        modeles_a_eliminer = []
        for modele in self.modeles_credibles:
            distribution = modele.choisir_coup(jeu)
            if not distribution:
                continue  #aucun coup possible pour ce modèle, on ne l'élimine pas 
            if coup not in distribution or distribution[coup] == 0:
                modeles_a_eliminer.append(modele)

        for modele in modeles_a_eliminer:
            self.modeles_credibles.remove(modele)
            print(f"Modèle {modele.__class__.__name__} éliminé car incompatible avec le coup {coup}")
            

