from gestion_fichiers_local import gestion_fichiers_local
from naviguer_ftp import naviguer_ftp
from upload_ftp import upload_fichier
from download_ftp import download_fichier
from sauvegarde_ftp import sauvegarde_incrementale, sauvegarde_versionnee
from chiffrement_fichier import generer_cle, chiffrer_fichier, dechiffrer_fichier
from authentification import login_system

def affichage_menu():
    role_connecte = login_system()
    if role_connecte is None:
        print("Programme arrete")
        return
    elif role_connecte == "user":
        print("Acces refuse")
        return

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
         0. Quitter""")

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
                print("Vous avez quitte le programme")
                return

            case _:
                print("---->je ne comprend pas la demande")


affichage_menu()
