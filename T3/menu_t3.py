from scan_ports import menu_scan_ports
from scan_reseau import menu_scan_reseau


def menu_t3():
    while True:
        print("""
    ===== GESTION RESEAU / SYSTEME (T3) =====
         1. Scan de ports
         2. Scan reseau IPv4/IPv6
         3. Lancer le serveur de chat
         4. Lancer un client de chat
         0. Quitter""")

        choix = input("Selectionnez une option presente sur le menu : ").strip()

        match choix:
            case '1':
                print("Vous avez selectionne le scan de ports")
                menu_scan_ports()
            case '2':
                print("Vous avez selectionne le scan reseau")
                menu_scan_reseau()
            case '3':
                print("Vous avez selectionne le serveur de chat")
            case '4':
                print("Vous avez selectionne le client de chat")
            case '0':
                print("Vous avez quitte le programme")
                return
            case _:
                print("---->je ne comprend pas la demande")


if __name__ == "__main__":
    menu_t3()
