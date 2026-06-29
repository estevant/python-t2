import socket
import threading

from journal_log import ecrire_log

HOTE = "0.0.0.0"
PORT = 5050
NB_CLIENTS_MAX = 4
TAILLE_BUFFER = 1024

clients_connectes = {}  # socket -> pseudo
verrou_clients = threading.Lock()


def diffuser_message(message, expediteur=None):
    # envoie le message a tous les clients connectes, sauf l'expediteur
    with verrou_clients:
        for client_socket in list(clients_connectes.keys()):
            if client_socket is expediteur:
                continue
            try:
                client_socket.send(message.encode())
            except Exception as e:
                ecrire_log(f"Erreur d'envoi a un client : {e}")


def gerer_client(client_socket, adresse):
    # un thread par client connecte
    try:
        pseudo = client_socket.recv(TAILLE_BUFFER).decode().strip()
        with verrou_clients:
            clients_connectes[client_socket] = pseudo

        print(f">>> {pseudo} ({adresse[0]}:{adresse[1]}) a rejoint le chat")
        ecrire_log(f"Connexion de {pseudo} depuis {adresse[0]}:{adresse[1]}")
        diffuser_message(f"*** {pseudo} a rejoint le chat ***", client_socket)

        while True:
            message = client_socket.recv(TAILLE_BUFFER)
            if not message or message.decode().upper() == "FIN":
                break
            texte = message.decode()
            print(f"{pseudo} : {texte}")
            ecrire_log(f"{pseudo} : {texte}")
            diffuser_message(f"{pseudo} : {texte}", client_socket)

    except Exception as e:
        ecrire_log(f"Exception avec le client {adresse} : {e}")

    finally:
        with verrou_clients:
            pseudo_parti = clients_connectes.pop(client_socket, "inconnu")
        diffuser_message(f"*** {pseudo_parti} a quitte le chat ***", client_socket)
        print(f">>> {pseudo_parti} a quitte le chat")
        ecrire_log(f"Deconnexion de {pseudo_parti}")
        client_socket.close()


def lancer_serveur_chat():
    socket_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        socket_principale.bind((HOTE, PORT))
        socket_principale.listen(NB_CLIENTS_MAX)
    except Exception as e:
        print(f"Erreur au demarrage du serveur : {e}")
        ecrire_log(f"Erreur au demarrage du serveur de chat : {e}")
        return

    print(f">>> Serveur de chat pret sur le port {PORT}, en attente des clients...")
    print(">>> Ctrl+C pour arreter le serveur")
    ecrire_log(f"Serveur de chat demarre sur le port {PORT}")

    try:
        while True:
            client_socket, adresse = socket_principale.accept()
            thread_client = threading.Thread(target=gerer_client, args=(client_socket, adresse))
            thread_client.start()
    except KeyboardInterrupt:
        print(">>> Arret du serveur demande")
        ecrire_log("Arret manuel du serveur de chat")
    finally:
        socket_principale.close()


if __name__ == "__main__":
    lancer_serveur_chat()
