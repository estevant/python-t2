import os
import shutil

def gestion_fichiers_local():
    while True:
        print("""
         1. Naviguer dans l'arborescence
         2. Creer un repertoire/fichier
         3. Modifier un fichier
         4. Copier un repertoire/fichier
         5. Deplacer un repertoire/fichier
         6. Supprimer un repertoire/fichier
         0. Retour au menu""")

        choix = input("Selectionnez une option : ").strip()

        match choix:
            case '1':
                naviguer_arborescence()
            case '2':
                creer_fichier_repertoire()
            case '3':
                modifier_fichier()
            case '4':
                copier_fichier_repertoire()
            case '5':
                deplacer_fichier_repertoire()
            case '6':
                supprimer_fichier_repertoire()
            case '0':
                print("retour au menu")
                return
            case _:
                print("---->je ne comprend pas la demande")


def naviguer_arborescence():
    chemin = input("saisir le chemin du repertoire a explorer (. pour le courant) : ").strip()
    if not chemin:
        chemin = "."  # dossier courant par défaut

    if not os.path.isdir(chemin):
        print("Erreur: ce repertoire n'existe pas")
        return

    print(f"\ncontenu de '{os.path.abspath(chemin)}' :")
    for element in os.listdir(chemin):
        chemin_complet = os.path.join(chemin, element)
        if os.path.isdir(chemin_complet):
            print(f"  [REP] {element}")  # affiche les répertoires
        else:
            taille = os.path.getsize(chemin_complet)
            print(f"  [FIC] {element} ({taille} octets)")  # affiche les fichiers + taille


def creer_fichier_repertoire():
    print("1. Creer un repertoire")
    print("2. Creer un fichier")
    choix = input("Votre choix : ").strip()

    if choix == "1":
        chemin = input("saisir le chemin du repertoire a creer : ").strip()
        try:
            os.makedirs(chemin, exist_ok=True)# crée le répertoire (+ parents)

            print(f"le repertoire '{chemin}' a ete cree")
        except Exception as e:
            print(f"Erreur : {e}")

    elif choix == "2":
        chemin = input("saisir le chemin du fichier a creer : ").strip()
        contenu = input("saisir le contenu du fichier (laisser vide pour un fichier vide) : ")
        try:
            with open(chemin, 'w') as fichier:
                fichier.write(contenu)
            print(f"le fichier '{chemin}' a ete cree")
        except Exception as e:
            print(f"Erreur : {e}")
    else:
        print("on ne comprend pas la demande")


def modifier_fichier():
    chemin = input("saisir le chemin du fichier a modifier : ").strip()

    if not os.path.isfile(chemin):
        print("Erreur: ce fichier n'existe pas")
        return

    try:
        with open(chemin, 'r') as fichier:
            contenu_actuel = fichier.read()
        print(f"\ncontenu actuel :\n{contenu_actuel}")

        print("\n1. Ecraser le contenu")
        print("2. Ajouter du contenu a la fin")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            nouveau_contenu = input("saisir le nouveau contenu : ")
            with open(chemin, 'w') as fichier:
                fichier.write(nouveau_contenu)# Écrase le fichier avec le nouveau contenu
            print("le fichier a ete modifie")

        elif choix == "2":
            ajout = input("saisir le contenu a ajouter : ")
            with open(chemin, 'a') as fichier:
                fichier.write("\n" + ajout)# Ajoute le contenu à la fin
            print("le contenu a ete ajoute")
        else:
            print("on ne comprend pas la demande")

    except Exception as e:
        print(f"Erreur : {e}")


def copier_fichier_repertoire():
    source = input("saisir le chemin source : ").strip()
    destination = input("saisir le chemin de destination : ").strip()

    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)# Copie récursive d'un répertoire
            print(f"le repertoire '{source}' a ete copie vers '{destination}'")
        elif os.path.isfile(source):
            shutil.copy2(source, destination)# Copie d'un fichier en conservant les métadonnées
            print(f"le fichier '{source}' a ete copie vers '{destination}'")
        else:
            print("Erreur: le chemin source n'existe pas")
    except Exception as e:
        print(f"Erreur : {e}")


def deplacer_fichier_repertoire():
    source = input("saisir le chemin source : ").strip()
    destination = input("saisir le chemin de destination : ").strip()

    if not os.path.exists(source):
        print("Erreur: le chemin source n'existe pas")
        return

    try:
        shutil.move(source, destination)# déplace le fichier ou répertoire -> destination
        print(f"'{source}' a ete deplace vers '{destination}'")
    except Exception as e:
        print(f"Erreur : {e}")


def supprimer_fichier_repertoire():
    chemin = input("saisir le chemin a supprimer : ").strip()

    if not os.path.exists(chemin):
        print("Erreur: ce chemin n'existe pas")
        return

    confirmation = input(f"confirmer la suppression de '{chemin}' ? (oui/non) : ").strip().lower()
    if confirmation != "oui":
        print("suppression annulee")
        return

    try:
        if os.path.isdir(chemin):
            shutil.rmtree(chemin)# Supprime le répertoire et son contenu
            print(f"le repertoire '{chemin}' et son contenu ont ete supprimes")
        else:
            os.remove(chemin)# Supprime
            print(f"le fichier '{chemin}' a ete supprime")
    except Exception as e:
        print(f"Erreur : {e}")

# gestion_fichiers_local()