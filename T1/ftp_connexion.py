from ftplib import FTP, error_perm, error_temp
from config_ftp import (
    FTP_HOST, FTP_PORT, FTP_USER, FTP_PASS, FTP_TIMEOUT
)


def connecter_ftp(host=None, port=None, user=None, passwd=None, timeout=None):
    host = host or FTP_HOST
    port = port or FTP_PORT
    user = user or FTP_USER
    passwd = passwd or FTP_PASS
    timeout = timeout or FTP_TIMEOUT

    try:
        ftp = FTP()
        ftp.connect(host=host, port=port, timeout=timeout)
        ftp.login(user=user, passwd=passwd)
        ftp.encoding = "utf-8"
        print(f"[OK] Connecté au serveur FTP {host}:{port} en tant que '{user}'")
        print(f"     Message serveur : {ftp.getwelcome()}")
        return ftp

    except error_perm as e:
        raise ConnectionError(f"[ERREUR] Authentification refusée : {e}")
    except error_temp as e:
        raise ConnectionError(f"[ERREUR] Erreur temporaire serveur : {e}")
    except OSError as e:
        raise ConnectionError(f"[ERREUR] Impossible de joindre {host}:{port} : {e}")


def deconnecter_ftp(ftp):
    if ftp is None:
        print("[AVERTISSEMENT] Aucune connexion FTP à fermer.")
        return False

    try:
        ftp.quit()
        print("[OK] Déconnexion FTP propre (QUIT).")
        return True
    except Exception:
        try:
            ftp.close()
            print("[OK] Déconnexion FTP forcée (CLOSE).")
            return True
        except Exception as e:
            print(f"[ERREUR] Échec de la déconnexion : {e}")
            return False


if __name__ == "__main__":
    print("=== Test de connexion FTP ===")
    try:
        session = connecter_ftp()
        print(f"Répertoire courant : {session.pwd()}")
        deconnecter_ftp(session)
    except ConnectionError as e:
        print(e)
