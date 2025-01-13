import tkinter as tk
from tkinter import messagebox
from time import strftime
import pygame
import os
from PIL import Image, ImageTk

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("L'horloge de Mamie")

        # Set geometry to be responsive to screen size
        self.root.geometry("800x600")
        self.root.minsize(400, 300)  # Minimum size for responsiveness

        # Get screen dimensions to scale elements proportionally
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Define background image path and alarm sound path
        self.bg_image_path = r"C:\Users\microstar\Downloads\background.png"
        self.alarm_sound_path = r"C:\Users\microstar\Downloads\alarm_sound.mp3.wav"

        # Load background image
        self.load_background(screen_width, screen_height)

        # Time label with dynamic resizing
        self.time_label = tk.Label(root, font=('Helvetica', int(screen_width // 15)), fg='blue', bg='#ffffff', relief='ridge')
        self.time_label.pack(pady=20, fill=tk.X, expand=True)

        # Control frame centered below the clock
        self.control_frame = tk.Frame(root, bg='#ffffff')
        self.control_frame.pack(pady=50)  # Adds space between the clock and buttons

        # Buttons for controlling the clock, positioned in a single row
        self.set_time_btn = tk.Button(self.control_frame, text="Set Time", command=self.set_time)
        self.set_time_btn.grid(row=0, column=0, padx=20, pady=10, sticky='ew')

        self.set_alarm_btn = tk.Button(self.control_frame, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_btn.grid(row=0, column=1, padx=20, pady=10, sticky='ew')

        self.toggle_mode_btn = tk.Button(self.control_frame, text="Switch to 12H Mode", command=self.toggle_mode)
        self.toggle_mode_btn.grid(row=0, column=2, padx=20, pady=10, sticky='ew')

        self.pause_btn = tk.Button(self.control_frame, text="Pause", command=self.toggle_pause)
        self.pause_btn.grid(row=0, column=3, padx=20, pady=10, sticky='ew')

        # Default settings
        self.running = True
        self.alarm_time = None
        self.is_24h_mode = True

        # Initialize Pygame for sound
        self.initialize_pygame()

        # Alarm stop button (initially hidden)
        self.stop_alarm_btn = tk.Button(self.root, text="Stop Alarm", command=self.stop_alarm, font=('Helvetica', 20), bg='red', fg='white')
        self.stop_alarm_btn.pack(pady=20)
        self.stop_alarm_btn.place(x=screen_width // 2 - 100, y=screen_height - 100)  # Position at the bottom center
        self.stop_alarm_btn.pack_forget()  # Hide the button initially

        # Update time every second
        self.update_time()

    def load_background(self, screen_width, screen_height):
        """Load and set the background image."""
        if os.path.exists(self.bg_image_path):
            # Open the image using Pillow
            img = Image.open(self.bg_image_path)
            
            # Resize the image to fit the screen while maintaining its resolution
            img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            
            # Convert the image to a format tkinter can use
            self.bg_image = ImageTk.PhotoImage(img)
            
            # Set the background image as the label
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        else:
            messagebox.showerror("Error", "Background image not found. Please check the file path.")

    def initialize_pygame(self):
        """Initialize pygame and load the alarm sound."""
        try:
            pygame.mixer.init()
            if os.path.exists(self.alarm_sound_path):
                self.alarm_sound = self.alarm_sound_path
            else:
                raise FileNotFoundError
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize sound: {e}")
            self.alarm_sound = None

    def update_time(self):
        """Update time every second and check for alarm."""
        if self.running:
            current_time = strftime('%H:%M:%S') if self.is_24h_mode else strftime('%I:%M:%S %p')
            self.time_label.config(text=current_time)

            if self.alarm_time and current_time.startswith(self.alarm_time):
                if self.alarm_sound:
                    pygame.mixer.music.load(self.alarm_sound)
                    pygame.mixer.music.play(-1)  # Loop the alarm sound
                messagebox.showinfo("Alarm!", "C'est l'heure de l'alarme!")
                self.show_stop_alarm_button()  # Show the stop alarm button when alarm rings
                self.alarm_time = None  # Reset alarm after triggering

        self.root.after(1000, self.update_time)

    def show_stop_alarm_button(self):
        """Show the stop alarm button."""
        self.stop_alarm_btn.pack()  # Display the stop alarm button

    def hide_stop_alarm_button(self):
        """Hide the stop alarm button."""
        self.stop_alarm_btn.pack_forget()

    def stop_alarm(self):
        """Stop the alarm sound if it's playing."""
        pygame.mixer.music.stop()
        self.hide_stop_alarm_button()  # Hide the stop alarm button after stopping the alarm
        messagebox.showinfo("Alarm Stopped", "The alarm has been stopped.")

    def set_time(self):
        """Set the current time."""
        time_input = self.simple_input("Set Time", "Enter time (HH:MM:SS):")
        if time_input:
            try:
                hours, minutes, seconds = map(int, time_input.split(':'))
                self.alarm_time = None
                messagebox.showinfo("Time Set", f"Time set to {hours:02}:{minutes:02}:{seconds:02}")
            except ValueError:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM:SS.")

    def set_alarm(self):
        """Set the alarm time."""
        alarm_input = self.simple_input("Set Alarm", "Enter alarm time (HH:MM:SS):")
        if alarm_input:
            self.alarm_time = alarm_input
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_input}")

    def toggle_mode(self):
        """Toggle between 12-hour and 24-hour modes."""
        self.is_24h_mode = not self.is_24h_mode
        self.toggle_mode_btn.config(text="Switch to 24H Mode" if not self.is_24h_mode else "Switch to 12H Mode")

    def toggle_pause(self):
        """Pause or resume the time updates."""
        self.running = not self.running
        self.pause_btn.config(text="Resume" if not self.running else "Pause")

    def simple_input(self, title, prompt):
        """Show a dialog to get user input."""
        input_win = tk.Toplevel(self.root)
        input_win.title(title)
        tk.Label(input_win, text=prompt).pack(pady=5)

        user_input = tk.Entry(input_win)
        user_input.pack(pady=5)

        def submit():
            input_win.user_input = user_input.get()
            input_win.destroy()

        tk.Button(input_win, text="Submit", command=submit).pack(pady=5)

        input_win.user_input = None
        self.root.wait_window(input_win)
        return input_win.user_input

if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()