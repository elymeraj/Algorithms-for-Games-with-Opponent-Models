from Jeu.JeuInformationIncomplete import JeuInformationIncomplete
import random

class Domino(JeuInformationIncomplete):
    def __init__(self):
        super().__init__()
        self.dominoes = [(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(self.dominoes)
        self.main_joueur1 = []
        self.main_joueur2 = []
        self.plateau = []
        self.joueur_actuel = 1
        self.score_joueur1 = 0
        self.score_joueur2 = 0
        self.pioche_disponible = True
        self.tours_sans_coup = 0 # compteur pour les tours sans coup 
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

        # les extrémité du plateau
        gauche, droite = (self.plateau[0][0], self.plateau[-1][1]) if self.plateau else (None, None)
        coups = []
        
        # vérifier chaque domino dans la main
        for domino in main_actuelle:
            if not self.plateau:
                coups.append(domino)
                continue

            if domino[0] == gauche or domino[1] == gauche or domino[0] == droite or domino[1] == droite:
                coups.append(domino)


        if not coups:
            self.tours_sans_coup += 1
        else:
            self.tours_sans_coup = 0

        return coups
    
    def piocher(self):
        """Pioche un domino si possible."""
        if self.dominoes and self.pioche_disponible:
            pioche = self.dominoes.pop(0)
            main_actuelle = self.main_joueur1 if self.joueur_actuel == 1 else self.main_joueur2
            main_actuelle.append(pioche)
            print(f"Joueur {self.joueur_actuel} pioche le domino {pioche}.")
            self.pioche_disponible = False
            if self.joueur_actuel == 1:
                self.score_joueur1 -= 10
            else:
                self.score_joueur2 -= 10


    def est_termine(self):
        """Déterminer si le jeu est terminé."""
        if not self.main_joueur1 or not self.main_joueur2:
            return True

        # Si aucun joueur ne peut jouer pendant 2 tours consécutifs
        if self.tours_sans_coup >= 4:
            return True

        # Si la pioche est vide et aucun joueur ne peut jouer
        if not self.dominoes:
            joueur1_peut_jouer = any(self.peut_jouer(domino) for domino in self.main_joueur1)
            joueur2_peut_jouer = any(self.peut_jouer(domino) for domino in self.main_joueur2)
            if not joueur1_peut_jouer and not joueur2_peut_jouer:
                return True

        return False

    def evaluer_coup(self, coup):
        """Évalue un coup selon des critères stratégiques."""
        points = 0
            
        # Bonus pour jouer un domino
        points += 5
        
        # Bonus pour les valeurs du domino
        points += 2 * (coup[0] + coup[1])
        
        # Bonus pour un double
        if coup[0] == coup[1]:
            points += 10
        
        if self.plateau:
            gauche, droite = self.plateau[0][0], self.plateau[-1][1]
            # Bonus pour double connexion possible
            if (gauche in coup and droite in coup):
                points += 15
            # Si ce coup force probablement l'adversaire à piocher
            main_adverse = self.main_joueur2 if self.joueur_actuel == 1 else self.main_joueur1
            nouveau_gauche = coup[1] if gauche == coup[0] else gauche
            nouveau_droite = coup[0] if droite == coup[1] else droite
            
            # Vérifier si l'adversaire pourra jouer
            adversaire_pourra_jouer = False
            for d in main_adverse:
                if nouveau_gauche in d or nouveau_droite in d:
                    adversaire_pourra_jouer = True
                    break
            
            # Bonus si l'adversaire ne pourra pas jouer
            if not adversaire_pourra_jouer:
                points += 20
        
        return points

    def calculer_score_final(self):
        """Calcule les scores finaux en tenant compte des pénalités."""
        # Pénalités pour les dominos restants dans la main
        penalite_j1 = sum(d[0] + d[1] for d in self.main_joueur1)
        penalite_j2 = sum(d[0] + d[1] for d in self.main_joueur2)
        
        self.score_joueur1 -= penalite_j1
        self.score_joueur2 -= penalite_j2
        
        # Bonus pour être le premier à vider sa main
        if not self.main_joueur1:
            self.score_joueur1 += 50
        elif not self.main_joueur2:
            self.score_joueur2 += 50

    def jouer(self, coup):
        """Joue un domino sur le plateau et met à jour l'état du jeu."""
        main_actuelle = self.main_joueur1 if self.joueur_actuel == 1 else self.main_joueur2

        if coup not in main_actuelle:
            raise ValueError(f"Le domino {coup} n'est pas dans la main du joueur {self.joueur_actuel}.")

        # mettre à jour le score
        points = self.evaluer_coup(coup)
        if self.joueur_actuel == 1:
            self.score_joueur1 += points
        else:
            self.score_joueur2 += points

        # placer le domino
        if self.peut_jouer(coup):
            if not self.plateau:
                self.plateau.append(coup)
            else:
                gauche, droite = self.plateau[0][0], self.plateau[-1][1]
                if gauche == coup[0]:
                    self.plateau.insert(0, (coup[1], coup[0]))  # Inverser pour connecter
                elif gauche == coup[1]:
                    self.plateau.insert(0, coup)
                elif droite == coup[0]:
                    self.plateau.append(coup)
                elif droite == coup[1]:
                    self.plateau.append((coup[1], coup[0]))  # Inverser pour connecter

            # supprimer le domino de main de joueur
            main_actuelle.remove(coup)

            # Réinitialiser la possibilité de piocher pour le prochain tour
            self.pioche_disponible = True

            # joueur suivant 
            self.joueur_actuel = 2 if self.joueur_actuel == 1 else 1
        else:
            raise ValueError(f"Le domino {coup} ne peut pas être joué.")

    def evaluation(self):
        """Évaluation améliorée de l'état du jeu pour MinMax."""
        # Différence de score comme base
        score = self.score_joueur1 - self.score_joueur2
        
        # Avantage pour avoir moins de dominos en main
        score -= len(self.main_joueur1) * 5
        score += len(self.main_joueur2) * 5
        
        # Bonus si on est proche de vider sa main
        if len(self.main_joueur1) <= 2:
            score += 30
        if len(self.main_joueur2) <= 2:
            score -= 30

        # Avantage pour avoir des dominos connectables aux extrémités
        if self.plateau:
            gauche, droite = self.plateau[0][0], self.plateau[-1][1]
            
            # Points pour les possibilités de connexion du joueur 1
            connectables_j1 = sum(1 for d in self.main_joueur1 if gauche in d or droite in d)
            score += connectables_j1 * 3
            
            # Points pour les possibilités de connexion du joueur 2
            connectables_j2 = sum(1 for d in self.main_joueur2 if gauche in d or droite in d)
            score -= connectables_j2 * 3
            
            # Bonus pour bloquer l'adversaire
            if connectables_j2 == 0 and not self.dominoes:
                score += 25
            if connectables_j1 == 0 and not self.dominoes:
                score -= 25

        return score

    def peut_jouer(self, domino):
        """Vérifie si un domino peut être joué sur le plateau actuel."""
        if not self.plateau:  # aucun domino sur le plateau
            return True
            
        gauche, droite = self.plateau[0][0], self.plateau[-1][1]
        return gauche in domino or droite in domino

    def afficher_plateau(self):
        """Afficher le plateau de jeu et les scores."""
        print("==============================================================")
        print(f"Main joueur 1 : {self.main_joueur1}")
        print(f"Main joueur 2 : {self.main_joueur2}")
        print("Plateau :", " - ".join(f"[{a}|{b}]" for a, b in self.plateau))
        print(f"Score Joueur 1 : {self.score_joueur1} points")
        print(f"Score Joueur 2 : {self.score_joueur2} points")
        print("==============================================================")
        
    def afficher_etat(self):
        """Affiche l'état complet du jeu avec les mains et le plateau."""
        print(f"Main Joueur 1 : {self.main_joueur1}")
        print(f"Main Joueur 2 : {self.main_joueur2}")
        print(f"Pioche restante : {len(self.dominoes)} dominos")
        if self.plateau:
            print("\nPlateau actuel :")
            print(" - ".join(f"[{a}|{b}]" for a, b in self.plateau))
        else:
            print("\nPlateau vide")
        print(f"\nScore Joueur 1 : {self.score_joueur1} points")
        print(f"Score Joueur 2 : {self.score_joueur2} points")
        print("\n" + "="*60)
        
    def joueur_suivant(self):
        """Passe au joueur suivant."""
        self.joueur_actuel = 2 if self.joueur_actuel == 1 else 1
        return self.joueur_actuel

    def determiner_premier_joueur(self):
        """Détermine quel joueur commence en fonction des règles."""
        meilleur_domino = None
        joueur_debutant = None

        #chercher le plus grand double ou le domino avec la plus grande somme
        for joueur, main in enumerate([self.main_joueur1, self.main_joueur2], start=1):
            for domino in main:
                if (not meilleur_domino or 
                    (domino[0] == domino[1] and (meilleur_domino[0] != meilleur_domino[1] or domino[0] > meilleur_domino[0])) or
                    (domino[0] != domino[1] and meilleur_domino[0] != meilleur_domino[1] and sum(domino) > sum(meilleur_domino))):
                    meilleur_domino = domino
                    joueur_debutant = joueur

        #mettre à jour le score et le plateau (premier coup)
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
    
    def copie(self):
        """Crée une copie indépendante de l'état actuel du jeu"""
        nouveau_jeu = Domino.__new__(Domino)
        nouveau_jeu.main_joueur1 = self.main_joueur1.copy()
        nouveau_jeu.main_joueur2 = self.main_joueur2.copy()
        nouveau_jeu.plateau = self.plateau.copy()
        nouveau_jeu.dominoes = self.dominoes.copy()
        nouveau_jeu.joueur_actuel = self.joueur_actuel
        nouveau_jeu.score_joueur1 = self.score_joueur1
        nouveau_jeu.score_joueur2 = self.score_joueur2
        nouveau_jeu.pioche_disponible = self.pioche_disponible
        nouveau_jeu.tours_sans_coup = self.tours_sans_coup
        
        return nouveau_jeu
    
    def numero_joueur_actuel(self):
        """Retourne le numéro du joueur actuel."""
        return self.joueur_actuel
    
    def jeu_termine_score(self):
        """Retourne le score du joueur actuel si le jeu est terminé."""
        jeu_copie = self.copie()
        jeu_copie.calculer_score_final()
        
        diff_score = jeu_copie.score_joueur1 - jeu_copie.score_joueur2
        
        #si le joueur 1 a gagné, bonus important
        if len(self.main_joueur1) == 0:
            return 700
        #si le joueur 2 a gagné, pénalité importante
        if len(self.main_joueur2) == 0:
            return -700
        
        return diff_score

