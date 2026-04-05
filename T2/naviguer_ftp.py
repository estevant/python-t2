from ftp_connexion import get_ftp_connection

def naviguer_ftp():
    ftp = get_ftp_connection()
    if ftp is None:
        return

    try:
        print(f"repertoire actuel : {ftp.pwd()}")

        while True:
            print("""
         1. Lister les fichiers du repertoire courant
         2. Changer de repertoire
         3. Creer un repertoire
         4. Supprimer un repertoire
         5. Supprimer un fichier
         0. Retour au menu""")

            choix = input("Selectionnez une option : ").strip()

            match choix:

                case '1':
                    print("\ncontenu du repertoire :")
                    ftp.retrlines('LIST')# Liste le contenu du répertoire courant
                    print(f"\nrepertoire actuel : {ftp.pwd()}")

                case '2':
                    dossier = input("saisir le nom du repertoire (.. pour remonter) : ").strip()
                    try:
                        ftp.cwd(dossier)# Change de répertoire sur le serveur FTP
                        print(f"repertoire actuel : {ftp.pwd()}")
                    except Exception:
                        print(f"Erreur: impossible d'acceder a '{dossier}'")

                case '3':
                    nom_rep = input("saisir le nom du nouveau repertoire : ").strip()
                    try:
                        ftp.mkd(nom_rep)# Crée un nouveau répertoire sur le serveur
                        print(f"le repertoire '{nom_rep}' a ete cree")
                    except Exception as e:
                        print(f"Erreur lors de la creation : {e}")

                case '4':
                    nom_rep = input("saisir le nom du repertoire a supprimer : ").strip()
                    try:
                        ftp.rmd(nom_rep)# Supprime un répertoire sur le serveur
                        print(f"le repertoire '{nom_rep}' a ete supprime")
                    except Exception as e:
                        print(f"Erreur lors de la suppression : {e}")

                case '5':
                    nom_fichier = input("saisir le nom du fichier a supprimer : ").strip()
                    try:
                        ftp.delete(nom_fichier)# Supprime un fichier sur le serveur
                        print(f"le fichier '{nom_fichier}' a ete supprime")
                    except Exception as e:
                        print(f"Erreur lors de la suppression : {e}")

                case '0':
                    print("retour au menu")
                    return

                case _:
                    print("---->je ne comprend pas la demande")

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        ftp.quit()

# naviguer_ftp()