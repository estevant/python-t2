import socket
import threading
import ipaddress

from chrono import demarrer_chrono, arreter_chrono
from journal_log import ecrire_log


def resoudre_dns(nom_machine):
    # nom/URL --> adresse IP (IPv4 ou IPv6)
    try:
        ip = socket.gethostbyname(nom_machine)
        return ip
    except socket.error as e:
        ecrire_log(f"Erreur resolution DNS de {nom_machine} : {e}")
        return None


def resoudre_reverse_dns(adresse_ip):
    # adresse IP --> nom/URL (reverse DNS)
    try:
        infos = socket.gethostbyaddr(adresse_ip)
        return infos[0]
    except socket.error as e:
        ecrire_log(f"Erreur reverse DNS de {adresse_ip} : {e}")
        return None


def tester_hote_actif(adresse_ip, port=80, timeout=0.5):
    # teste si une machine repond sur un port (a defaut de ping ICMP, plus simple en socket)
    try:
        famille = socket.AF_INET6 if ":" in adresse_ip else socket.AF_INET
        sock = socket.socket(famille, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((adresse_ip, port))
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False
    except Exception as e:
        ecrire_log(f"Exception test hote {adresse_ip} : {e}")
        return False


def scanner_ip_specifique():
    ip = input("Saisir l'adresse IP a scanner : ").strip()

    debut = demarrer_chrono()
    actif = tester_hote_actif(ip)
    duree = arreter_chrono(debut, f"Scan IP {ip}")

    etat = "actif" if actif else "inactif/injoignable"
    print(f"La machine {ip} est {etat}")
    ecrire_log(f"Scan IP specifique {ip} -> {etat} ({duree:.4f}s)")


def scanner_nom_machine():
    nom = input("Saisir le nom de machine / URL a resoudre (DNS) : ").strip()

    debut = demarrer_chrono()
    ip = resoudre_dns(nom)
    duree = arreter_chrono(debut, f"Resolution DNS de {nom}")

    if ip:
        print(f"L'adresse IP de {nom} est : {ip}")
        ecrire_log(f"Resolution DNS {nom} -> {ip} ({duree:.4f}s)")
    else:
        print(f"Impossible de resoudre {nom}")
        ecrire_log(f"Resolution DNS {nom} -> echec ({duree:.4f}s)")


def _scanner_adresse_thread(adresse_ip, resultats, verrou):
    if tester_hote_actif(str(adresse_ip)):
        nom = resoudre_reverse_dns(str(adresse_ip))
        with verrou:
            resultats.append((str(adresse_ip), nom))


def scanner_plage_adresses():
    reseau_cidr = input("Saisir la plage d'adresses au format CIDR (ex: 192.168.1.0/29) : ").strip()

    try:
        reseau = ipaddress.ip_network(reseau_cidr, strict=False)
    except ValueError as e:
        print(f"Erreur : {e}")
        return

    print("==> Scan de la plage avec threads (1 thread par adresse) ...")
    resultats = []
    verrou = threading.Lock()
    threads = []

    debut = demarrer_chrono()
    try:
        for adresse in reseau.hosts():
            t = threading.Thread(target=_scanner_adresse_thread, args=(adresse, resultats, verrou))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except Exception as e:
        ecrire_log(f"Exception lors du scan de la plage {reseau_cidr} : {e}")
        print(f"Erreur : {e}")
        return

    duree = arreter_chrono(debut, f"Scan plage d'adresses {reseau_cidr}")

    for ip, nom in resultats:
        print(f"  {ip}  ({'reverse DNS : ' + nom if nom else 'pas de reverse DNS'})")
    ecrire_log(f"Scan plage {reseau_cidr} -> {len(resultats)} machine(s) active(s) ({duree:.4f}s)")


def scanner_reseau_complet():
    # scan de tout le reseau/sous-reseau (et vlan associes le cas echeant)
    reseau_cidr = input("Saisir le reseau complet au format CIDR (ex: 192.168.1.0/24) : ").strip()

    try:
        reseau = ipaddress.ip_network(reseau_cidr, strict=False)
    except ValueError as e:
        print(f"Erreur : {e}")
        return

    print(f"==> Scan complet de {reseau} ({reseau.num_addresses} adresses) avec threads ...")
    resultats = []
    verrou = threading.Lock()
    threads = []

    debut = demarrer_chrono()
    try:
        for adresse in reseau.hosts():
            t = threading.Thread(target=_scanner_adresse_thread, args=(adresse, resultats, verrou))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
    except Exception as e:
        ecrire_log(f"Exception lors du scan reseau {reseau_cidr} : {e}")
        print(f"Erreur : {e}")
        return

    duree = arreter_chrono(debut, f"Scan reseau complet {reseau_cidr}")

    print(f"Machines actives trouvees : {len(resultats)}")
    for ip, nom in resultats:
        print(f"  {ip}  ({'reverse DNS : ' + nom if nom else 'pas de reverse DNS'})")
    ecrire_log(f"Scan reseau complet {reseau_cidr} -> {len(resultats)} machine(s) active(s) ({duree:.4f}s)")


def menu_scan_reseau():
    while True:
        print("""
    ===== SCAN RESEAU IPv4/IPv6 =====
         1. Scanner une IP specifique
         2. Scanner un nom de machine (DNS)
         3. Scanner une plage d'adresses (reverse DNS, avec threads)
         4. Scanner tout le reseau/sous-reseau (avec threads)
         0. Retour au menu""")

        choix = input("Selectionnez une option : ").strip()

        match choix:
            case '1':
                scanner_ip_specifique()
            case '2':
                scanner_nom_machine()
            case '3':
                scanner_plage_adresses()
            case '4':
                scanner_reseau_complet()
            case '0':
                print("retour au menu")
                return
            case _:
                print("---->je ne comprend pas la demande")
