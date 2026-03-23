from connexion_bdd import get_connection 

def maj_user():
    connexion = get_connection()
    
    if connexion is None:
        return 

    cursor = connexion.cursor() #cursor methode que j'applique sur mon objet conn et qui permet de renvoyer a la bdd les commandes sql

    # print("connexion établie")
    choix=input("1.modif prenom \n2.modif mail : \n ")
        
    if choix=="1":
            user_a_changer=input("quel est le nom de l utilisateur que vous voulez mettre a jour? : \n")
            prenom_a_changer=input("saisir le prenom a changer : ")
            cursor.execute("UPDATE users SET prenom= %s  WHERE nom = %s",(prenom_a_changer,user_a_changer,))
    elif choix=="2":
            user_a_changer=input("quel est le nom de l utilisateur que vous voulez mettre a jour? : \n")
            mail_a_changer=input("saisir le nouveau mail : ")
            cursor.execute("UPDATE users SET mail= %s  WHERE nom = %s",(mail_a_changer,user_a_changer,))
    else:
            print("on ne comprend pas la demande")
       
    connexion.commit()
    print("la mise a jour a ete prise en compte")
    
    cursor.close()
    connexion.close()

        
  
# maj_user()