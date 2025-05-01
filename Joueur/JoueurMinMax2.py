from Joueur.Joueur import Joueur
from Adversaire.AdversaireRandom import AdversaireRandom


class JoueurMinMax2(Joueur):
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
            
            tous_les_coups = set()
            for modele in self.modeles_credibles:
                distribution = modele.choisir_coup(jeu)
                if distribution:
                    tous_les_coups.update(distribution.keys())

            meilleure_eval = float('-inf')
            for coup in tous_les_coups: # a editer aussi, ici ya pas de question de mod adversaire, donc ca vient a supprimer plaind de lignes
                sous_modeles = [m for m in self.modeles_credibles if m.choisir_coup(jeu) and coup in m.choisir_coup(jeu)]

                if not sous_modeles:
                    continue

                copie_jeu = jeu.copie()
                copie_jeu.jouer(coup)
            
            
                eval_min = self._minimax(copie_jeu, self.profondeur - 1, False, sous_modeles)
                
                if eval_min > meilleure_eval:
                    meilleure_eval = eval_min
                    meilleur_coup = coup

        return meilleur_coup

    def _minimax(self, jeu, profondeur, maximisant, modeles_credibles):
        """
        MinMax récursif avec prise en compte de plusieurs modèles d'adversaires.

        :param modeles_credibles: Liste des modèles crédibles à ce niveau.
        """
        if jeu.est_termine() or profondeur == 0:
            return jeu.evaluation()

        if maximisant:
            tous_les_coups = set()
            for modele in modeles_credibles:
                distribution = modele.choisir_coup(jeu)
                if distribution:
                    tous_les_coups.update(distribution.keys())

            meilleure_eval = float('-inf')
            for coup in tous_les_coups:
                sous_modeles = [m for m in modeles_credibles if m.choisir_coup(jeu) and coup in m.choisir_coup(jeu)] #il faut decaler cette ligne

                if not sous_modeles:
                    continue

                copie_jeu = jeu.copie()
                copie_jeu.jouer(coup)

                eval = self._minimax(copie_jeu, profondeur - 1, False, sous_modeles)
                meilleure_eval = max(meilleure_eval, eval)

            return meilleure_eval

        else:
            eval_min = float('inf')

            for modele_adversaire in modeles_credibles:
                distribution_proba = modele_adversaire.choisir_coup(jeu)
                if not distribution_proba:
                    continue

                if modele_adversaire.aleatoire:
                    evaluation_ponderee = 0
                    total_proba = sum(distribution_proba.values())

                    for coup, proba in distribution_proba.items(): 
                        if proba > 0:
                            copie_jeu = jeu.copie() # c'est la ou il faut que je calcule les sous-models, notre sous modele apres va servire dans la recursion
                            copie_jeu.jouer(coup)
                            eval = self._minimax(copie_jeu, profondeur - 1, True, modeles_credibles)
                            evaluation_ponderee += (proba / total_proba) * eval

                    eval_min = min(eval_min, evaluation_ponderee)

                else: #si le modele adv n'est pas aleatoire, dans ce cas il faut ecrire ce que le prof ecrit dans la feuille
                    # il fait faire:
                    # else: assert len (distribution_proba) == 1
                    # coup_predit = next(iter(distribution_proba.keys()))
                    coup_predit = max(distribution_proba, key=distribution_proba.get)
                    copie_jeu = jeu.copie() #ecoute l'enrregistrement du prof, donc il y a pkus de sous-modele
                    copie_jeu.jouer(coup_predit)
                    eval = self._minimax(copie_jeu, profondeur - 1, True, modeles_credibles)
                    eval_min = min(eval_min, eval)

            return eval_min if eval_min != float('inf') else jeu.evaluation()

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
            print(f"Modèle {modele.__class__.__name__} éliminé car incompatible avec le coup {coup}")#
            



