from ftplib import FTP, error_perm

def get_ftp_connection():
    try:
        config = {
            'host': "127.0.0.1",
            'port': 21,
            'user': "admin_paris",
            'passwd': "paris"
        }

        ftp = FTP()
        ftp.connect(config['host'], config['port'])
        ftp.login(config['user'], config['passwd'])
        print("on est connecte au serveur FTP")
        return ftp

    except error_perm as e:
        print(f"Erreur: Faux nom d'utilisateur ou mot de passe FTP. ({e})")
        return None
    except ConnectionRefusedError:
        print("Erreur: Le serveur FTP refuse la connexion. Verifiez qu'il est bien lance.")
        return None
    except Exception as e:
        print(f"Erreur de connexion FTP: {e}")
        return None
