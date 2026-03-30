from ftplib import FTP, error_perm

def get_ftp_connection():
    utilisateur = input("Login FTP : ").strip()
    mot_de_passe = input("Mot de passe FTP : ").strip()

    try:
        ftp = FTP()
        ftp.connect("127.0.0.1", 21)
        ftp.login(utilisateur, mot_de_passe)
        print("on est connecte au serveur FTP")
        return ftp

    except error_perm as e:
        print(f"Erreur: identifiants FTP incorrects. ({e})")
        return None
    except ConnectionRefusedError:
        print("Erreur: serveur FTP inaccessible. Verifiez qu'il est bien lance.")
        return None
    except Exception as e:
        print(f"Erreur de connexion FTP: {e}")
        return None