import time


def demarrer_chrono():
    return time.time()


def arreter_chrono(debut, libelle=""):
    duree = time.time() - debut
    print(f"==> {libelle} a dure : {duree:.4f} secondes")
    return duree
