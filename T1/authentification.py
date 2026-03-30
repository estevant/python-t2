from connexion_bdd import get_connection
import bcrypt

# fonction de connexion
def login_system():
    connexion = get_connection()
    if connexion is None:
        return None

    cursor = connexion.cursor()

    max_tentatives = 3
    tentatives = 0

    jours_expiration = 90

    # On vérifie si la date actuelle dépasse date_modification_password + jours_expiration
    sql_check_expiration = """SELECT EXISTS(SELECT 1 FROM users WHERE login = %s AND date_modification_password IS NOT NULL AND NOW() > DATE_ADD(date_modification_password, INTERVAL %s DAY))"""

    while tentatives < max_tentatives:
        print("\nAuthentification requise")
        login_saisi = input("Login : ")
        password_saisi = input("Mot de passe : ")

        sql_select_user = "SELECT nom, role, password FROM users WHERE login = %s"
        cursor.execute(sql_select_user, (login_saisi,))

        user_trouve = cursor.fetchone()

        if user_trouve:
            nom_user = user_trouve[0]
            role_user = user_trouve[1]
            password_hash_bdd = user_trouve[2]

            #vérifie que le mot de passe saisi correspond au hash
            if bcrypt.checkpw(password_saisi.encode('utf-8'),password_hash_bdd.encode('utf-8')):

                #vérifie si le mot de passe a expiré
                cursor.execute(sql_check_expiration, (login_saisi, jours_expiration))
                is_expired = cursor.fetchone()[0]

                if is_expired:
                    print(
                        f"\n/!\\ Votre mot de passe a expiré (plus de {jours_expiration} jours).")
                    print("Vous devez obligatoirement le modifier pour continuer.\n")

                    #saisie du nouveau mdp
                    while True:
                        new_pass = input("Nouveau mot de passe : ")
                        confirm_pass = input("Confirmez le mot de passe : ")

                        if new_pass != confirm_pass:
                            print("Erreur : Les mots de passe ne correspondent pas.")
                            continue

                        if new_pass == password_saisi:
                            print("Erreur : Le nouveau mot de passe doit être différent de l'ancien.")
                            continue

                        if not new_pass:
                            print("Erreur : Le mot de passe ne peut pas être vide.")
                            continue

                        try:
                            new_hash = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                            cursor.execute(
                                "UPDATE users SET password = %s, date_modification_password = NOW() WHERE login = %s",
                                (new_hash, login_saisi)
                            )
                            connexion.commit()
                            print("Succès : Mot de passe mis à jour.")
                            break

                        except Exception as e:
                            print(f"Erreur lors de la mise à jour : {e}")
                            return None

                print(f"Bienvenue {nom_user} (Vous êtes connecté en tant que : {role_user})")
                cursor.close()
                connexion.close()
                return role_user, login_saisi
            else:
                print("Identifiants incorrects.")
        else:
            print("Identifiants incorrects.")

        tentatives += 1  # rajoute une tentative au compteur quand il y a un echec

        if tentatives < max_tentatives:
            print(f"Tentative {tentatives}/{max_tentatives} échouée.")
        else:
            print("Nombre de tentatives dépassé. Fin du programme.")

    cursor.close()
    connexion.close()
    return None