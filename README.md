# Terminal-Based Clock with Alarm

This project is a terminal-based clock that allows users to set the current time, choose the time format (12h or 24h), and set an alarm. The clock updates in real-time and includes functionalities to pause, resume, and return to the main menu.

## Features
- **Set Current Time**: Enter the current hour, minute, and second.
- **Choose Time Format**: Select between 12-hour or 24-hour format.
- **Set Alarm**: Set the alarm time and get notified when the time matches the set alarm.
- **Clock Control**: Pause and resume the clock with the option to return to the main menu.
- **Non-blocking Keypress**: Key presses are checked without blocking the clock's operation.

## Functions
- **afficher_heure**: Updates the time (hours, minutes, seconds).
- **format_time**: Formats the time according to the chosen format (12h or 24h).
- **alarm_setting**: Checks if the current time matches the alarm time.
- **print_time**: Displays the current time in the terminal.
- **print_alarm_time**: Displays the alarm time in the terminal.
- **set_time**: Prompts the user to set the current time.
- **set_format**: Prompts the user to select the time format (12h/24h).
- **set_alarm**: Prompts the user to set the alarm time.
- **check_keypress**: Checks for non-blocking key presses (works on Windows with `msvcrt`).
- **main**: Main menu to interact with the clock, set time, format, and alarm, and control the clock.

## How It Works
1. **Set the time**: The user enters the current time in hours, minutes, and seconds.
2. **Choose the format**: The user selects either 12-hour or 24-hour format.
3. **Set the alarm**: The user sets the alarm time.
4. **Start the clock**: The clock starts, updating the time every second.
5. **Control the clock**: Pause and resume the clock, or return to the main menu.

## Requirements
- Python 3.x
- `msvcrt` module (works on Windows for non-blocking key press detection)

## How to Run
1. Clone the repository.
2. Run the script in a terminal-based Python environment.

```bash
git clone https://github.com/yourusername/terminal-based-clock.git
cd terminal-based-clock
python clock_script.py
