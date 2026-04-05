import os
from connexion_ftp import get_ftp_connection

def download_fichier():
    ftp = get_ftp_connection()
    if ftp is None:
        return

    try:
        rep_distant = input("saisir le repertoire distant (laisser vide pour la racine) : ").strip()
        if rep_distant:
            try:
                # pour se déplacer dans le répertoire
                ftp.cwd(rep_distant)
            except Exception:
                print(f"Erreur: le repertoire distant '{rep_distant}' n'existe pas")
                return

        print("fichiers disponibles :")
        ftp.retrlines('LIST') # affiche les fichiers dispon

        nom_fichier = input("\nsaisir le nom du fichier a telecharger : ").strip()

        chemin_local = input("saisir le dossier local de destination (laisser vide pour le dossier courant) : ").strip()
        if not chemin_local:
            chemin_local = "."  # Utilise le dossier courant par défaut

        chemin_complet = os.path.join(chemin_local, nom_fichier)# construit le chemin complet

        with open(chemin_complet, 'wb') as fichier:
            ftp.retrbinary(f'RETR {nom_fichier}', fichier.write)# Télécharge le fichier en mode binaire et l'écrit localement

        print(f"le fichier '{nom_fichier}' a ete telecharge avec succes dans '{chemin_complet}'")

    except Exception as e:
        print(f"Erreur lors du download : {e}")

    finally:
        ftp.quit()

# download_fichier()