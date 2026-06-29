import socket
import threading

from chrono import demarrer_chrono, arreter_chrono
from journal_log import ecrire_log

TIMEOUT_PORT = 0.5


def tester_port(hote, port):
    # teste un port unique, renvoie True si ouvert, False sinon
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT_PORT)
        sock.connect((hote, port))
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False
    except Exception as e:
        ecrire_log(f"Exception sur le port {port} de {hote} : {e}")
        return False


def scanner_port_specifique():
    hote = input("Saisir l'hote a scanner (IP ou nom) : ").strip()
    try:
        port = int(input("Saisir le port a scanner : ").strip())
    except ValueError:
        print("Erreur : le port doit etre un nombre")
        return

    debut = demarrer_chrono()
    ouvert = tester_port(hote, port)
    duree = arreter_chrono(debut, f"Scan du port {port}")

    etat = "ouvert" if ouvert else "ferme"
    print(f"Le port {port} de {hote} est {etat}")
    ecrire_log(f"Scan port specifique {hote}:{port} -> {etat} ({duree:.4f}s)")


def scanner_plage_ports():
    hote = input("Saisir l'hote a scanner (IP ou nom) : ").strip()
    try:
        debut_plage = int(input("Port de debut : ").strip())
        fin_plage = int(input("Port de fin : ").strip())
    except ValueError:
        print("Erreur : les bornes doivent etre des nombres")
        return

    print("==> Scan sequentiel (sans thread) ...")
    debut = demarrer_chrono()
    ports_ouverts = []
    for port in range(debut_plage, fin_plage + 1):
        if tester_port(hote, port):
            ports_ouverts.append(port)
            print(f"  Le port {port} est ouvert")
    duree = arreter_chrono(debut, f"Scan sequentiel de {hote} [{debut_plage}-{fin_plage}]")

    print(f"Ports ouverts trouves : {ports_ouverts}")
    ecrire_log(f"Scan plage sequentiel {hote}:[{debut_plage}-{fin_plage}] -> "
               f"{ports_ouverts} ({duree:.4f}s)")


def _scanner_port_thread(hote, port, resultats, verrou):
    if tester_port(hote, port):
        with verrou:
            resultats.append(port)


def scanner_tous_ports_thread():
    hote = input("Saisir l'hote a scanner (IP ou nom) : ").strip()
    try:
        debut_plage = int(input("Port de debut : ").strip())
        fin_plage = int(input("Port de fin : ").strip())
    except ValueError:
        print("Erreur : les bornes doivent etre des nombres")
        return

    print("==> Scan simultane (avec threads) ...")
    resultats = []
    verrou = threading.Lock()
    threads = []

    debut = demarrer_chrono()
    try:
        for port in range(debut_plage, fin_plage + 1):
            t = threading.Thread(target=_scanner_port_thread, args=(hote, port, resultats, verrou))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except Exception as e:
        ecrire_log(f"Exception lors du scan thread de {hote} : {e}")
        print(f"Erreur : {e}")
        return

    duree = arreter_chrono(debut, f"Scan simultane (threads) de {hote} [{debut_plage}-{fin_plage}]")

    resultats.sort()
    print(f"Ports ouverts trouves : {resultats}")
    ecrire_log(f"Scan plage threads {hote}:[{debut_plage}-{fin_plage}] -> "
               f"{resultats} ({duree:.4f}s)")


def menu_scan_ports():
    while True:
        print("""
    ===== SCAN DE PORTS =====
         1. Scanner un port specifique
         2. Scanner une plage de ports (sans thread)
         3. Scanner une plage de ports (avec threads)
         0. Retour au menu""")

        choix = input("Selectionnez une option : ").strip()

        match choix:
            case '1':
                scanner_port_specifique()
            case '2':
                scanner_plage_ports()
            case '3':
                scanner_tous_ports_thread()
            case '0':
                print("retour au menu")
                return
            case _:
                print("---->je ne comprend pas la demande")
