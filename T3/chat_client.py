import socket
import sys
import threading

HOTE = "127.0.0.1"
PORT = 5050
TAILLE_BUFFER = 1024


def recevoir_messages(sock):
    # thread d'ecoute des messages du serveur/des autres clients
    while True:
        try:
            message = sock.recv(TAILLE_BUFFER)
            if not message:
                print(">>> Connexion fermee par le serveur")
                break
            print(message.decode())
        except Exception:
            break


def lancer_client_chat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOTE, PORT))
    except socket.error as e:
        print(f"La connexion a echoue : {e}")
        sys.exit()

    pseudo = input("Saisir votre pseudo : ").strip()
    sock.send(pseudo.encode())

    print(">>> Connexion etablie, tapez FIN pour quitter")

    thread_ecoute = threading.Thread(target=recevoir_messages, args=(sock,), daemon=True)
    thread_ecoute.start()

    while True:
        message = input("")
        sock.send(message.encode())
        if message.upper() == "FIN":
            break

    print(">>> Fermeture de la connexion")
    sock.close()


if __name__ == "__main__":
    lancer_client_chat()
