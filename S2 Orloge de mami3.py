import time
import threading
from colorama import Fore, Style, init
import os
from datetime import datetime

# Install and import playsound for alarm functionality
try:
    from playsound import playsound
except ImportError:
    print("Installing playsound...")
    os.system("pip install playsound")
    from playsound import playsound

# Initialize colorama
init(autoreset=True)

# Global variables
current_time = (0, 0, 0)
alarm_time = None
is_24_hour_format = True
is_paused = False
is_alarm_active = False
time_lock = threading.Lock()  # Lock to handle time updates and user input without interference

alarm_sound = "malarm.mp3"  # Path to alarm sound file (ensure you have this file)

def afficher_heure(heure_tuple):
    """Set the current time."""
    global current_time
    with time_lock:
        current_time = heure_tuple

def set_alarm(heure_tuple):
    """Set an alarm time."""
    global alarm_time, is_alarm_active
    alarm_time = heure_tuple
    is_alarm_active = True
    print(Fore.GREEN + f"⏰ Alarme réglée pour {format_time(alarm_time)}")

def format_time(heure_tuple):
    """Format time in 12-hour or 24-hour format."""
    hours, minutes, seconds = heure_tuple
    if not is_24_hour_format:
        period = "AM" if hours < 12 else "PM"
        hours = hours % 12 if hours % 12 != 0 else 12
        return f"{hours:02}:{minutes:02}:{seconds:02} {period}"
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def toggle_time_format():
    """Toggle between 12-hour and 24-hour format."""
    global is_24_hour_format
    is_24_hour_format = not is_24_hour_format
    print(Fore.CYAN + f"Le format d'heure est maintenant {'24 heures' if is_24_hour_format else '12 heures AM/PM'} 🕰️")

def toggle_pause():
    """Pause or resume the clock."""
    global is_paused, is_alarm_active
    is_paused = not is_paused
    if is_paused:
        is_alarm_active = False  # Stop the alarm when paused
    print(Fore.YELLOW + ("⏸️  Horloge en pause. Vous pouvez maintenant régler l'heure ou l'alarme." if is_paused else "▶️  Horloge reprise."))

def check_alarm():
    """Check if the current time matches the alarm time and play a sound if it does."""
    global current_time, alarm_time, is_alarm_active
    while True:
        with time_lock:
            if is_alarm_active and alarm_time and current_time == alarm_time:
                print(Fore.RED + "⏰ Alarme ! Il est temps !")
                while is_alarm_active:
                    try:
                        playsound(alarm_sound)
                    except Exception as e:
                        print(Fore.RED + f"Erreur lors de la lecture du son : {e}")
                    print(Fore.RED + "⏰ Alarme en cours. Appuyez sur 4 pour arrêter.")
                    time.sleep(2)  # Beeping interval
                alarm_time = None  # Reset the alarm after stopping
        time.sleep(1)

def update_time():
    """Continuously update the time."""
    global current_time, is_paused
    while True:
        if not is_paused:
            with time_lock:
                hours, minutes, seconds = current_time
                seconds += 1
                if seconds == 60:
                    seconds = 0
                    minutes += 1
                if minutes == 60:
                    minutes = 0
                    hours += 1
                if hours == 24:
                    hours = 0
                current_time = (hours, minutes, seconds)

            # Clear the screen for cleaner display
            os.system('cls' if os.name == 'nt' else 'clear')

            # Display the current time and menu
            print(Fore.MAGENTA + Style.BRIGHT + "👵 L’horloge de mamie")  # Added old woman emoji
            print(Fore.MAGENTA + Style.BRIGHT + "Montre folle 🤪🤯🎉, montre folle 🤪🤯🎉, montre folle 🤪🤯🎉!")  # Crazy emojis
            print(Fore.MAGENTA + f"🕒 Heure actuelle : {format_time(current_time)} 🕰️")
            print(Fore.BLUE + Style.BRIGHT + "\n=== 🕑 Menu de l'horloge ===")
            print(Fore.CYAN + "✨ Veuillez mettre l'horloge en pause (option 4) avant de faire des réglages !")
            print(Fore.YELLOW + "1. 🕐 Régler l'heure")
            print(Fore.GREEN + "2. ⏰ Régler l'alarme")
            print(Fore.CYAN + "3. 🕰️ Basculer le format de l'heure (12/24 heures)")
            print(Fore.MAGENTA + "4. ⏸️ Mettre en pause/Reprendre l'horloge")
            print(Fore.BLUE + "5. 🖥️ Régler l'heure depuis l'ordinateur")
            print(Fore.RED + "6. 🚪 Quitter")

        time.sleep(1)

def display_input_prompt():
    """Keep the input prompt visible until a valid choice is made."""
    while True:
        choice = input(Fore.YELLOW + "🔑 Choisissez une option : ").strip()
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        else:
            print(Fore.RED + "❌ Choix invalide. Veuillez réessayer.")

def set_time_from_computer():
    """Set the time based on the system's current time."""
    global current_time
    system_time = datetime.now()
    hours = system_time.hour
    minutes = system_time.minute
    seconds = system_time.second
    afficher_heure((hours, minutes, seconds))
    print(Fore.GREEN + f"✅ Heure réglée sur l'heure actuelle de l'ordinateur : {format_time(current_time)}")

def main():
    # Start the clock in a separate thread
    clock_thread = threading.Thread(target=update_time, daemon=True)
    clock_thread.start()

    # Start the alarm checker in a separate thread
    alarm_thread = threading.Thread(target=check_alarm, daemon=True)
    alarm_thread.start()

    while True:
        choice = display_input_prompt()  # Prompt user for a choice

        if choice == "1":
            try:
                h, m, s = map(int, input(Fore.GREEN + "🕘 Entrez l'heure (hh:mm:ss) : ").split(":"))
                afficher_heure((h, m, s))
                print(Fore.CYAN + f"✅ Heure réglée à {format_time(current_time)}")
            except ValueError:
                print(Fore.RED + "❌ Format de l'heure invalide. Veuillez utiliser hh:mm:ss.")

        elif choice == "2":
            try:
                h, m, s = map(int, input(Fore.GREEN + "🕓 Entrez l'heure de l'alarme (hh:mm:ss) : ").split(":"))
                set_alarm((h, m, s))
            except ValueError:
                print(Fore.RED + "❌ Format de l'heure invalide. Veuillez utiliser hh:mm:ss.")

        elif choice == "3":
            toggle_time_format()

        elif choice == "4":
            toggle_pause()

        elif choice == "5":
            set_time_from_computer()

        elif choice == "6":
            print(Fore.YELLOW + "👋 Au revoir !")
            break

if __name__ == "__main__":
    main()
