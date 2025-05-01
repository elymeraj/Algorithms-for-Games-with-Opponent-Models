from Jeu.JeuInformationComplete import JeuInformationComplete

class Morpion(JeuInformationComplete):
    def __init__(self):
        super().__init__()
        self.plateau = [[' ' for _ in range(3)] for _ in range(3)]
        self.joueur_actuel = 'X'

    def est_termine(self):
        """Vérifie si le jeu est terminé."""
        # vérifie les lignes
        for ligne in self.plateau:
            if ligne.count(ligne[0]) == 3 and ligne[0] != ' ':
                return True
        # vérifie ls colonnes
        for col in range(3):
            if self.plateau[0][col] == self.plateau[1][col] == self.plateau[2][col] and self.plateau[0][col] != ' ':
                return True
        # vérifie les diagonales
        if self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] and self.plateau[0][0] != ' ':
            return True
        if self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] and self.plateau[0][2] != ' ':
            return True
        # s'il reste des cases vides
        return not any(' ' in ligne for ligne in self.plateau)

    def coups_possibles(self):
        res = [(i, j) for i in range(3) for j in range(3) if self.plateau[i][j] == ' ']
        return res

    def jouer(self, coup):
        i, j = coup
        if self.plateau[i][j] == ' ':
            self.plateau[i][j] = self.joueur_actuel
            self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'

    def evaluation(self):
        if self.est_termine():
            if self.qui_gagne() == 'O':
                return -10  # Victoire de l'adversaire
            else:
                return 10  # Victoire de l'algorithme
        
        score = 0
        poids = {1: 1, 2: 3, 3: 10} 

        # Avantage pour des lignes presque remplies
        for ligne in self.plateau:
            x_count = ligne.count('X')
            o_count = ligne.count('O')
            if o_count == 0 and x_count > 0: 
                score += poids[x_count]
            elif x_count == 0 and o_count > 0:
                score -= poids[o_count]

        # Avantage pour colonnes
        for col in range(len(self.plateau[0])):
            colonne = [self.plateau[row][col] for row in range(len(self.plateau))]
            x_count = colonne.count('X')
            o_count = colonne.count('O')
            if o_count == 0 and x_count > 0: 
                score += poids[x_count]
            elif x_count == 0 and o_count > 0: 
                score -= poids[o_count]

        # Avantage pour diagonales
        diagonale1 = [self.plateau[i][i] for i in range(len(self.plateau))]
        diagonale2 = [self.plateau[i][len(self.plateau) - 1 - i] for i in range(len(self.plateau))]
        for diagonale in [diagonale1, diagonale2]:
            x_count = diagonale.count('X')
            o_count = diagonale.count('O')
            if o_count == 0 and x_count > 0: 
                score += poids[x_count]
            elif x_count == 0 and o_count > 0:
                score -= poids[o_count]

        # Bonus pour la case centrale 
        if len(self.plateau) % 2 == 1:
            centre = self.plateau[len(self.plateau) // 2][len(self.plateau) // 2]
            if centre == 'X':
                score += 2 
            elif centre == 'O':
                score -= 2  
        return score

    def qui_gagne(self):
        """Détermine le gagnant."""
        # Vérifie les lignes
        for ligne in self.plateau:
            if ligne.count(ligne[0]) == 3 and ligne[0] != ' ':
                return ligne[0]
        # Vérifie les colonnes
        for col in range(3):
            if self.plateau[0][col] == self.plateau[1][col] == self.plateau[2][col] and self.plateau[0][col] != ' ':
                return self.plateau[0][col]
        # Vérifie les diagonales
        if self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] and self.plateau[0][0] != ' ':
            return self.plateau[0][0]
        if self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] and self.plateau[0][2] != ' ':
            return self.plateau[0][2]
        return None

    def afficher_plateau(self):
        for ligne in self.plateau:
            print('|'.join(ligne))
            print('-' * 5)

    def afficher_etat(self):
        self.afficher_plateau()

    def copie(self):
        """Crée une copie indépendante du jeu Morpion."""
        copie_jeu = Morpion()
        copie_jeu.plateau = [ligne[:] for ligne in self.plateau]
        copie_jeu.joueur_actuel = self.joueur_actuel
        return copie_jeu
    
    
    def numero_joueur_actuel(self):
        if self.joueur_actuel == 'X':
            return 1
        else:
            return 2
