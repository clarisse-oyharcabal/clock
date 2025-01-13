import time
import threading
from colorama import Fore, Style, init
import os
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Global variables
current_time = (0, 0, 0)
alarm_time = None
is_24_hour_format = True
is_paused = False
time_lock = threading.Lock()  # Lock to handle time updates and user input without interference

def afficher_heure(heure_tuple):
    """Set the current time."""
    global current_time
    with time_lock:
        current_time = heure_tuple

def set_alarm(heure_tuple):
    """Set an alarm time."""
    global alarm_time
    alarm_time = heure_tuple
    print(Fore.GREEN + f"⏰ Alarm set for {format_time(alarm_time)}")

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
    print(Fore.CYAN + f"Time format switched to {'24-hour' if is_24_hour_format else '12-hour AM/PM'} 🕰️")

def toggle_pause():
    """Pause or resume the clock."""
    global is_paused
    is_paused = not is_paused
    print(Fore.YELLOW + ("⏸️  Clock paused. You can now set the time or alarm." if is_paused else "▶️  Clock resumed."))

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

            # Clear the screen for cleaner display, but do not clear menu
            os.system('cls' if os.name == 'nt' else 'clear')

            # Display the current time with a placeholder for menu
            print(Fore.MAGENTA + f"🕒 Current time: {format_time(current_time)} 🕰️")
            print(Fore.BLUE + Style.BRIGHT + "\n=== 🕑 Clock Menu ===")
            print(Fore.CYAN + "✨ Please pause the clock (option 4) before making any settings!")
            print(Fore.YELLOW + "1. 🕐 Set Time")
            print(Fore.YELLOW + "2. ⏰ Set Alarm")
            print(Fore.YELLOW + "3. 🕰️ Toggle Time Format (12/24 Hour)")
            print(Fore.YELLOW + "4. ⏸️ Pause/Resume Clock")
            print(Fore.RED + "5. 🚪 Exit")
            print(Fore.GREEN + "6. 🖥️ Set Time from Computer")

        time.sleep(1)

def display_input_prompt():
    """Keep the input prompt visible until a valid choice is made."""
    while True:
        choice = input(Fore.YELLOW + "🔑 Choose an option: ").strip()
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        else:
            print(Fore.RED + "❌ Invalid choice. Please try again.")

def set_time_from_computer():
    """Set the time based on the system's current time."""
    global current_time
    system_time = datetime.now()
    hours = system_time.hour
    minutes = system_time.minute
    seconds = system_time.second
    afficher_heure((hours, minutes, seconds))
    print(Fore.GREEN + f"✅ Time set to current system time: {format_time(current_time)}")

def main():
    # Start the clock in a separate thread
    clock_thread = threading.Thread(target=update_time, daemon=True)
    clock_thread.start()

    while True:
        choice = display_input_prompt()  # Prompt user for a choice

        if choice == "1":
            try:
                h, m, s = map(int, input(Fore.GREEN + "🕘 Enter time (hh:mm:ss): ").split(":"))
                afficher_heure((h, m, s))
                print(Fore.CYAN + f"✅ Time set to {format_time(current_time)}")
            except ValueError:
                print(Fore.RED + "❌ Invalid time format. Please use hh:mm:ss.")

        elif choice == "2":
            try:
                h, m, s = map(int, input(Fore.GREEN + "🕓 Enter alarm time (hh:mm:ss): ").split(":"))
                set_alarm((h, m, s))
            except ValueError:
                print(Fore.RED + "❌ Invalid time format. Please use hh:mm:ss.")

        elif choice == "3":
            toggle_time_format()

        elif choice == "4":
            toggle_pause()

        elif choice == "5":
            print(Fore.YELLOW + "👋 Goodbye!")
            break

        elif choice == "6":
            set_time_from_computer()

if __name__ == "__main__":
    main()
