from Joueur.Joueur import Joueur
from Adversaire.AdversaireRandom import AdversaireRandom


class JoueurMinMax2(Joueur):
    def __init__(self, profondeur=3):
        super().__init__()
        self.profondeur = profondeur
        self.modeles_credibles = []  #liste des modèles d'adversaires consideres comme crédibles
    
    def choisir_coup(self, jeu):
        """
        MinMax avec plusieurs modèles d'adversaires, approche réaliste qui considère
        les modèles adverses compatibles avec chaque coup possible
        """
        coups = jeu.coups_possibles()
        if not coups and hasattr(jeu, 'piocher'):
            jeu.piocher()
        if not coups:
            return None

        meilleur_coup = None
        meilleure_eval = float('-inf')

        for coup in coups:
            #onn copie le jeu pour simuler le coup
            copie_jeu = jeu.copie()
            copie_jeu.jouer(coup)
            
            #on évalue le jeu après le coup joué
            eval_min = self._minimax(copie_jeu, self.profondeur-1, False, self.modeles_credibles)
            if eval_min > meilleure_eval:
                meilleure_eval = eval_min
                meilleur_coup = coup

        return meilleur_coup

    def _minimax(self, jeu, profondeur, maximisant, modeles_credibles):
        """
        MinMax récursif avec prise en compte de plusieurs modèles d'adversaires.

        :param modeles_credibles: Liste des modèles crédibles à ce niveau.
        """
        if jeu.est_termine():
            return jeu.jeu_termine_score()
            
        if profondeur == 0:
            return jeu.evaluation()

        if maximisant:
            coups = jeu.coups_possibles()
            if not coups and hasattr(jeu, 'piocher'):
                jeu.piocher()
            if not coups:
                return jeu.evaluation()  # Plus de coups possibles

            meilleure_eval = float('-inf')
            for coup in coups:
                # On copie le jeu pour simuler le coup
                copie_jeu = jeu.copie()
                copie_jeu.jouer(coup)

                # On évalue le jeu après le coup joué
                eval_min = self._minimax(copie_jeu, profondeur-1, False, modeles_credibles)
                meilleure_eval = max(meilleure_eval, eval_min)

            return meilleure_eval

        else:
            #pour chaque coup possible selon les modèles crédibles,
            #on ne considère que les modèles pour lesquels ce coup est probable
            tous_les_coups = set()
            for modele_adversaire in modeles_credibles:
                distribution = modele_adversaire.choisir_coup(jeu)
                if distribution:
                    tous_les_coups.update(distribution.keys()) 
            
            if not tous_les_coups:
                return jeu.evaluation()  #aucun coup possible pour les modèles crédibles
                
            eval_min = float('inf')
            for coup in tous_les_coups:
                #on ne considère que les modèles qui auraient pu jouer ce coup
                sous_modeles = []
                for modele in modeles_credibles:
                    distribution = modele.choisir_coup(jeu)
                    if distribution and coup in distribution and distribution[coup] > 0:
                        sous_modeles.append(modele)
                
                if not sous_modeles:
                    continue  #aucun modèle ne prédit ce coup, on passe au suivant
                
                copie_jeu = jeu.copie()
                copie_jeu.jouer(coup)

                eval = self._minimax(copie_jeu, profondeur-1, True, sous_modeles)
                eval_min = min(eval_min, eval)

            #si aucun coup n'a pu etre evalue on renvoie l'évaluation actuelle
            if eval_min == float('inf'):
                return jeu.evaluation()
                
            return eval_min

    def informer_coup_adversaire(self, jeu, coup):
        """
        Met à jour la liste des modèles crédibles en fonction du coup joué par l'adversaire
        """
        modeles_a_eliminer = []
        for modele in self.modeles_credibles:
            distribution = modele.choisir_coup(jeu)
            if not distribution:
                continue  #aucun coup possible pour ce modèle donc on ne l'élimine pas 
            if coup not in distribution or distribution[coup] == 0:
                modeles_a_eliminer.append(modele)

        for modele in modeles_a_eliminer:
            self.modeles_credibles.remove(modele)
            print(f"Modèle {modele.__class__.__name__} éliminé car incompatible avec le coup {coup}")
            
        #s'assurer qu'il reste au moins un modèle crédible
        if not self.modeles_credibles:
            raise RuntimeError("Plus aucun modèle crédible après le coup adverse : comportement inattendu de l'adversaire")


