from connexion_bdd import get_connection

def maj_user(current_user_login, current_user_role):
    connexion = get_connection()

    if connexion is None:
        return

    cursor = connexion.cursor()  # cursor methode que j'applique sur mon objet conn et qui permet de renvoyer a la bdd les commandes sql

    choix = input("1.modif prenom \n2.modif mail : \n ")

    if choix == "1":
        user_a_changer = input("quel est le login de l utilisateur que vous voulez mettre a jour? : \n")
        cursor.execute("SELECT login, role FROM users WHERE login = %s", (user_a_changer,))
        user_trouve = cursor.fetchone()

        if not user_trouve:
            print("aucun utilisateur trouvé avec ce login")
        else:
            login_cible = user_trouve[0]
            role_cible = user_trouve[1]

            #gestion des différentes exception possibles

            if login_cible == current_user_login:
                print("Vous ne pouvez pas modifier votre propre compte.")
            elif role_cible == "admin" and current_user_role != "superadmin":
                print("Seul le superadmin peut modifier un compte administrateur.")
            else:
                prenom_a_changer = input("saisir le nouveau prenom : ")
                cursor.execute("UPDATE users SET prenom = %s WHERE login = %s", (prenom_a_changer, user_a_changer,))
                connexion.commit()
                print("la mise a jour a ete prise en compte")

    #meme chose que le choix 1 mais pour les mails
    elif choix == "2":
        user_a_changer = input("quel est le login  de l utilisateur que vous voulez mettre a jour? : \n")
        cursor.execute("SELECT login, role FROM users WHERE login = %s", (user_a_changer,))
        user_trouve = cursor.fetchone()

        if not user_trouve:
            print("aucun utilisateur trouvé avec ce login")
        else:
            login_cible = user_trouve[0]
            role_cible = user_trouve[1]

            if login_cible == current_user_login:
                print("Vous ne pouvez pas modifier votre propre compte.")
            elif role_cible == "admin" and current_user_role != "superadmin":
                print("Seul le superadmin peut modifier un compte administrateur.")
            else:
                mail_a_changer = input("saisir le nouveau mail : ")
                cursor.execute("UPDATE users SET mail = %s WHERE login = %s", (mail_a_changer, user_a_changer,))
                connexion.commit()
                print("la mise a jour a ete prise en compte")
    else:
        print("on ne comprend pas la demande")

    cursor.close()
    connexion.close()

# maj_user()
#l'admin d'un site peut modifier que les users de son site , Rajouter modif ville et modif nom