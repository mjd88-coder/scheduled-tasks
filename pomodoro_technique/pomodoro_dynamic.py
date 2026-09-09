from tkinter import *
import math
import winsound
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Default values
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
timer = None


# ---------------------------- GET USER SETTINGS ------------------------------- #
def get_timer_values():
    """Get timer values entered by the user."""

    global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN

    try:
        work_value = int(work_entry.get())
        short_break_value = int(short_break_entry.get())
        long_break_value = int(long_break_entry.get())

        # Make sure values are positive
        if work_value <= 0 or short_break_value <= 0 or long_break_value <= 0:
            raise ValueError

        WORK_MIN = work_value
        SHORT_BREAK_MIN = short_break_value
        LONG_BREAK_MIN = long_break_value

        return True

    except ValueError:
        error_label.config(
            text="Please enter positive whole numbers.",
            fg=RED
        )
        return False


# ---------------------------- DISABLE / ENABLE SETTINGS ------------------------------- #
def disable_settings():
    work_entry.config(state="disabled")
    short_break_entry.config(state="disabled")
    long_break_entry.config(state="disabled")


def enable_settings():
    work_entry.config(state="normal")
    short_break_entry.config(state="normal")
    long_break_entry.config(state="normal")


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global timer, reps

    if timer:
        window.after_cancel(timer)
        timer = None

    canvas.itemconfig(timer_text, text="00:00")

    title_label.config(
        text="Timer",
        fg=GREEN
    )

    check_marks.config(text="")

    reps = 0

    enable_settings()

    error_label.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps

    # Get the latest values entered by the user
    if not get_timer_values():
        return

    # Disable settings while timer is running
    disable_settings()

    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        # Every 8th session = long break
        count_down(long_break_sec)

        title_label.config(
            text="Long Break",
            fg=RED
        )

    elif reps % 2 == 0:
        # Even sessions = short break
        count_down(short_break_sec)

        title_label.config(
            text="Short Break",
            fg=PINK
        )

    else:
        # Odd sessions = work
        count_down(work_sec)

        title_label.config(
            text="Work",
            fg=GREEN
        )


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(
        timer_text,
        text=f"{count_min}:{count_sec}"
    )

    if count > 0:
        global timer

        timer = window.after(
            1000,
            count_down,
            count - 1
        )

    else:
        # Beep when timer finishes
        winsound.Beep(1000, 1000)

        start_timer()

        marks = ""
        work_sessions = math.floor(reps / 2)

        for _ in range(work_sessions):
            marks += "✓"

        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()

window.title(
    "Pomodoro Technique - Helping you to work effectively"
)

window.config(
    padx=80,
    pady=40,
    bg=YELLOW
)


# ---------------------------- TIMER SETTINGS ------------------------------- #
settings_frame = Frame(
    window,
    bg=YELLOW
)

settings_frame.grid(
    column=0,
    row=0,
    columnspan=3,
    pady=(0, 15)
)


# Work duration
Label(
    settings_frame,
    text="Work (min):",
    bg=YELLOW,
    font=(FONT_NAME, 10)
).grid(
    column=0,
    row=0,
    padx=5,
    pady=5
)

work_entry = Entry(
    settings_frame,
    width=5,
    justify="center",
    font=(FONT_NAME, 12)
)

work_entry.grid(
    column=1,
    row=0,
    padx=5
)

work_entry.insert(
    0,
    str(WORK_MIN)
)


# Short break duration
Label(
    settings_frame,
    text="Short Break (min):",
    bg=YELLOW,
    font=(FONT_NAME, 10)
).grid(
    column=2,
    row=0,
    padx=5
)

short_break_entry = Entry(
    settings_frame,
    width=5,
    justify="center",
    font=(FONT_NAME, 12)
)

short_break_entry.grid(
    column=3,
    row=0,
    padx=5
)

short_break_entry.insert(
    0,
    str(SHORT_BREAK_MIN)
)


# Long break duration
Label(
    settings_frame,
    text="Long Break (min):",
    bg=YELLOW,
    font=(FONT_NAME, 10)
).grid(
    column=4,
    row=0,
    padx=5
)

long_break_entry = Entry(
    settings_frame,
    width=5,
    justify="center",
    font=(FONT_NAME, 12)
)

long_break_entry.grid(
    column=5,
    row=0,
    padx=5
)

long_break_entry.insert(
    0,
    str(LONG_BREAK_MIN)
)


# ---------------------------- ERROR MESSAGE ------------------------------- #
error_label = Label(
    window,
    text="",
    bg=YELLOW,
    font=(FONT_NAME, 9)
)

error_label.grid(
    column=1,
    row=1,
    columnspan=2
)


# ---------------------------- TITLE ------------------------------- #
# Title is now directly ABOVE the tomato image
title_label = Label(
    window,
    text="Timer",
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 40)
)

title_label.grid(
    column=1,
    row=2,
    columnspan=1,
    pady=(5, 0)
)


# ---------------------------- TOMATO IMAGE ------------------------------- #
canvas = Canvas(
    window,
    width=200,
    height=224,
    bg=YELLOW,
    highlightthickness=0
)

tomato_img = PhotoImage(
    file=resource_path("tomato.png")
)

canvas.create_image(
    100,
    112,
    image=tomato_img
)

timer_text = canvas.create_text(
    100,
    130,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)

canvas.grid(
    column=1,
    row=3
)


# ---------------------------- BUTTONS ------------------------------- #
start_button = Button(
    window,
    text="Start",
    command=start_timer,
    width=8
)

start_button.grid(
    column=0,
    row=4,
    pady=15
)


reset_button = Button(
    window,
    text="Reset",
    command=reset_timer,
    width=8
)

reset_button.grid(
    column=2,
    row=4,
    pady=15
)


# ---------------------------- CHECK MARKS ------------------------------- #
check_marks = Label(
    window,
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 15)
)

check_marks.grid(
    column=1,
    row=5
)


window.mainloop()