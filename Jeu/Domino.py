from Jeu.JeuInformationIncomplete import JeuInformationIncomplete
import random

class Domino(JeuInformationIncomplete):
    def __init__(self):
        super().__init__()
        self.dominoes = [(i, j) for i in range(7) for j in range(i, 7)]  # Toutes les pièces de domino
        random.shuffle(self.dominoes)
        self.main_joueur1 = []
        self.main_joueur2 = []
        self.plateau = []
        self.joueur_actuel = 1
        self.score_joueur1 = 0
        self.score_joueur2 = 0
        self.distribuer_dominos()
        self.determiner_premier_joueur()

    def distribuer_dominos(self):
        """Distribuer 7 dominos à chaque joueur."""
        self.main_joueur1 = self.dominoes[:7]
        self.main_joueur2 = self.dominoes[7:14]
        self.dominoes = self.dominoes[14:]
    
    def coups_possibles(self):
        """Retourner tous les dominos que le joueur actuel peut jouer."""
        main_actuelle = self.main_joueur1 if self.joueur_actuel == 1 else self.main_joueur2

        #vérifeir si les dominos peuvent être joués
        gauche, droite = (self.plateau[0][0], self.plateau[-1][1]) if self.plateau else (None, None)
        coups = [domino for domino in main_actuelle if gauche in domino or droite in domino]

        #pioche un domino si pas de coups possibles
        if not coups and self.dominoes:
            pioche = self.dominoes.pop(0)
            main_actuelle.append(pioche)
            print(f"Joueur {self.joueur_actuel} pioche le domino {pioche}.")
            coups = [domino for domino in main_actuelle if gauche in domino or droite in domino]
            
            # celui qui pioche -10 de score
            if self.joueur_actuel == 1:
                self.score_joueur1 -= 10
            else:
                self.score_joueur2 -= 10

        return coups


    def est_termine(self):
        """Déterminer si le jeu est terminé."""
        if len(self.main_joueur1) == 0 or len(self.main_joueur2) == 0:
            return True

        #si aucun joueur ne peut jouer et la pioche est vide
        joueur1_peut_jouer = any(self.peut_jouer(domino) for domino in self.main_joueur1)
        joueur2_peut_jouer = any(self.peut_jouer(domino) for domino in self.main_joueur2)
        if not joueur1_peut_jouer and not joueur2_peut_jouer and not self.dominoes:
            return True

        return False


    def evaluer_coup(self, coup, a_pioche=False):
        """
        Évalue un coup selon les règles de score définies.
        ####### il faut corriger 
        """
        points = 0
        if a_pioche:
            return -10
            
        #bonus pour jouer un domino
        points += 5
        
        #bonus pour jouer un double
        points += 2 * (coup[0] + coup[1]) #on se debarrase de ca, mais je suis pas sur????????
        
        #si le plateau n'est pas vide, on vérifie les bonus spéciaux
        if self.plateau:
            gauche, droite = self.plateau[0][0], self.plateau[-1][1]
            
            #bonus pour double connexion possible
            if gauche in coup and droite in coup:
                points += 15
            
            #bnus pour extrémités correspondantes (doubles)
            if coup[0] == coup[1] or gauche == droite:
                points += 10
                
            #si ce coup force l'adversaire à piocher
            main_adverse = self.main_joueur2 if self.joueur_actuel == 1 else self.main_joueur1
            nouveau_gauche = coup[0] if gauche in coup else gauche
            nouveau_droite = coup[1] if droite in coup else droite
            coups_possibles_adverse = [d for d in main_adverse if nouveau_gauche in d or nouveau_droite in d]
            
            if not coups_possibles_adverse:
                points += 20
        
        return points

    def calculer_score_final(self):
        """Calcule les scores finaux en tenant compte des pénalités."""
        penalite_j1 = sum(d[0] + d[1] for d in self.main_joueur1)
        penalite_j2 = sum(d[0] + d[1] for d in self.main_joueur2)
        
        self.score_joueur1 -= penalite_j1
        self.score_joueur2 -= penalite_j2

    def jouer(self, coup):
        """Joue un domino sur le plateau et met à jour l'état du jeu."""
        main_actuelle = self.main_joueur1 if self.joueur_actuel == 1 else self.main_joueur2

        if coup not in main_actuelle:
            raise ValueError(f"Le domino {coup} n'est pas dans la main du joueur {self.joueur_actuel}.")

        # evaluer le coup 
        points = self.evaluer_coup(coup)
        if self.joueur_actuel == 1:
            self.score_joueur1 += points
        else:
            self.score_joueur2 += points

        if self.peut_jouer(coup):
            gauche, droite = self.plateau[0][0] if self.plateau else None, self.plateau[-1][1] if self.plateau else None
            if not self.plateau:
                self.plateau.append(coup)
            elif gauche in coup:
                self.plateau.insert(0, coup if gauche == coup[1] else coup[::-1])
            elif droite in coup:
                self.plateau.append(coup if droite == coup[0] else coup[::-1])

            # enlever le domino de la main du joueur
            main_actuelle.remove(coup)

            # si la main est vide (victoire)
            if len(main_actuelle) == 0:
                if self.joueur_actuel == 1:
                    self.score_joueur1 += 30  # Bonus de victoire
                else:
                    self.score_joueur2 += 30  # Bonus de victoire

            # joueur suivant 
            self.joueur_actuel = 2 if self.joueur_actuel == 1 else 1
        else:
            raise ValueError(f"Le domino {coup} ne peut pas être joué.")

    def evaluation(self): # à éditier ici 
        """Évaluation améliorée de l'état du jeu pour MinMax."""
        
        # Si le jeu est terminé, on calcule les scores finaux en tenant compte des pénalités
        if self.est_termine():
            penalite_j1 = sum(d[0] + d[1] for d in self.main_joueur1)
            penalite_j2 = sum(d[0] + d[1] for d in self.main_joueur2)

            score_final_j1 = self.score_joueur1 - penalite_j1
            score_final_j2 = self.score_joueur2 - penalite_j2

            return score_final_j1 - score_final_j2

        score = self.score_joueur1 - self.score_joueur2
        
        # Avantage pour avoir moins de dominos en main (éviter les pénalités)
        score -= len(self.main_joueur1) * 2
        score += len(self.main_joueur2) * 2

        #Avantage pour garder les doubles (ils offrent plus de flexibilité)
        score += sum(5 for d in self.main_joueur1 if d[0] == d[1])
        score -= sum(5 for d in self.main_joueur2 if d[0] == d[1])


        #Prendre en compte les valeurs des extrémités du plateau
        if self.plateau:
            gauche, droite = self.plateau[0][0], self.plateau[-1][1]
            
            # Vérifier si le joueur actuel peut jouer sans piocher
            coups_possibles = self.coups_possibles()
            if coups_possibles:
                # Bonus si le joueur peut jouer immédiatement
                score += 10
            else:
                # Malus si le joueur doit piocher
                score -= 15

            adversaire_peut_jouer = any(self.peut_jouer(d) for d in self.main_joueur2)
            if not adversaire_peut_jouer:
                score += 20

        return score


    def peut_jouer(self, domino):
        """Vérifie si un domino peut être joué."""
        if not self.plateau:
            return True
        gauche, droite = self.plateau[0][0], self.plateau[-1][1]
        return gauche in domino or droite in domino

    def afficher_plateau(self):
        """Afficher le plateau de jeu et les scores."""
        print("==============================================================")
        print(f"main joueur 1 : {self.main_joueur1}")
        print(f"main joueur 2 : {self.main_joueur2}")
        print("Plateau :", " - ".join(f"[{a}|{b}]" for a, b in self.plateau))
        print(f"Score Joueur 1 : {self.score_joueur1} points")
        print(f"Score Joueur 2 : {self.score_joueur2} points")
        print("==============================================================")
        
    def afficher_etat(self):
        """Affiche l'état complet du jeu avec les mains et le plateau."""
        print(f"Main Joueur 1 : {self.main_joueur1}")
        print(f"Main Joueur 2 : {self.main_joueur2}")
        if self.plateau:
            print("\nPlateau actuel :")
            print(" - ".join(f"[{a}|{b}]" for a, b in self.plateau))
        else:
            print("\nPlateau vide")
        print(f"\nScore Joueur 1 : {self.score_joueur1} points")
        print(f"Score Joueur 2 : {self.score_joueur2} points")
        print("\n" + "="*60)
        

    def afficher_mains(self):
        """Afficher les mains des joueurs."""
        print(f"Main Joueur 1: {self.main_joueur1}")
        print(f"Main Joueur 2: {self.main_joueur2}")
        
    def joueur_suivant(self):
        """Passe au joueur suivant."""
        self.joueur_actuel = 2 if self.joueur_actuel == 1 else 1
        return self.joueur_actuel

    def determiner_premier_joueur(self):
        """Détermine quel joueur commence en fonction des règles."""
        meilleur_domino = None
        joueur_debutant = None

        for joueur, main in enumerate([self.main_joueur1, self.main_joueur2], start=1):
            for domino in main:
                if (not meilleur_domino or 
                    (domino[0] == domino[1] and (meilleur_domino[0] != meilleur_domino[1] or domino[0] > meilleur_domino[0])) or
                    (domino[0] != domino[1] and meilleur_domino[0] != meilleur_domino[1] and sum(domino) > sum(meilleur_domino))):
                    meilleur_domino = domino
                    joueur_debutant = joueur

        # mettre à jour le score et le plateau (premiere coup)
        if joueur_debutant == 1:
            self.main_joueur1.remove(meilleur_domino)
            self.score_joueur1 += self.evaluer_coup(meilleur_domino)
        else:
            self.main_joueur2.remove(meilleur_domino)
            self.score_joueur2 += self.evaluer_coup(meilleur_domino)
        
        self.plateau.append(meilleur_domino)
        self.joueur_actuel = joueur_debutant
        self.joueur_suivant()
        return joueur_debutant
    
    def dominos_inconnus(self):
        """Retourne les dominos non visibles."""
        visibles = set(self.main_joueur1 + self.main_joueur2 + self.plateau)
        return [domino for domino in self.dominoes if domino not in visibles]
    
    def copie(self):
        """Crée une copie indépendante de l'état actuel du jeu."""
        copie_jeu = Domino()
        copie_jeu.main_joueur1 = self.main_joueur1[:]
        copie_jeu.main_joueur2 = self.main_joueur2[:] + self.dominoes[:]
        copie_jeu.plateau = self.plateau[:]
        copie_jeu.joueur_actuel = self.joueur_actuel
        copie_jeu.score_joueur1 = self.score_joueur1
        copie_jeu.score_joueur2 = self.score_joueur2
        return copie_jeu
    
    
    def numero_joueur_actuel(self):
        return self.joueur_actuel
    
