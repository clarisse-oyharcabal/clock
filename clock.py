import time
from threading import Thread, Lock
import os

class Horloge:
    def __init__(self):
        self.heure = (0, 0, 0)  # Heure initiale : 00:00:00
        self.alarme = None
        self.arret = False
        self.lock = Lock()

    def afficher_heure(self):
        """
        Affiche l'heure actuelle sous la forme hh:mm:ss.
        """
        while not self.arret:
            with self.lock:
                heures, minutes, secondes = self.heure
                print(f"\r{heures:02}:{minutes:02}:{secondes:02}", end="")
            time.sleep(1)
            self.incrementer_heure()
            self.verifier_alarme()

    def incrementer_heure(self):
        """
        Incrémente l'heure d'une seconde.
        """
        with self.lock:
            heures, minutes, secondes = self.heure
            secondes += 1
            if secondes == 60:
                secondes = 0
                minutes += 1
            if minutes == 60:
                minutes = 0
                heures += 1
            if heures == 24:
                heures = 0
            self.heure = (heures, minutes, secondes)

    def regler_heure(self, nouvelle_heure):
        """
        Met à jour l'heure actuelle avec une nouvelle heure.
        :param nouvelle_heure: tuple (heures, minutes, secondes)
        """
        with self.lock:
            self.heure = nouvelle_heure

    def regler_alarme(self, heure_alarme):
        """
        Définit une alarme.
        :param heure_alarme: tuple (heures, minutes, secondes)
        """
        with self.lock:
            self.alarme = heure_alarme
        print(f"\nAlarme réglée à {heure_alarme[0]:02}:{heure_alarme[1]:02}:{heure_alarme[2]:02}")

    def verifier_alarme(self):
        """
        Vérifie si l'heure actuelle correspond à l'heure de l'alarme.
        Affiche un message si l'alarme est déclenchée.
        """
        with self.lock:
            if self.alarme is not None and self.heure == self.alarme:
                print("\n\n*** Alarme ! Il est temps ! ***\n")
                self.alarme = None  # Désactiver l'alarme après déclenchement

    def demarrer(self):
        """
        Démarre l'horloge dans un thread séparé.
        """
        self.arret = False
        Thread(target=self.afficher_heure, daemon=True).start()

    def arreter(self):
        """
        Arrête l'horloge.
        """
        self.arret = True

def clear_console():
    # Clear the console for better readability
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_menu(horloge):
    clear_console()
    with horloge.lock:
        heures, minutes, secondes = horloge.heure
        print(f"Current Time: {heures:02}:{minutes:02}:{secondes:02}")
    print("\nMenu:")
    print("1. Régler l'heure")
    print("2. Régler l'alarme")
    print("3. Quitter")

def main():
    horloge = Horloge()
    horloge.demarrer()

    try:
        while True:
            afficher_menu(horloge)
            choix = input("Choisissez une option: ")

            if choix == '1':
                heures = int(input("Entrez les heures: "))
                minutes = int(input("Entrez les minutes: "))
                secondes = int(input("Entrez les secondes: "))
                horloge.regler_heure((heures, minutes, secondes))
            elif choix == '2':
                heures = int(input("Entrez les heures pour l'alarme: "))
                minutes = int(input("Entrez les minutes pour l'alarme: "))
                secondes = int(input("Entrez les secondes pour l'alarme: "))
                horloge.regler_alarme((heures, minutes, secondes))
            elif choix == '3':
                horloge.arreter()
                print("\nHorloge arrêtée.")
                break
            else:
                print("Option invalide. Veuillez réessayer.")
    except KeyboardInterrupt:
        horloge.arreter()
        print("\nHorloge arrêtée.")

if __name__ == "__main__":
    main()
