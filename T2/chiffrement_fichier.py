from cryptography.fernet import Fernet
import os

def generer_cle():
    key = Fernet.generate_key()
    print("La cle generee :", key)

    chemin_cle = input("saisir le chemin pour sauvegarder la cle (par defaut: conf.txt) : ").strip()
    if not chemin_cle:
        chemin_cle = "conf.txt"

    with open(chemin_cle, "wb") as key_file:
        key_file.write(key)

    print(f"la cle a ete sauvegardee dans '{chemin_cle}'")


def chiffrer_fichier():
    chemin_cle = input("saisir le chemin du fichier de cle (par defaut: conf.txt) : ").strip()
    if not chemin_cle:
        chemin_cle = "conf.txt"

    if not os.path.isfile(chemin_cle):
        print("Erreur: le fichier de cle n'existe pas. Generez d'abord une cle.")
        return

    # Charger la cle d'abord
    with open(chemin_cle, "rb") as key_file:
        key = key_file.read()

    f = Fernet(key)  # reference vers l'objet cle
    print(" la cle :", f)

    chemin_fichier = input("saisir le chemin du fichier a chiffrer : ").strip()

    if not os.path.isfile(chemin_fichier):
        print("Erreur: le fichier n'existe pas")
        return

    with open(chemin_fichier, "rb") as file:
        data = file.read()

    # Chiffrer le contenu lu
    encrypted_data = f.encrypt(data)

    # Sauvegarder le fichier chiffre
    chemin_chiffre = chemin_fichier + ".enc"
    with open(chemin_chiffre, "wb") as file:
        file.write(encrypted_data)

    print(f"le fichier a ete chiffre et sauvegarde dans '{chemin_chiffre}'")


def dechiffrer_fichier():
    chemin_cle = input("saisir le chemin du fichier de cle (par defaut: conf.txt) : ").strip()
    if not chemin_cle:
        chemin_cle = "conf.txt"

    if not os.path.isfile(chemin_cle):
        print("Erreur: le fichier de cle n'existe pas")
        return

    with open(chemin_cle, "rb") as key_file:
        key = key_file.read()

    f = Fernet(key)

    chemin_fichier = input("saisir le chemin du fichier chiffre (.enc) : ").strip()

    if not os.path.isfile(chemin_fichier):
        print("Erreur: le fichier n'existe pas")
        return

    # Lire le fichier chiffre
    with open(chemin_fichier, "rb") as file:
        encrypted_data = file.read()

    # Dechiffrer
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except Exception:
        print("Erreur: impossible de dechiffrer. Mauvaise cle ou fichier corrompu.")
        return

    # Sauvegarder le fichier dechiffre
    if chemin_fichier.endswith(".enc"):
        chemin_dechiffre = chemin_fichier[:-4] + ".dechiffre"
    else:
        chemin_dechiffre = chemin_fichier + ".dechiffre"

    with open(chemin_dechiffre, "wb") as file:
        file.write(decrypted_data)

    print(f"le fichier a ete dechiffre et sauvegarde dans '{chemin_dechiffre}'")

# generer_cle()
# chiffrer_fichier()
# dechiffrer_fichier()
