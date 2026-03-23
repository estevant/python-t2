from connexion_bdd import get_connection 

def show_user():
    connexion = get_connection()
    cursor = None
    if connexion is None:
        return 
    try:
        cursor = connexion.cursor() #cursor methode que j'applique sur mon objet conn et qui permet de renvoyer a la bdd les commandes sql
        print("connexion établie")
        
        choix = input("quel est le nom de l utilisateur que vous voulez voir?  \n" \
                      "(Si vous voulez tous les voir tapez *) \n :").strip()
        if choix == "*":
            cursor.execute("SELECT * FROM users")
        else:
            cursor.execute("SELECT * FROM users WHERE nom = %s", (choix,))

        resultat = cursor.fetchall()

        for x in resultat:     #pour afficher les resultats un par un 
            print(x)
 
    finally:
        if cursor:
            cursor.close()
        if connexion:
            connexion.close()    

        # connexion.cmd_change_user(nom='', prenom='', mail='')
# show_user()