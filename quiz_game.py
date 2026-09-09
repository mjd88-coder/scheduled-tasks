import tkinter as tk
import random


# ---------------------------- QUESTIONS ------------------------------- #

questions = [
    {
        "question": "What is the largest animal in the world?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Shark"],
        "answer": "Blue Whale"
    },
    {
        "question": "How many legs does a spider have?",
        "options": ["6", "8", "10", "12"],
        "answer": "8"
    },
    {
        "question": "What is 7 + 8?",
        "options": ["14", "15", "16", "17"],
        "answer": "15"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": "Mars"
    },
    {
        "question": "What is the capital city of France?",
        "options": ["London", "Paris", "Rome", "Berlin"],
        "answer": "Paris"
    },
    {
        "question": "Which animal is known as the King of the Jungle?",
        "options": ["Tiger", "Lion", "Elephant", "Bear"],
        "answer": "Lion"
    },
    {
        "question": "How many days are there in a week?",
        "options": ["5", "6", "7", "8"],
        "answer": "7"
    },
    {
        "question": "Which planet do we live on?",
        "options": ["Mars", "Earth", "Venus", "Saturn"],
        "answer": "Earth"
    },
    {
        "question": "What color do you get when you mix red and yellow?",
        "options": ["Green", "Purple", "Orange", "Blue"],
        "answer": "Orange"
    },
    {
        "question": "Which bird cannot fly?",
        "options": ["Eagle", "Penguin", "Sparrow", "Parrot"],
        "answer": "Penguin"
    }
]


# ---------------------------- VARIABLES ------------------------------- #

score = 0
question_number = 0
quiz_questions = []


# ---------------------------- START GAME ------------------------------- #

def start_game():
    global score
    global question_number
    global quiz_questions

    score = 0
    question_number = 0

    # Randomize questions
    quiz_questions = random.sample(
        questions,
        len(questions)
    )

    score_label.config(
        text="Score: 0"
    )

    feedback_label.config(
        text=""
    )

    start_button.pack_forget()
    play_again_button.pack_forget()

    # Show answer buttons
    for button in answer_buttons:
        button.pack(
            fill="x",
            padx=100,
            pady=5
        )

    show_question()


# ---------------------------- SHOW QUESTION ------------------------------- #

def show_question():

    global question_number

    feedback_label.config(
        text=""
    )

    # Check whether quiz is finished
    if question_number >= len(quiz_questions):
        finish_game()
        return

    current_question = quiz_questions[question_number]

    question_count_label.config(
        text=f"Question {question_number + 1} of {len(quiz_questions)}"
    )

    question_label.config(
        text=current_question["question"]
    )

    # Update answer buttons
    for i in range(4):

        answer_buttons[i].config(
            text=current_question["options"][i],
            state="normal",
            bg="#74b9ff"
        )


# ---------------------------- CHECK ANSWER ------------------------------- #

def check_answer(selected_answer):

    global score
    global question_number

    current_question = quiz_questions[question_number]

    # Disable all buttons after answer
    for button in answer_buttons:
        button.config(
            state="disabled"
        )

    if selected_answer == current_question["answer"]:

        score += 1

        score_label.config(
            text=f"Score: {score}"
        )

        feedback_label.config(
            text="🎉 Correct! Great job!",
            fg="#00b894"
        )

    else:

        feedback_label.config(
            text=f"😊 Not quite! The answer was: "
                 f"{current_question['answer']}",
            fg="#d63031"
        )

    question_number += 1

    # Wait 1.2 seconds before showing next question
    window.after(
        1200,
        show_question
    )


# ---------------------------- FINISH GAME ------------------------------- #

def finish_game():

    question_label.config(
        text="🎊 Quiz Complete! 🎊"
    )

    question_count_label.config(
        text=""
    )

    feedback_label.config(
        text=f"You scored {score} out of {len(quiz_questions)}!",
        fg="#6c5ce7"
    )

    # Hide answer buttons
    for button in answer_buttons:
        button.pack_forget()

    # Show play again
    play_again_button.pack(
        pady=20
    )


# ---------------------------- BUTTON CLICK ------------------------------- #

def answer_button_clicked(button):
    """
    Gets the text from the clicked button
    and sends it to check_answer().
    """

    selected_answer = button.cget("text")

    check_answer(
        selected_answer
    )


# ---------------------------- WINDOW ------------------------------- #

window = tk.Tk()

window.title(
    "🌟 My Fun Quiz Game 🌟"
)

window.geometry(
    "650x600"
)

window.config(
    bg="#ffeaa7"
)

window.resizable(
    False,
    False
)


# ---------------------------- TITLE ------------------------------- #

title_label = tk.Label(
    window,
    text="🌟 My Fun Quiz 🌟",
    font=("Arial", 32, "bold"),
    bg="#ffeaa7",
    fg="#6c5ce7"
)

title_label.pack(
    pady=(25, 10)
)


# ---------------------------- SCORE ------------------------------- #

score_label = tk.Label(
    window,
    text="Score: 0",
    font=("Arial", 16, "bold"),
    bg="#ffeaa7",
    fg="#2d3436"
)

score_label.pack(
    anchor="ne",
    padx=30
)


# ---------------------------- QUESTION NUMBER ------------------------------- #

question_count_label = tk.Label(
    window,
    text="",
    font=("Arial", 14),
    bg="#ffeaa7",
    fg="#636e72"
)

question_count_label.pack(
    pady=5
)


# ---------------------------- QUESTION ------------------------------- #

question_label = tk.Label(
    window,
    text="Welcome to the quiz!",
    font=("Arial", 20, "bold"),
    bg="#ffeaa7",
    fg="#2d3436",
    wraplength=550,
    justify="center"
)

question_label.pack(
    pady=30
)


# ---------------------------- ANSWER BUTTONS ------------------------------- #

answer_buttons = []


for i in range(4):

    button = tk.Button(
        window,
        text="",
        font=("Arial", 14, "bold"),
        width=25,
        height=2,
        bg="#74b9ff",
        fg="white",
        activebackground="#0984e3",
        activeforeground="white"
    )

    # IMPORTANT:
    # Use a default argument in lambda so each button
    # remembers which button it belongs to.
    button.config(
        command=lambda b=button: answer_button_clicked(b)
    )

    answer_buttons.append(
        button
    )


# ---------------------------- FEEDBACK ------------------------------- #

feedback_label = tk.Label(
    window,
    text="",
    font=("Arial", 15, "bold"),
    bg="#ffeaa7",
    wraplength=550
)

feedback_label.pack(
    pady=10
)


# ---------------------------- START BUTTON ------------------------------- #

start_button = tk.Button(
    window,
    text="🚀 Start Quiz",
    font=("Arial", 16, "bold"),
    bg="#00b894",
    fg="white",
    activebackground="#00a383",
    width=15,
    height=2,
    command=start_game
)

start_button.pack(
    pady=20
)


# ---------------------------- PLAY AGAIN BUTTON ------------------------------- #

play_again_button = tk.Button(
    window,
    text="🔄 Play Again",
    font=("Arial", 16, "bold"),
    bg="#6c5ce7",
    fg="white",
    activebackground="#5a4bcf",
    width=15,
    height=2,
    command=start_game
)


# ---------------------------- START APPLICATION ------------------------------- #

window.mainloop()
