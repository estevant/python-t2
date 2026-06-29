import datetime

FICHIER_LOG = "journal_activite.log"


def ecrire_log(message, fichier=FICHIER_LOG):
    # journal d'activite horodate, commun a tous les modules T3
    horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = f"[{horodatage}] {message}"
    try:
        with open(fichier, "a", encoding="utf-8") as f:
            f.write(ligne + "\n")
    except Exception as e:
        print(f"Erreur d ecriture dans le journal : {e}")
    return ligne
