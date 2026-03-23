import re
import random
import string
from T1.connexion_bdd import get_connection
import bcrypt
from send_email import envoie_mail

def add_user(current_user_role):
    connexion = get_connection()
    if connexion is None:
        return

    cursor = connexion.cursor()  # cursor methode que j'applique sur mon objet conn et qui permet de renvoyer a la bdd les commandes sql

    print("connexion établie")
    print('saisir les information concernant l\' utilisateur')
    nom = str(input("saisir le nom : ")).strip()
    prenom = str(input("saisir le prenom : ")).strip()
    mail = str(input("saisir le mail : ")).strip()

    print("Quel est le rôle de ce nouvel utilisateur ?")
    print("1. Utilisateur standard (Médecin, infirmier...)")
    print("2. Administrateur réseau (Marseille, Rennes, Grenoble)")
    choix_role = input("Votre choix (1 ou 2) : ")

    role_a_attribuer = "user"

    if choix_role == "2":
        if current_user_role == "superadmin":
            role_a_attribuer = "admin"
            print("Création d'un Administrateur.")
        else:
            print("Seul le superadmin peut créer d'autres administrateurs.")
            print("Création annulée.")
            cursor.close()
            connexion.close()
            return

    regex = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')  # {min,max}  #compile pour definir un motif
    resultat = regex.search(mail)

    if resultat:
        if not nom or not prenom:
            print("des info sont vides")
        else:
            base_login = (prenom[0] + nom).lower()
            login_genere = base_login
            suffixe = 0

            while True:
                cursor.execute("SELECT id FROM users WHERE login = %s", (login_genere,))
                if cursor.fetchone() is None:
                    break
                suffixe += 1
                login_genere = f"{base_login}{suffixe}"

            chars = string.ascii_letters + string.digits + string.punctuation
            password_air = "".join(random.choice(chars) for _ in range(12))

            password_bytes = password_air.encode('utf-8')
            password_hash_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            password_hash_bdd = password_hash_bytes.decode('utf-8')

            print(f"--> LOGIN : {login_genere}")
            print(f"--> PASSWORD : {password_air}")  # On affiche le mot de passe en clair pour le noter

            try:
                cursor.execute(
                    "INSERT INTO users (nom, prenom, mail, login, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nom, prenom, mail, login_genere, password_hash_bdd, role_a_attribuer)
                )
                connexion.commit()
                print(f"L'utilisateur (Rôle: {role_a_attribuer}) a été rajouté")
            except Exception as e:
                print(f"Erreur d'insertion dans la BDD: {e}")
                print("L'utilisateur n'a pas été ajouté.")

            finally:
                envoie_mail(mail,login_genere,password_air)
                cursor.close()
                connexion.close()
    else:
        print("veillez saisir une addrese mail correct")

# add_user()