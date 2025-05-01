from Jeu.Morpion import Morpion
from Jeu.Domino import Domino
from Joueur.JoueurMinMax import JoueurMinMax
from Joueur.JoueurMinMax2 import JoueurMinMax2
from Joueur.JoueurAdversaire import JoueurAdversaire
from Adversaire.AdversaireRandom import AdversaireRandom
from Adversaire.AdversairePremierCoup import AdversairePremierCoup
from Adversaire.AdversaireDernierCoup import AdversaireDernierCoup
from Adversaire.AdversaireDominoFort import AdversaireDominoFort


def creer_modeles_adversaires():
    return [
        AdversaireRandom(),
        AdversairePremierCoup(),
        AdversaireDernierCoup(),
        AdversaireDominoFort()
    ]

def choisir_adversaire():
    print("\nChoisissez le modele d'adversaire réel contre lequel MinMax va jouer :")
    print("1 - Adversaire Random (débutant)")
    print("2 - Adversaire Premier Coup (intermédiaire)")
    print("3 - Adversaire Dernier Coup (intermédiaire)")
    print("4 - Adversaire Fort Domino (expert, uniquement Domino)")
    choix = input("Entrez votre choix (1/2/3/4) : ").strip()

    if choix == "1":
        return AdversaireRandom()
    elif choix == "2":
        return AdversairePremierCoup()
    elif choix == "3":
        return AdversaireDernierCoup()
    elif choix == "4":
        return AdversaireDominoFort()
    else:
        print("Choix invalide. L'adversaire par défaut sera AdversaireRandom.")
        return AdversaireRandom()

def lancer_partie(jeu, joueur1, joueur2):
    print("\n=== Début de la partie ===")
    jeu.afficher_etat()

    while not jeu.est_termine():
        joueur_actuel = joueur1 if jeu.numero_joueur_actuel() == 1 else joueur2
        autre_joueur = joueur2 if jeu.numero_joueur_actuel() == 1 else joueur1

        print(f"\n--- Tour du Joueur {jeu.joueur_actuel} ---")
        coup = joueur_actuel.choisir_coup(jeu)
        if coup:
            print(f"Joueur {jeu.joueur_actuel} joue : {coup}")
            autre_joueur.informer_coup_adversaire(jeu, coup)
            jeu.jouer(coup)
        else:
            print(f"Joueur {jeu.joueur_actuel} ne peut pas jouer")
            jeu.joueur_suivant()

        jeu.afficher_etat()

    print("\n=== Fin de la partie ===")
    if isinstance(jeu, Domino):
        jeu.calculer_score_final()
        print(f"Score final Joueur 1 (MinMax) : {jeu.score_joueur1} points")
        print(f"Score final Joueur 2 (Adversaire) : {jeu.score_joueur2} points")
        if jeu.score_joueur1 > jeu.score_joueur2:
            print("Victoire du Joueur 1 (MinMax) !")
        elif jeu.score_joueur2 > jeu.score_joueur1:
            print("Victoire du Joueur 2 (Adversaire) !")
        else:
            print("Match nul !")
    else:
        if jeu.evaluation() == 10:
            print("Victoire du Joueur 1 (X / MinMax) !")
        elif jeu.evaluation() == -10:
            print("Victoire du Joueur 2 (O / Adversaire) !")
        else:
            print("Match nul !")


def test_experience(jeu_type, minmax,nb_iterations=100):
    adversaire_modele = choisir_adversaire()

    minmax_victoires = 0
    adversaire_victoires = 0
    nuls = 0

    for i in range(nb_iterations):
        joueur_minmax = minmax
        joueur_minmax.modeles_credibles = creer_modeles_adversaires()
        joueur_adversaire = JoueurAdversaire(adversaire_modele)

        jeu = Domino() if jeu_type == "D" else Morpion()
        lancer_partie(jeu, joueur_minmax, joueur_adversaire)

        if isinstance(jeu, Domino):
            jeu.calculer_score_final()
            if jeu.score_joueur1 > jeu.score_joueur2:
                minmax_victoires += 1
            elif jeu.score_joueur2 > jeu.score_joueur1:
                adversaire_victoires += 1
            else:
                nuls += 1
        else:
            if jeu.evaluation() == 10:
                minmax_victoires += 1
            elif jeu.evaluation() == -10:
                adversaire_victoires += 1
            else:
                nuls += 1

    print(f"\nRésultat après {nb_iterations} parties ({'Domino' if jeu_type == 'D' else 'Morpion'}) :")
    print(f"Victoire MinMax      : {minmax_victoires}")
    print(f"Victoire Adversaire  : {adversaire_victoires}")
    print(f"Matchs nuls          : {nuls}")

if __name__ == "__main__":
    print("Que souhaitez-vous faire ?")
    print("1 - Lancer une partie")
    print("2 - Lancer les experiences statistiques (100 parties)")

    mode = input("Entrez votre choix (1/2) : ").strip()

    if mode == "1":
        print("\nChoisissez le jeu :")
        print("D - Domino")
        print("M - Morpion")
        jeu_choix = input("Entrez votre choix (D/M) : ").strip().upper()
        
        print("\n Choisissez L'algo MinMax :")
        print("1 - MinMax approximatif")
        print("2 - MinMax réaliste")
        choix_minmax = input("Entrez votre choix (1/2) : ").strip()
        
        if choix_minmax == "1":
            joueur_minmax = JoueurMinMax(profondeur=3)
        elif choix_minmax == "2":
            joueur_minmax = JoueurMinMax2(profondeur=3)
        else:
            print("Choix invalide, MinMax approximatif sera utilisé par défaut.")
            joueur_minmax = JoueurMinMax(profondeur=3)
            
        joueur_minmax.modeles_credibles = creer_modeles_adversaires()

        adversaire_modele = choisir_adversaire()

        if jeu_choix == "M" and isinstance(adversaire_modele, AdversaireDominoFort):
            print("\n[ATTENTION] AdversaireDominoFort ne fonctionne que pour Domino")
            print("L'adversaire sera remplacé par AdversaireRandom")
            adversaire_modele = AdversaireRandom()

        joueur_adversaire = JoueurAdversaire(adversaire_modele)

        if jeu_choix == "D":
            jeu = Domino()
        elif jeu_choix == "M":
            jeu = Morpion()
        else:
            print("Choix invalide")
            exit()

        # Lancer la partie, la fin de partie est gérée dans cette fonction
        lancer_partie(jeu, joueur_minmax, joueur_adversaire)

    elif mode == "2":
        print("\nMode test statistique !")
        print("1 - Lancer 100 parties de Domino")
        print("2 - Lancer 100 parties de Morpion")
        print("3 - Lancer les deux expériences")
        choix_stat = input("Entrez votre choix (1/2/3) : ").strip()
        
        print("\n Choisissez L'algo MinMax :")
        print("1 - MinMax approximatif")
        print("2 - MinMax réaliste")
        choix_minmax = input("Entrez votre choix (1/2) : ").strip()
        
        if choix_minmax == "1":
            joueur_minmax = JoueurMinMax(profondeur=3)
        elif choix_minmax == "2":
            joueur_minmax = JoueurMinMax2(profondeur=3)
        else:
            print("Choix invalide, MinMax approximatif sera utilisé par défaut.")
            joueur_minmax = JoueurMinMax(profondeur=3)
        

        if choix_stat == "1":
            test_experience(jeu_type="D", minmax=joueur_minmax, nb_iterations=100)
        elif choix_stat == "2":
            test_experience(jeu_type="M", minmax=joueur_minmax, nb_iterations=100)
        elif choix_stat == "3":
            test_experience(jeu_type="D", minmax=joueur_minmax, nb_iterations=100)
            test_experience(jeu_type="M", minmax=joueur_minmax, nb_iterations=100)
        else:
            print("Choix invalide")
    else:
        print("Choix invalide")
        
        
# 

