from connexion_bdd import get_connection

def delete_user():
    connexion = get_connection()
    if connexion is None:
        return

    cursor = connexion.cursor()
    print("connexion établie")
    supp_login=input("saisir le login de l'utilisateur : ")
    cursor.execute("DELETE FROM users WHERE login = %s",(supp_login,))

    connexion.commit()
    print("l utilisateur a ete supprime")

    cursor.close()
    connexion.close()

# delete_user()