from connexion_bdd import get_connection
import bcrypt

def login_system():
    connexion = get_connection()
    if connexion is None:
        return None

    print("\nAuthentification requise")
    login_saisi = input("Login : ")
    password_saisi = input("Mot de passe : ")

    cursor = connexion.cursor()
    sql = "SELECT nom, role, password FROM users WHERE login = %s"
    cursor.execute(sql, (login_saisi,))

    user_trouve = cursor.fetchone()

    cursor.close()
    connexion.close()

    if user_trouve:
        nom_user = user_trouve[0]
        role_user = user_trouve[1]
        password_hash_bdd = user_trouve[2]

        if bcrypt.checkpw(password_saisi.encode('utf-8'), password_hash_bdd.encode('utf-8')):
            print(f"Bienvenue {nom_user} (Vous êtes connecté en tant que : {role_user})")
            return role_user
        else:
            print("Identifiants incorrects.")
            return None
    else:
        print("Identifiants incorrects.")
        return None