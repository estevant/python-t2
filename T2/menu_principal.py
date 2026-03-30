import sys
import os

from authentification import login_system
from interaction_user import add_user
from afficher_utilisateur import show_user
from suppression_utilisateur import delete_user
from mise_a_jour import maj_user
from gestion_fichiers_local import gestion_fichiers_local
from naviguer_ftp import naviguer_ftp
from upload_ftp import upload_fichier
from download_ftp import download_fichier
from sauvegarde_ftp import sauvegarde_incrementale, sauvegarde_versionnee
from chiffrement_fichier import generer_cle, chiffrer_fichier, dechiffrer_fichier

def menu_gestion_users(role_connecte):
    while True:
        print("""
    ===== GESTION DES UTILISATEURS =====
         1. Ajouter un utilisateur
         2. Mise a jour d'un utilisateur
         3. Supprimer un utilisateur
         4. Consulter les utilisateurs
         0. Retour au menu principal""")

        choix = input("Selectionnez une option presente sur le menu : ")

        match choix:

            case '1':
                print("Vous avez selectionne l option ajouter un utilisateur")
                add_user(role_connecte)

            case '2':
                print("Vous avez selectionne l option mise a jour")
                maj_user(login_connecte, role_connecte)

            case '3':
                print("Vous avez selectionne l option supprimer un compte")
                delete_user(login_connecte, role_connecte)

            case '4':
                print("Vous avez selectionne l option consulter la BDD")
                show_user()

            case '0':
                print("retour au menu principal")
                return

            case _:
                print("---->je ne comprend pas la demande")

def menu_gestion_fichiers():
    while True:
        print("""
    ===== GESTION DES FICHIERS =====
         1. Gestion des fichiers/repertoires en local
         2. Naviguer sur le serveur FTP
         3. Envoyer un fichier sur le FTP (upload)
         4. Telecharger un fichier depuis le FTP (download)
         5. Sauvegarde incrementale vers le FTP
         6. Sauvegarde versionnee d'un fichier
         7. Generer une cle de chiffrement
         8. Chiffrer un fichier
         9. Dechiffrer un fichier
         0. Retour au menu principal""")

        choix = input("Selectionnez une option presente sur le menu : ")

        match choix:

            case '1':
                print("Vous avez selectionne la gestion locale des fichiers")
                gestion_fichiers_local()

            case '2':
                print("Vous avez selectionne la navigation FTP")
                naviguer_ftp()

            case '3':
                print("Vous avez selectionne l upload FTP")
                upload_fichier()

            case '4':
                print("Vous avez selectionne le download FTP")
                download_fichier()

            case '5':
                print("Vous avez selectionne la sauvegarde incrementale")
                sauvegarde_incrementale()

            case '6':
                print("Vous avez selectionne la sauvegarde versionnee")
                sauvegarde_versionnee()

            case '7':
                print("Vous avez selectionne la generation de cle")
                generer_cle()

            case '8':
                print("Vous avez selectionne le chiffrement")
                chiffrer_fichier()

            case '9':
                print("Vous avez selectionne le dechiffrement")
                dechiffrer_fichier()

            case '0':
                print("retour au menu principal")
                return

            case _:
                print("---->je ne comprend pas la demande")

def menu_gestion_reseau():
    while True:
        print("""
    ===== GESTION RESEAU / SYSTEME =====
         (Fonctionnalites T3 - a venir)
         0. Retour au menu principal""")

        choix = input("Selectionnez une option presente sur le menu : ")

        match choix:

            case '0':
                print("retour au menu principal")
                return

            case _:
                print("---->je ne comprend pas la demande")

def affichage_menu_principal():
    resultat_login = login_system()

    if resultat_login is None:
        print("Programme arrete : authentification echouee")
        return

    role_connecte = resultat_login[0]
    login_connecte = resultat_login[1]

    if role_connecte == "user":
        print("Acces refuse : droits insuffisants")
        return

    while True:
        print(f"""
    ===== BOITE A OUTILS - ADMIN ({role_connecte.upper()}) =====
         1. Gestion Users
         2. Gestion Fichiers
         3. Gestion reseau SYS
         0. Quitter""")

        choix = input("Selectionnez une option presente sur le menu : ")

        match choix:

            case '1':
                print("Vous avez selectionne la Gestion des Utilisateurs")
                menu_gestion_users(role_connecte)

            case '2':
                print("Vous avez selectionne la Gestion des Fichiers")
                menu_gestion_fichiers()

            case '3':
                print("Vous avez selectionne la Gestion Reseau / SYS")
                menu_gestion_reseau()

            case '0':
                print("Vous avez quitte le programme")
                return

            case _:
                print("---->je ne comprend pas la demande")


affichage_menu_principal()