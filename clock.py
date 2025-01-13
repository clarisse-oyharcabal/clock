#import the librairies

import time
import threading


#etabish the functions
def afficher_heure(hours, minutes, seconds):  # Update the time
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


def format_time(hours, minutes, seconds, format_choice):  # Choose the format 
    struct_time = time.struct_time((2025, 1, 6, hours, minutes, seconds, 0, 0, -1))
    if format_choice == '12h':
        return time.strftime("%I:%M:%S %p", struct_time) 
    elif format_choice == '24h':
        return time.strftime("%H:%M:%S", struct_time)  
    else:
        raise ValueError("Invalid format choice! Please choose '12h' or '24h'.")


def alarm_setting(current_h, current_m, current_s, alarm_h, alarm_m, alarm_s):  # Check if the alarm time matches the current time
    return (current_h == alarm_h and current_m == alarm_m and current_s == alarm_s)
    

def print_time(formatted_time):  # Print the formatted time
    print(f"The current time is: {formatted_time}", end="\r")
    

def print_alarm_time(alarm_h, alarm_m, alarm_s, format_choice):  # Print the time of the alarm
    formatted_alarm = format_time(alarm_h, alarm_m, alarm_s, format_choice)
    print(f"Alarm is set for: {formatted_alarm}")



#Enter the values
def set_time():
    while True:
        try:
            hours = int(input("Enter current hour (0 - 23): "))
            if not (0 <= hours < 24):
                print("Hour value out of range. Please try again.")
                continue  # Re-ask for hours if out of range

            while True:
                try:
                    minutes = int(input("Enter current minute (0 - 59): "))
                    if not (0 <= minutes < 60):
                        print("Minute value out of range. Please try again.")
                        continue  # Re-ask for minutes if out of range
                    while True:
                        try:
                            seconds = int(input("Enter current second (0 - 59): "))
                            if not (0 <= seconds < 60):
                                print("Second value out of range. Please try again.")
                                continue  # Re-ask for seconds if out of range
                            return hours, minutes, seconds
                        except ValueError:
                            print("Invalid input for seconds. Please enter a numeric value between 0 and 59.")
                            continue  # Re-ask for seconds if input is invalid
                except ValueError:
                    print("Invalid input for minutes. Please enter a numeric value between 0 and 59.")
                    continue  # Re-ask for minutes if input is invalid
        except ValueError:
            print("Invalid input for hours. Please enter a numeric value between 0 and 23.")
            continue  # Re-ask for hours if input is invalid



#Choose the appropriate format 
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


#Set an alarm
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
                continue  # Re-ask for alarm hour if out of range

            while True:
                try:
                    alarm_minute = int(input("Choose the alarm minute (0 - 59): "))
                    if not (0 <= alarm_minute < 60):
                        print("Alarm minute value out of range. Please try again.")
                        continue  # Re-ask for alarm minute if out of range
                    while True:
                        try:
                            alarm_second = int(input("Choose the alarm second (0 - 59): "))
                            if not (0 <= alarm_second < 60):
                                print("Alarm second value out of range. Please try again.")
                                continue  # Re-ask for alarm second if out of range
                            return alarm_hour, alarm_minute, alarm_second
                        except ValueError:
                            print("Invalid input for alarm seconds. Please enter a numeric value between 0 and 59.")
                            continue  # Re-ask for alarm seconds if input is invalid
                except ValueError:
                    print("Invalid input for alarm minutes. Please enter a numeric value between 0 and 59.")
                    continue  # Re-ask for alarm minutes if input is invalid
        except ValueError:
            print("Invalid input for alarm hours. Please enter a numeric value between 0 and 23.")
            continue  # Re-ask for alarm hours if input is invalid


#Call all the different functions (mainloop)
def main():
    print("⏲️  Welcome to your Clock !")
    print("\n🚨 Before starting the clock and set an alarm, please set the time and choose the format.\n")

    hours, minutes, seconds = None, None, None
    format_choice = None
    alarm_hour, alarm_minute, alarm_second = None, None, None

    while True:
        print("\n📖 Main Menu")
        print("1. Set the current time")
        print("2. Choose the time format")
        print("3. Set an alarm (optional)")
        print("4. Start the clock")
        print("5. Exit")

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

            print("\nTo exit, press Ctrl + C or press 'm' to return to the menu.")     
            print_alarm_time(alarm_hour, alarm_minute, alarm_second, format_choice)  # Display alarm time when clock starts
                   
        

            def update_clock():
                nonlocal hours, minutes, seconds
                try:
                    while True:
                        formatted_time = format_time(hours, minutes, seconds, format_choice)
                        print_time(formatted_time)

                        if alarm_setting(hours, minutes, seconds, alarm_hour, alarm_minute, alarm_second):
                            ALARM = format_time(alarm_hour, alarm_minute, alarm_second, format_choice)
                            print(f"\nIt's {ALARM}. It's wake-up time!")

                        time.sleep(1)  # Introduce a 1-second delay between updates.
                        hours, minutes, seconds = afficher_heure(hours, minutes, seconds) 
                except KeyboardInterrupt:
                    print("\nClock interrupted!")

            clock_thread = threading.Thread(target=update_clock)
            clock_thread.daemon = True
            clock_thread.start()

            while True:
                user_input = input()
                if user_input.lower() == 'm':  # If the user presses 'm', return to the menu.
                    break
                else:
                    print("Invalid input. Please enter 'm' to return to the menu.")
                    
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()