FTP_HOST = "127.0.0.1"
FTP_PORT = 21
FTP_USER = "admin_paris"
FTP_PASS = "paris"
FTP_TIMEOUT = 30

SITES = ["Paris", "Marseille", "Rennes", "Grenoble"]

ARBORESCENCE_SITE = [
    "patients",
    "patients/dossiers_medicaux",
    "patients/ordonnances",
    "administratif",
    "administratif/comptes_rendus",
    "administratif/plannings",
    "sauvegardes",
    "sauvegardes/archives",
]

SAUVEGARDE_JOUR = "friday"
SAUVEGARDE_HEURE = "20:00"
DOSSIER_LOCAL_TEMP = "./temp_ftp"

CLE_CHIFFREMENT_FICHIER = "cle_chiffrement.key"
