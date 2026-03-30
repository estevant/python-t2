import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        config = {
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_DATABASE")
        }
        
        connexion = mysql.connector.connect(**config)
        return connexion

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erreur: Faux nom d'utilisateur ou mot de passe.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erreur: La base de données 'hopital' n'existe pas.")
        else:
            print(f"Erreur de connexion: {err}")
        return None
    
