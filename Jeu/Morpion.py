from Jeu.JeuInformationComplete import JeuInformationComplete

class Morpion(JeuInformationComplete):
    def __init__(self):
        super().__init__()
        self.plateau = [[' ' for _ in range(3)] for _ in range(3)]
        self.joueur_actuel = 'X'  #X commence toujours

    def est_termine(self):
        """Vérifie si le jeu est terminé (victoire ou match nul)."""
        #vérifier s'il y a un gagnant
        if self.qui_gagne() is not None:
            return True
            
        #vérifier s'il reste des cases vides
        return all(all(case != ' ' for case in ligne) for ligne in self.plateau)

    def coups_possibles(self):
        """Retourne toutes les positions vides où un joueur peut jouer."""
        return [(i, j) for i in range(3) for j in range(3) if self.plateau[i][j] == ' ']

    def jouer(self, coup):
        """Joue un coup et passe au joueur suivant."""
        i, j = coup
        if self.plateau[i][j] == ' ':
            self.plateau[i][j] = self.joueur_actuel
            self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'

    def jeu_termine_score(self):
        """
        Retourne le score de fin de partie:
        10 pour une victoire de X (joueur 1)
        -10 pour une victoire de O (joueur 2)
        0 pour un match nul
        """
        gagnant = self.qui_gagne()
        if gagnant == 'X':
            return 10
        elif gagnant == 'O':
            return -10
        return 0  

    def evaluation(self):
        """
        Évalue la position actuelle du jeu.
        Une évaluation positive favorise X (joueur 1), négative favorise O (joueur 2).
        """
        # Vérifier d'abord si la partie est terminée
        gagnant = self.qui_gagne()
        if gagnant == 'X':
            return 10
        elif gagnant == 'O':
            return -10
            
        score = 0
        poids = {1: 1, 2: 3}  # point pour 1 ou 2 symboles alignés
        
        #évaluer les lignes
        for ligne in self.plateau:
            x_count = ligne.count('X')
            o_count = ligne.count('O')
            
            # des alignements qui sont non bloqués sont favorisés
            if o_count == 0 and x_count > 0:
                score += poids.get(x_count, 0)
            elif x_count == 0 and o_count > 0:
                score -= poids.get(o_count, 0)

        #evaluer les colonnes
        for col in range(3):
            colonne = [self.plateau[row][col] for row in range(3)]
            x_count = colonne.count('X')
            o_count = colonne.count('O')
            
            if o_count == 0 and x_count > 0:
                score += poids.get(x_count, 0)
            elif x_count == 0 and o_count > 0:
                score -= poids.get(o_count, 0)

        #evaluer les diagonales
        diagonale1 = [self.plateau[i][i] for i in range(3)]
        diagonale2 = [self.plateau[i][2-i] for i in range(3)]
        
        for diagonale in [diagonale1, diagonale2]:
            x_count = diagonale.count('X')
            o_count = diagonale.count('O')
            
            if o_count == 0 and x_count > 0:
                score += poids.get(x_count, 0)
            elif x_count == 0 and o_count > 0:
                score -= poids.get(o_count, 0)

        #bonus pourle centre
        if self.plateau[1][1] == 'X':
            score += 3
        elif self.plateau[1][1] == 'O':
            score -= 3
            
        #bonus poru les coins
        coins = [(0,0), (0,2), (2,0), (2,2)]
        for i, j in coins:
            if self.plateau[i][j] == 'X':
                score += 2
            elif self.plateau[i][j] == 'O':
                score -= 2

        return score

    def qui_gagne(self):
        """
        Détermine le gagnant ('X', 'O' ou None si pas de gagnant).
        """
        # Vérifier les lignes
        for ligne in self.plateau:
            if ligne[0] == ligne[1] == ligne[2] and ligne[0] != ' ':
                return ligne[0]
                
        # Vérifier les colonnes
        for col in range(3):
            if self.plateau[0][col] == self.plateau[1][col] == self.plateau[2][col] and self.plateau[0][col] != ' ':
                return self.plateau[0][col]
                
        # vérifier les diagonales
        if self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] and self.plateau[0][0] != ' ':
            return self.plateau[0][0]
        if self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] and self.plateau[0][2] != ' ':
            return self.plateau[0][2]
            
        # Pas de gagnant
        return None

    def afficher_plateau(self):
        """Affiche le plateau de jeu."""
        print("\n  0 1 2")
        for i, ligne in enumerate(self.plateau):
            print(f"{i} {' '.join(ligne)}")
        print()

    def afficher_etat(self):
        """Affiche l'état actuel du jeu."""
        self.afficher_plateau()
        print(f"Tour du joueur : {self.joueur_actuel}")

    def copie(self):
        """Crée une copie indépendante du jeu Morpion."""
        nouveau_jeu = Morpion.__new__(Morpion)
        
        nouveau_jeu.plateau = [ligne[:] for ligne in self.plateau]
        nouveau_jeu.joueur_actuel = self.joueur_actuel
        
        return nouveau_jeu
    
    def numero_joueur_actuel(self):
        """Retourne le numéro du joueur actuel (1 pour X, 2 pour O)."""
        return 1 if self.joueur_actuel == 'X' else 2