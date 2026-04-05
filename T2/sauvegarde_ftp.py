import os
import datetime
from ftp_connexion import get_ftp_connection

def lister_fichiers_ftp(ftp):
    fichiers = []
    ftp.retrlines('NLST', fichiers.append)
    return fichiers

def obtenir_version_suivante(ftp, nom_base):
    fichiers_distants = lister_fichiers_ftp(ftp)
    nom_sans_ext = os.path.splitext(nom_base)[0]
    ext = os.path.splitext(nom_base)[1]

    version = 1
    while True:
        nom_versionne = f"{nom_sans_ext}_V{version}{ext}"
        if nom_versionne not in fichiers_distants:
            return nom_versionne
        version += 1

def sauvegarde_incrementale():
    ftp = get_ftp_connection()
    if ftp is None:
        return

    try:
        dossier_local = input("saisir le chemin du dossier local a sauvegarder : ").strip()# Demande le dossier à sauvegarder

        if not os.path.isdir(dossier_local):
            print("Erreur: le dossier n'existe pas")
            return

        print("Selectionnez le site :")
        print("1. Paris")
        print("2. Marseille")
        print("3. Rennes")
        print("4. Grenoble")
        choix_site = input("Votre choix : ").strip()

        sites = {'1': 'Paris', '2': 'Marseille', '3': 'Rennes', '4': 'Grenoble'}
        site = sites.get(choix_site)

        if site is None:
            print("choix invalide")
            return

        try:
            ftp.cwd(site)
        except Exception:
            try:
                ftp.mkd(site)
                ftp.cwd(site)
                print(f"le repertoire '{site}' a ete cree sur le FTP")
            except Exception as e:
                print(f"Erreur: impossible de creer le repertoire du site : {e}")
                return

        horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")# Génère un nom de dossier de sauvegarde avec date

        nom_sauvegarde = f"sauvegarde_{horodatage}"

        try:
            ftp.mkd(nom_sauvegarde)
            ftp.cwd(nom_sauvegarde)
        except Exception as e:
            print(f"Erreur lors de la creation du dossier de sauvegarde : {e}")
            return

        fichiers_distants = lister_fichiers_ftp(ftp)
        compteur = 0

        for nom_fichier in os.listdir(dossier_local):
            chemin_complet = os.path.join(dossier_local, nom_fichier)

            if not os.path.isfile(chemin_complet):
                continue

            if nom_fichier in fichiers_distants:
                nom_versionne = obtenir_version_suivante(ftp,
                                                         nom_fichier)  # Signale si une ancienne version existe déjà
                print(f"  archivage de l'ancienne version -> {nom_versionne}")

            with open(chemin_complet, 'rb') as fichier:
                ftp.storbinary(f'STOR {nom_fichier}', fichier)# Envoie le fichier sur le FTP

                compteur += 1
                print(f"  envoye : {nom_fichier}")

        print(f"\nsauvegarde terminee : {compteur} fichier(s) envoye(s) dans {site}/{nom_sauvegarde}")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

    finally:
        ftp.quit()


def sauvegarde_versionnee():
    ftp = get_ftp_connection()
    if ftp is None:
        return

    try:
        chemin_fichier = input("saisir le chemin du fichier a sauvegarder : ").strip()

        if not os.path.isfile(chemin_fichier):
            print("Erreur: le fichier n'existe pas")
            return

        rep_distant = input("saisir le repertoire distant de destination : ").strip()
        if rep_distant:
            try:
                ftp.cwd(rep_distant)
            except Exception:
                print(f"Erreur: le repertoire '{rep_distant}' n'existe pas sur le FTP")
                return

        nom_fichier = os.path.basename(chemin_fichier)
        nom_versionne = obtenir_version_suivante(ftp, nom_fichier)

        with open(chemin_fichier, 'rb') as fichier:
            ftp.storbinary(f'STOR {nom_versionne}', fichier)# Envoie le fichier

        print(f"le fichier a ete sauvegarde sous le nom '{nom_versionne}'")

    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

    finally:
        ftp.quit()

# sauvegarde_incrementale()
# sauvegarde_versionnee()