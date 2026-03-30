from interaction_user import add_user
from afficher_utilisateur import show_user
from suppression_utilisateur import delete_user
from mise_a_jour import maj_user
from authentification import login_system

def affichage_menu():
    resultat_login = login_system()
    if resultat_login is None:
        print("Programme arrêté")
        return

    #extrait du rôle et du login de l'user
    role_connecte = resultat_login[0]
    login_connecte = resultat_login[1]

    #acces refusé si user
    if role_connecte == "user":
        print("Accès refusé")
        return

    while True:
        print("""
         1. Ajouter un utilisateur
         2. Mise à jour sur les données
         3. Suppression du compte
         4. Consultation
         0. Quitter : """)

        choix=input("Selectionnez une option presente sur le menu : ")

        match choix:

            case '1':
                print('Vous avez séléctionné l option ajouter un user')
                add_user(role_connecte)

            case '2':
                print('Vous avez séléctionné l option faire une mise a jour')
                maj_user(login_connecte, role_connecte)

            case '3':
                print('Vous avez séléctionné l option supprimer un compte')
                delete_user(login_connecte, role_connecte)

            case '4':
                print("consulter la BDD")
                show_user()

            case '0':
                print("Vous avez quitté le programme")
                return

            case _:
                print("---->je ne comprend pas la demande")

affichage_menu()


