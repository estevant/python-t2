from connexion_bdd import get_connection

def delete_user(current_user_login, current_user_role):
    connexion = get_connection()
    if connexion is None:
        return

    cursor = connexion.cursor()
    print("connexion établie")
    supp_login=input("saisir le login de l'utilisateur : ")

    cursor.execute("SELECT role FROM users WHERE login = %s",(supp_login,))
    user_trouve = cursor.fetchone()

    if not user_trouve:
        print("aucun utilisateur trouvé avec ce login")
    else:
        role_cible = user_trouve[0]

        #gestion des exception :

        if supp_login == current_user_login:
            print("Vous ne pouvez pas supprimer votre propre compte.")
        elif role_cible == "admin" and current_user_role != "superadmin":
            print("Seul le superadmin peut supprimer un compte administrateur.")
        else:
            cursor.execute("DELETE FROM users WHERE login = %s",(supp_login,))
            connexion.commit()
            print("l utilisateur a ete supprime")

    cursor.close()
    connexion.close()

# delete_user()