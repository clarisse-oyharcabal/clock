import time
import os
from threading import Thread, Lock

current_time = (0, 0, 0)
alarm = None
paused = False
format_24h = True
lock = Lock()
displaying_time = False

def display_time():
    global current_time, format_24h
    while True:
        if displaying_time:  # Affiche l'heure uniquement si la variable est True
            os.system('cls' if os.name == 'nt' else 'clear')
            hours, minutes, seconds = current_time
            if not format_24h:
                suffix = "AM" if hours < 12 else "PM"
                hours = hours % 12 if hours % 12 != 0 else 12
                print(f"{hours:02}:{minutes:02}:{seconds:02} {suffix}", end="", flush=True)
            else:
                print(f"{hours:02}:{minutes:02}:{seconds:02}", end="", flush=True)
            time.sleep(1)
        else:
            time.sleep(1)

def set_time(new_time: tuple):
    global current_time
    try:
        hours, minutes, seconds = new_time
        if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
            current_time = new_time
        else:
            raise ValueError
    except ValueError:
        print("Error: Please enter a valid time in the format (hh, mm, ss).")

def set_alarm(alarm_time: tuple):
    global alarm
    try:
        hours, minutes, seconds = alarm_time
        if 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60:
            alarm = alarm_time
            print(f"Alarm set for {hours:02}:{minutes:02}:{seconds:02}.")
        else:
            raise ValueError
    except ValueError:
        print("Error: Please enter a valid time in the format (hh, mm, ss).")

def check_alarm():
    global current_time, alarm
    if alarm and current_time == alarm:
        print("\nAlarm! It's time!\n")
        alarm = None

def toggle_pause():
    global paused
    with lock:
        paused = not paused
        if paused:
            print("\nClock paused.")
        else:
            print("\nClock resumed.")

def toggle_format():
    global format_24h
    format_24h = not format_24h
    format_type = "12-hour" if not format_24h else "24-hour"
    print(f"\nFormat changed to {format_type}.")

def clock():
    global current_time, paused
    while True:
        with lock:
            if not paused and displaying_time:
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
                check_alarm()
        time.sleep(1)

def menu():
    global displaying_time
    while True:
        print("\nMenu:")
        print("1: Set time")
        print("2: Set alarm")
        print("3: Change format 12-hour/24-hour")
        print("4: Pause/Resume clock")
        print("5: Start/Stop displaying time")
        print("6: Exit")
        
        try:
            choice = input("Your choice: ")
        except KeyboardInterrupt:
            print("\nExiting menu...")
            break

        if choice == "1":
            time_input = input("Enter time in the format hh:mm:ss: ")
            try:
                hours, minutes, seconds = map(int, time_input.split(":"))
                set_time((hours, minutes, seconds))
            except ValueError:
                print("Error: Invalid format.")
        elif choice == "2":
            alarm_input = input("Enter alarm time in the format hh:mm:ss: ")
            try:
                hours, minutes, seconds = map(int, alarm_input.split(":"))
                set_alarm((hours, minutes, seconds))
            except ValueError:
                print("Error: Invalid format.")
        elif choice == "3":
            toggle_format()
        elif choice == "4":
            toggle_pause()
        elif choice == "5":
            displaying_time = not displaying_time
            if displaying_time:
                print("Started displaying time.")
            else:
                print("Stopped displaying time.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    time_input = input("Enter the initial time in the format hh:mm:ss: ")
    try:
        hours, minutes, seconds = map(int, time_input.split(":"))
        set_time((hours, minutes, seconds))
    except ValueError:
        print("Error: Invalid format. Default time is set to 00:00:00.")

    clock_thread = Thread(target=clock, daemon=True)
    clock_thread.start()

    display_time_thread = Thread(target=display_time, daemon=True)
    display_time_thread.start()

    while True:
        input("\nPress Enter to open the menu...")  # Attente de l'utilisateur pour ouvrir le menu
        menu()  # Appel du menu
