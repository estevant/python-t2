import os
from connexion_ftp import get_ftp_connection

def upload_fichier():
    ftp = get_ftp_connection()
    if ftp is None:
        return

    try:
        chemin_fichier = input("saisir le chemin du fichier a envoyer : ").strip()

        if not os.path.isfile(chemin_fichier):
            print("Erreur: le fichier n'existe pas")
            return

        nom_fichier = os.path.basename(chemin_fichier)

        rep_distant = input("saisir le repertoire distant (laisser vide pour la racine) : ").strip()
        if rep_distant:
            try:
                ftp.cwd(rep_distant)
            except Exception:
                print(f"Erreur: le repertoire distant '{rep_distant}' n'existe pas")
                return

        with open(chemin_fichier, 'rb') as fichier:
            ftp.storbinary(f'STOR {nom_fichier}', fichier) # Envoie le fichier en mode binaire sur le FTP


        print(f"le fichier '{nom_fichier}' a ete envoye avec succes")

    except Exception as e:
        print(f"Erreur lors de l'upload : {e}")

    finally:
        ftp.quit()

# upload_fichier()