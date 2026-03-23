import bcrypt
from T1.connexion_bdd import get_connection


def create_superadmin():
    connexion = get_connection()
    if connexion is None:
        return

    cursor = connexion.cursor()

    pwd_bytes = "root".encode('utf-8')
    hash_final = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode('utf-8')

    try:
        sql = "INSERT INTO users (nom, prenom, mail, login, password, role) VALUES (%s, %s, %s, %s, %s, %s)"
        valeurs = ('Superadmin', 'Superadmin', 'admin.paris@hopital.com', 'sadmin', hash_final, 'superadmin')

        cursor.execute(sql, valeurs)
        connexion.commit()
        print("Superadmin ajouté avec succès.")

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        cursor.close()
        connexion.close()


create_superadmin()