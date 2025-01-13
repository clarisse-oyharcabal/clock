import time
import threading
import msvcrt  # To capture keypresses without blocking input (only works on Windows)

# Functions definition : functions to update the time
def afficher_heure(hours, minutes, seconds):  
    seconds += 1 
    if seconds == 60: 
        seconds = 0
        minutes += 1
    if minutes == 60:
        minutes = 0
        hours += 1
    if hours == 24:
        hours = 0
    return hours, minutes, seconds

def format_time(hours, minutes, seconds, format_choice):  
    struct_time = time.struct_time((2025, 1, 6, hours, minutes, seconds, 0, 0, -1))
    if format_choice == '12h':
        return time.strftime("%I:%M:%S %p", struct_time) 
    elif format_choice == '24h':
        return time.strftime("%H:%M:%S", struct_time)  
    else:
        raise ValueError("Invalid format choice!")

def alarm_setting(current_h, current_m, current_s, alarm_h, alarm_m, alarm_s):  
    return (current_h == alarm_h and current_m == alarm_m and current_s == alarm_s)
    
def print_time(formatted_time):  
    print(f"⏲️ The current time is: {formatted_time}", end="\r")
    
def print_alarm_time(alarm_h, alarm_m, alarm_s, format_choice):  
    formatted_alarm = format_time(alarm_h, alarm_m, alarm_s, format_choice)
    print(f"🔔Alarm is set for: {formatted_alarm}")

def set_time():
    while True:
        try:
            hours = int(input("Enter current hour (0 - 23): "))
            if not (0 <= hours < 24):
                print("Hour value out of range. Please try again.")
                continue  

            while True:
                try:
                    minutes = int(input("Enter current minute (0 - 59): "))
                    if not (0 <= minutes < 60):
                        print("Minute value out of range. Please try again.")
                        continue  
                    while True:
                        try:
                            seconds = int(input("Enter current second (0 - 59): "))
                            if not (0 <= seconds < 60):
                                print("Second value out of range. Please try again.")
                                continue  
                            return hours, minutes, seconds
                        except ValueError:
                            print("Invalid input for seconds. Please enter a numeric value between 0 and 59.")
                            continue  
                except ValueError:
                    print("Invalid input for minutes. Please enter a numeric value between 0 and 59.")
                    continue  
        except ValueError:
            print("Invalid input for hours. Please enter a numeric value between 0 and 23.")
            continue  

def set_format():
    while True:
        try:
            format_choice = input("Choose the adequate format (12h / 24h): ").strip().lower()
            if format_choice not in ['12h', '24h']:
                print("Invalid choice, please choose '12h' or '24h'.")
                continue
            return format_choice
        except ValueError as e:
            print(f"Error: {e}")
            continue

def set_alarm(hours, minutes, seconds, format_choice):
    if hours is None or minutes is None or seconds is None:
        print("Please set the current time first.")
        return None, None, None
    if format_choice is None:
        print("Please choose the time format first.")
        return None, None, None
    
    while True:
        try:
            print(f"Please, set the alarm")

            alarm_hour = int(input("Choose the alarm hour (0 - 23): "))
            if not (0 <= alarm_hour < 24):
                print("Alarm hour value out of range. Please try again.")
                continue  

            while True:
                try:
                    alarm_minute = int(input("Choose the alarm minute (0 - 59): "))
                    if not (0 <= alarm_minute < 60):
                        print("Alarm minute value out of range. Please try again.")
                        continue  
                    while True:
                        try:
                            alarm_second = int(input("Choose the alarm second (0 - 59): "))
                            if not (0 <= alarm_second < 60):
                                print("Alarm second value out of range. Please try again.")
                                continue  
                            return alarm_hour, alarm_minute, alarm_second
                        except ValueError:
                            print("Invalid input for alarm seconds. Please enter a numeric value between 0 and 59.")
                            continue  
                except ValueError:
                    print("Invalid input for alarm minutes. Please enter a numeric value between 0 and 59.")
                    continue  
        except ValueError:
            print("Invalid input for alarm hours. Please enter a numeric value between 0 and 23.")
            continue  

def check_keypress():
    """Non-blocking keypress check."""
    while True:
        if msvcrt.kbhit():  # Check if a key is pressed
            key = msvcrt.getch().decode('latin-1').lower()
            return key
        time.sleep(0.1)

def main():
    print("⏲️ Welcome to your Clock !")
    print("\n🚨 Before starting the clock and setting an alarm, please set the time and choose the format.\n")

    hours, minutes, seconds = None, None, None
    format_choice = None
    alarm_hour, alarm_minute, alarm_second = None, None, None

    while True:
        print("\n📖 Main Menu")
        print("1.⏰ Set the current time")
        print("2.🔢 Choose the time format")
        print("3.🔔 Set an alarm (optional)")
        print("4.⛷️Start the clock")
        print("5.❌Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            hours, minutes, seconds = set_time()
        elif choice == '2':
            format_choice = set_format()
        elif choice == '3':
            if hours is None or minutes is None or seconds is None:
                print("You must set the current time first before setting the alarm.")
            elif format_choice is None:
                print("You must choose the time format before setting the alarm.")
            else:
                alarm_hour, alarm_minute, alarm_second = set_alarm(hours, minutes, seconds, format_choice)
                print_alarm_time(alarm_hour, alarm_minute, alarm_second, format_choice)
        elif choice == '4':
            if hours is None or minutes is None or seconds is None:
                print("Please set the current time first.")
                continue
            if format_choice is None:
                print("Please choose the time format first.")
                continue

            print("⏸️ Press 'p' to pause the clock, and ▶️ 'r' to resume it.")
            print("\n📖 To exit, press 'm' to return to the menu.")
            print_alarm_time(alarm_hour, alarm_minute, alarm_second, format_choice)

            clock_running = True
            clock_paused = False
            alarm_triggered = False

            def update_clock():
                nonlocal hours, minutes, seconds, clock_running, clock_paused, alarm_triggered
                try:
                    while clock_running:
                        if not clock_paused:
                            formatted_time = format_time(hours, minutes, seconds, format_choice)
                            print_time(formatted_time)

                            if alarm_setting(hours, minutes, seconds, alarm_hour, alarm_minute, alarm_second) and not alarm_triggered:
                                ALARM = format_time(alarm_hour, alarm_minute, alarm_second, format_choice)
                                print(f"\n🚨 It's {ALARM}. DdrRrRiIiiNnnnG")
                                alarm_triggered = True

                            hours, minutes, seconds = afficher_heure(hours, minutes, seconds)

                        time.sleep(1)  # Delay 1 second between updates
                except KeyboardInterrupt:
                    print("\nClock interrupted!")

            clock_thread = threading.Thread(target=update_clock)
            clock_thread.daemon = True
            clock_thread.start()

            while True:
                keypress = check_keypress()
                if keypress == 'm':
                    clock_running = False
                    break
                elif keypress == 'p':
                    clock_paused = True
                    print("Clock paused. Press 'r' to resume.")
                elif keypress == 'r':
                    clock_paused = False
                    print("Clock resumed.")
                else:
                    # Ignore any other keypresses
                    pass
                time.sleep(0.1)  # Small delay to avoid high CPU usage

        elif choice == '5':
            print("Exiting the clock...")
            break
        else:
            print("Invalid option! Please choose from the menu.")

if __name__ == "__main__":
    main()