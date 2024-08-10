from tkinter import *
from tkinter import Tk, Label, Canvas, Entry, Button
import tkinter.font as tkFont
import tkinter as tk

# Create the main window
root = Tk()
root.title("Welcome to Your Personal Task Manager")
root.configure(bg='light blue')

# Set the window size
root.geometry("600x500")  # Increased width for more horizontal space

# Create a custom font
custom_font = tkFont.Font(family="Helvetica", size=20, weight="bold")

# Create a label with the main message
label = Label(root, text="Welcome to Your Personal Task Manager", font=custom_font, bg='light blue', fg='purple')
label.pack(pady=20)

# Create a label with the secondary message
secondary_label = Label(root, text="Click anywhere to start", font=("Helvetica", 16), bg='light blue', fg='black')
secondary_label.pack(pady=10)

# Center the labels
label.place(relx=0.5, rely=0.4, anchor=CENTER)
secondary_label.place(relx=0.5, rely=0.6, anchor=CENTER)


# Function to create a new screen with a rectangle and 7 columns
def create_calendar(event):
    for widget in root.winfo_children():
        widget.destroy()

    global canvas
    canvas = Canvas(root, width=600, height=400, bg='white')
    canvas.pack(pady=20)

    # Draw a larger rectangle (weekly calendar)
    canvas.create_rectangle(20, 20, 580, 380, outline='black', width=4)  # Adjusted coordinates for a longer rectangle

    # Draw vertical lines to create 7 columns and add day labels
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for i in range(7):
        x = 20 + i * (560 // 7)  # Adjusted for the new width
        canvas.create_line(x, 20, x, 380, fill='black')
        canvas.create_text(x + (560 // 14), 10, text=days[i], font=("Helvetica", 12))

        # Bind click event to each column
        canvas.tag_bind(canvas.create_rectangle(x, 20, x + (560 // 7), 380, outline=''), '<Button-1>',
                         lambda e, day=days[i]: create_day_screen(day, canvas, x))

# Add squares under each column
    add_squares(canvas)


def add_squares(week_fg):
    for i in range(7):
        x = 20 + i * (560 // 7)
        week_fg.create_rectangle(x, 380, x + (560 // 7), 400, fill='white')


# Function to create a new screen for each day
def create_day_screen(day, canvas, x):
    for widget in root.winfo_children():
        widget.destroy()

    day_label = Label(root, text=f"Tasks for {day}", font=("Helvetica", 20, "bold"), bg='light blue', fg='purple')
    day_label.pack(pady=20)

    # Entry for wake up time and sleep time
    time_label = Label(root, text="Wake up time & Sleep time:", font=("Helvetica", 14), bg='light blue', fg='black')
    time_label.pack(pady=5)
    time_entry = Entry(root, font=("Helvetica", 14), width=35)
    time_entry.pack(pady=5)

    # Add placeholder text for time entry
    time_entry.insert(0, "Wake up time, AM/PM, Sleep time, AM/PM")
    time_entry.config(fg='grey')

    def on_click_time(event):
        if time_entry.get() == "Wake up time, AM/PM, Sleep time, AM/PM":
            time_entry.delete(0, "end")
            time_entry.config(fg='black')

    def on_focusout_time(event):
        if time_entry.get() == "":
            time_entry.insert(0, "Wake up time, AM/PM, Sleep time, AM/PM")
            time_entry.config(fg='grey')

    time_entry.bind("<FocusIn>", on_click_time)
    time_entry.bind("<FocusOut>", on_focusout_time)

    # Entry for number of hours
    hours_label = Label(root, text="Enter the number of hours in your day:", font=("Helvetica", 14), bg='light blue',
                        fg='black')
    hours_label.pack(pady=5)
    hours_entry = Entry(root, font=("Helvetica", 14), width=15)
    hours_entry.pack(pady=5)

    # Add placeholder text for hours entry
    hours_entry.insert(0, "Enter a number")
    hours_entry.config(fg='grey')

    def on_click_hours(event):
        if hours_entry.get() == "Enter a number":
            hours_entry.delete(0, "end")
            hours_entry.config(fg='black')

    def on_focusout_hours(event):
        if hours_entry.get() == "":
            hours_entry.insert(0, "Enter a number")
            hours_entry.config(fg='grey')

    hours_entry.bind("<FocusIn>", on_click_hours)
    hours_entry.bind("<FocusOut>", on_focusout_hours)

    # Restrict entry to numbers only
    def validate_hours(P):
        if P.isdigit() or P == "":
            return True
        return False

    hours_entry.config(validate="key", validatecommand=(root.register(validate_hours), '%P'))

    # Entry for tasks with placeholder text
    tasks_label = Label(root, text="Enter your tasks:", font=("Helvetica", 14), bg='light blue', fg='black')
    tasks_label.pack(pady=5)
    tasks_entry = Entry(root, font=("Helvetica", 14), width=50)
    tasks_entry.insert(0, "Enter task, then comma, then from what time to what time")
    tasks_entry.pack(pady=5)

    def on_click_tasks(event):
        if tasks_entry.get() == "Enter task, then comma, then from what time to what time":
            tasks_entry.delete(0, "end")
            tasks_entry.config(fg='pink')

    def on_focusout_tasks(event):
        if tasks_entry.get() == "":
            tasks_entry.insert(0, "Enter task, then comma, then from what time to what time")
            tasks_entry.config(fg='grey')

    tasks_entry.bind("<FocusIn>", on_click_tasks)
    tasks_entry.bind("<FocusOut>", on_focusout_tasks)
    tasks_entry.config(fg='grey')

    # List to store the entered times
    times = []

    # Function to save and display the entered times
    def save_times():
        wake_sleep_times = time_entry.get()
        canvas.create_text(x + (560 // 14), 390, text=wake_sleep_times, font=("Helvetica", 12), anchor=N)
        times.append(wake_sleep_times)

    save_button = Button(root, text="Save", command=save_times)
    save_button.pack(pady=10)

    back_button = Button(root, text="Back", command=lambda: create_calendar(None))
    back_button.pack(pady=10)

    # Extract wake up and sleep times from user input
    wake_up_time = time_entry.get().split('+')[0]
    sleep_time = time_entry.get().split('+')[1]

    # Add numbers to squares
    for i in range(7):
        x = 20 + i * (560 // 7)
        canvas.create_text(x + (560 // 14), 390, text=wake_up_time + '-' + sleep_time, font=("Helvetica", 12), anchor=N)


# Bind the click event to the function
root.bind("<u>", create_calendar)

# Create a Canvas widget and draw rectangles
canvas = tk.Canvas(root, width=100, height=100)
canvas.pack(pady=300)

# Draw multiple rectangles on the Canvas
canvas.create_rectangle(1, 1, 350, 350, fill="blue")

root.mainloop()
