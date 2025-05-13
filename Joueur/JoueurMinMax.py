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
        if not coups and hasattr(jeu, 'piocher'):
            jeu.piocher()
        if not coups:
            return None

        meilleur_coup = None
        meilleure_eval = float('-inf')

        for coup in coups:
            copie_jeu = jeu.copie()
            copie_jeu.jouer(coup)
            
            # Pour chaque modèle d'adversaire crédible, calculer l'évaluation minimale
            eval_min = float('inf')
            for modele in self.modeles_credibles:
                eval = self._minimax(copie_jeu, self.profondeur - 1, False, modele)
                eval_min = min(eval_min, eval)
            
            if eval_min > meilleure_eval:
                meilleure_eval = eval_min
                meilleur_coup = coup

        return meilleur_coup

    def _minimax(self, jeu, profondeur, maximisant, modele_adversaire):
        # Vérification de fin de jeu
        if jeu.est_termine():
            return jeu.jeu_termine_score()
        
        if profondeur == 0:
            return jeu.evaluation()

        coups = jeu.coups_possibles()
        if not coups and hasattr(jeu, 'piocher'):
            jeu.piocher()
        if not coups:
            return jeu.evaluation()

        if maximisant:
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
                
                if total_proba <= 0:
                    return jeu.evaluation()

                for coup, proba in distribution_proba.items():
                    if proba > 0:
                        copie_jeu = jeu.copie()
                        copie_jeu.jouer(coup)
                        eval = self._minimax(copie_jeu, profondeur - 1, True, modele_adversaire)
                        evaluation_ponderee += (proba / total_proba) * eval
                
                return evaluation_ponderee
            else:
                coup_predit = max(distribution_proba, key=distribution_proba.get)
                copie_jeu = jeu.copie()
                copie_jeu.jouer(coup_predit)
                return self._minimax(copie_jeu, profondeur - 1, True, modele_adversaire)

    def informer_coup_adversaire(self, jeu, coup):
        """
        Met à jour la liste des modèles crédibles en fonction du coup joué par l'adversaire
        """
        modeles_a_eliminer = []
        for modele in self.modeles_credibles:
            distribution = modele.choisir_coup(jeu)
            if not distribution:
                continue
            if coup not in distribution or distribution[coup] == 0:
                modeles_a_eliminer.append(modele)

        for modele in modeles_a_eliminer:
            self.modeles_credibles.remove(modele)
            print(f"Modèle {modele.__class__.__name__} éliminé car incompatible avec le coup {coup}")
            
        # verifier que y'a toutjours au moins un modèle crédible
        if not self.modeles_credibles:
            raise RuntimeError("Plus aucun modèle crédible après le coup adverse : comportement inattendu de l'adversaire")
        