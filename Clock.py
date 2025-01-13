import time

def horloge_avec_alarme():
    print("Horloge avec alarme")
    print("---------------------")

    # Saisie de l'heure initiale
    try:
        heure_actuelle = input("Entrez l'heure de départ (HH:MM:SS): ")
        parts = heure_actuelle.split(':')
        if len(parts) != 3:
            raise ValueError
        heure_actuelle = (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        print("Format incorrect. Veuillez utiliser HH:MM:SS.")
        return

    # Saisie de l'heure de l'alarme
    try:
        heure_alarme = input("Entrez l'heure de l'alarme (HH:MM:SS): ")
        parts = heure_alarme.split(':')
        if len(parts) != 3:
            raise ValueError
        heure_alarme = (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        print("Format incorrect. Veuillez utiliser HH:MM:SS.")
        return

    print("Alarme réglée pour: {:02d}:{:02d}:{:02d}".format(*heure_alarme))
    print("Appuyez sur Ctrl+C pour arrêter l'horloge.")

    try:
        while True:
            # Afficher l'heure actuelle
            print("Heure actuelle: {:02d}:{:02d}:{:02d}".format(*heure_actuelle), end="\r")

            # Vérifier si l'heure actuelle correspond à l'heure de l'alarme
            if heure_actuelle == heure_alarme:
                print("\nC'est l'heure de l'alarme!")

            # Mettre à jour l'heure actuelle
            heures, minutes, secondes = heure_actuelle
            secondes += 1
            if secondes == 60:
                secondes = 0
                minutes += 1
            if minutes == 60:
                minutes = 0
                heures += 1
            if heures == 24:
                heures = 0

            heure_actuelle = (heures, minutes, secondes)

            # Attendre une seconde
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nHorloge arrêtée.")

if __name__ == "__main__":
    horloge_avec_alarme()
     













