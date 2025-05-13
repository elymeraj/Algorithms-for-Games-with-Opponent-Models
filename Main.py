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
    print("\nChoisissez le modèle d'adversaire contre lequel MinMax va jouer :")
    print("1 - Adversaire Random")
    print("2 - Adversaire Premier Coup")
    print("3 - Adversaire Dernier Coup")
    print("4 - Adversaire Fort Domino (uniquement Domino)")
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
    print("\n=== Debut de la partie ===")
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
        gagnant = jeu.qui_gagne()
        if gagnant == 'X':
            print("Victoire du Joueur 1 (X / MinMax) !")
        elif gagnant == 'O':
            print("Victoire du Joueur 2 (O / Adversaire) !")
        else:
            print("Match nul !")


def test_experience(jeu_type, minmax, nb_iterations=100):
    adversaire_modele = choisir_adversaire()

    minmax_victoires = 0
    adversaire_victoires = 0
    nuls = 0

    for i in range(nb_iterations):
        print(f"\nPartie {i+1}/{nb_iterations}")
        
        #rinitialiser lesjoueurs pour chaque partie
        joueur_minmax = minmax.__class__(profondeur=minmax.profondeur)
        joueur_minmax.modeles_credibles = creer_modeles_adversaires()
        joueur_adversaire = JoueurAdversaire(adversaire_modele)

        jeu = Domino() if jeu_type == "D" else Morpion()

        lancer_partie(jeu, joueur_minmax, joueur_adversaire)

        #calculer les stats
        if isinstance(jeu, Domino):
            jeu.calculer_score_final()
            if jeu.score_joueur1 > jeu.score_joueur2:
                minmax_victoires += 1
            elif jeu.score_joueur2 > jeu.score_joueur1:
                adversaire_victoires += 1
            else:
                nuls += 1
        else:
            gagnant = jeu.qui_gagne()
            if gagnant == 'X':
                minmax_victoires += 1
            elif gagnant == 'O':
                adversaire_victoires += 1
            else:
                nuls += 1

    print(f"\nResultat apres {nb_iterations} parties ({'Domino' if jeu_type == 'D' else 'Morpion'}) :")
    print(f"Victoire MinMax      : {minmax_victoires} ({minmax_victoires/nb_iterations*100:.1f}%)")
    print(f"Victoire Adversaire  : {adversaire_victoires} ({adversaire_victoires/nb_iterations*100:.1f}%)")
    print(f"Matchs nuls          : {nuls} ({nuls/nb_iterations*100:.1f}%)")

if __name__ == "__main__":
    print("Que souhaitez-vous faire ?")
    print("1 - Lancer une partie")
    print("2 - Lancer les expériences statistiques")

    mode = input("Entrez votre choix (1/2) : ").strip()

    if mode == "1":
        print("\nchoisissez le jeu :")
        print("D - Domino")
        print("M - Morpion")
        jeu_choix = input("Entrez votre choix (D/M) : ").strip().upper()
        
        print("\nchoisissez l'algorithme MinMax :")
        print("1 - MinMax predictif")
        print("2 - MinMax réaliste")
        choix_minmax = input("Entrez votre choix (1/2) : ").strip()
        
        if choix_minmax == "1":
            joueur_minmax = JoueurMinMax(profondeur=3)
        elif choix_minmax == "2":
            joueur_minmax = JoueurMinMax2(profondeur=3)
        else:
            print("Choix invalide, MinMax predictif sera utilisé par défaut.")
            joueur_minmax = JoueurMinMax(profondeur=3)
            
        joueur_minmax.modeles_credibles = creer_modeles_adversaires()

        adversaire_modele = choisir_adversaire()

        if jeu_choix == "M" and isinstance(adversaire_modele, AdversaireDominoFort):
            print("\n!!!AdversaireDominoFort ne fonctionne que pour Domino")
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

        lancer_partie(jeu, joueur_minmax, joueur_adversaire)

    elif mode == "2":
        print("\nMode test statistique !")
        print("1 - Lancer les parties de Domino")
        print("2 - Lancer les parties de Morpion")
        print("3 - Lancer les deux expériences")
        choix_stat = input("Entrez votre choix (1/2/3) : ").strip()
        
        print("\nChoisissez l'algorithme MinMax :")
        print("1 - MinMax predictif")
        print("2 - MinMax réaliste")
        choix_minmax = input("Entrez votre choix (1/2) : ").strip()
        
        print("\nCombien de parties souhaitez-vous lancer ?")
        nb_parties = int(input("Nombre de parties (défaut: 100) : ") or "100")
        
        if choix_minmax == "1":
            joueur_minmax = JoueurMinMax(profondeur=3)
        elif choix_minmax == "2":
            joueur_minmax = JoueurMinMax2(profondeur=3)
        else:
            print("Choix invalide, MinMax predictif sera utilisé par défaut.")
            joueur_minmax = JoueurMinMax(profondeur=3)
        
        if choix_stat == "1":
            test_experience(jeu_type="D", minmax=joueur_minmax, nb_iterations=nb_parties)
        elif choix_stat == "2":
            test_experience(jeu_type="M", minmax=joueur_minmax, nb_iterations=nb_parties)
        elif choix_stat == "3":
            test_experience(jeu_type="D", minmax=joueur_minmax, nb_iterations=nb_parties)
            test_experience(jeu_type="M", minmax=joueur_minmax, nb_iterations=nb_parties)
        else:
            print("Choix invalide")
    else:
        print("Choix invalide")

