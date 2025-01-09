import time
from datetime import datetime, timedelta

class Horloge:
    def __init__(self):
        self.heure_actuelle = datetime.now().replace(microsecond=0)
        self.alarme = None

    def afficher_heure(self):
        self.heure_actuelle = datetime.now().replace(microsecond=0)
        print(f"\r{self.heure_actuelle.strftime('%H:%M:%S')}", end="", flush=True)

    def regler_heure(self, nouvelle_heure):
        try:
            heures, minutes, secondes = nouvelle_heure
            self.heure_actuelle = self.heure_actuelle.replace(hour=heures, minute=minutes, second=secondes)
        except ValueError:
            print("Erreur : Veuillez entrer une heure valide sous la forme (heures, minutes, secondes).")

    def regler_alarme(self, heure_alarme):
        try:
            heures, minutes, secondes = heure_alarme
            alarme_temp = self.heure_actuelle.replace(hour=heures, minute=minutes, second=secondes)
            if alarme_temp <= self.heure_actuelle:
                alarme_temp += timedelta(days=1)  # Alarme pour le jour suivant
            self.alarme = alarme_temp
            print(f"Alarme réglée à {self.alarme.strftime('%Y-%m-%d %H:%M:%S')}.")
        except ValueError:
            print("Erreur : Veuillez entrer une heure valide sous la forme (heures, minutes, secondes).")

    def verifier_alarme(self):
        if self.alarme and self.heure_actuelle >= self.alarme:
            print("\nAlarme ! Il est l'heure !\n")
            self.alarme = None

    def demarrer(self):
        try:
            while True:
                self.afficher_heure()
                self.verifier_alarme()
                self.heure_actuelle += timedelta(seconds=1)
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nHorloge arrêtée.")

# Exemple d'utilisation
if __name__ == "__main__":
    horloge = Horloge()

    horloge.regler_heure((16, 30, 0))  # Réglage de l'heure actuelle
    horloge.regler_alarme((16, 30, 10))  # Réglage de l'alarme

from threading import Thread

def gestion_pause(horloge):
        while True:
            input("\nAppuyez sur Entrée pour mettre en pause/reprendre...")
            horloge.mettre_en_pause()

Thread(target=gestion_pause, args=(horloge,), daemon=True).start()
horloge.demarrer()

