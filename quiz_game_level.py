import tkinter as tk
import random


# ============================================================
#                         QUESTIONS
# ============================================================

questions = {

    "Simple": [
        {
            "question": "What is 2 + 3?",
            "options": ["4", "5", "6", "7"],
            "answer": "5"
        },
        {
            "question": "What color is the sun usually drawn as?",
            "options": ["Blue", "Green", "Yellow", "Purple"],
            "answer": "Yellow"
        },
        {
            "question": "How many legs does a dog have?",
            "options": ["2", "4", "6", "8"],
            "answer": "4"
        },
        {
            "question": "Which animal says 'Moo'?",
            "options": ["Dog", "Cat", "Cow", "Horse"],
            "answer": "Cow"
        },
        {
            "question": "How many days are in a week?",
            "options": ["5", "6", "7", "8"],
            "answer": "7"
        },
        {
            "question": "What is 10 - 4?",
            "options": ["5", "6", "7", "8"],
            "answer": "6"
        },
        {
            "question": "Which planet do we live on?",
            "options": ["Mars", "Earth", "Venus", "Jupiter"],
            "answer": "Earth"
        },
        {
            "question": "What is the opposite of hot?",
            "options": ["Warm", "Cold", "Dry", "Bright"],
            "answer": "Cold"
        },
        {
            "question": "How many fingers are on one hand?",
            "options": ["4", "5", "6", "10"],
            "answer": "5"
        },
        {
            "question": "Which fruit is usually yellow?",
            "options": ["Banana", "Blueberry", "Strawberry", "Grape"],
            "answer": "Banana"
        }
    ],


    # ========================================================
    #                         MIDDLE
    # ========================================================

    "Middle": [
        {
            "question": "What is 12 × 4?",
            "options": ["36", "48", "52", "56"],
            "answer": "48"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "answer": "Mars"
        },
        {
            "question": "What is the capital of France?",
            "options": ["London", "Paris", "Rome", "Madrid"],
            "answer": "Paris"
        },
        {
            "question": "How many sides does a hexagon have?",
            "options": ["5", "6", "7", "8"],
            "answer": "6"
        },
        {
            "question": "What is 100 ÷ 4?",
            "options": ["20", "25", "30", "40"],
            "answer": "25"
        },
        {
            "question": "Which gas do humans need to breathe?",
            "options": ["Carbon dioxide", "Oxygen", "Helium", "Hydrogen"],
            "answer": "Oxygen"
        },
        {
            "question": "How many continents are there?",
            "options": ["5", "6", "7", "8"],
            "answer": "7"
        },
        {
            "question": "Which ocean is the largest?",
            "options": [
                "Atlantic Ocean",
                "Indian Ocean",
                "Pacific Ocean",
                "Arctic Ocean"
            ],
            "answer": "Pacific Ocean"
        },
        {
            "question": "What is 15 + 27?",
            "options": ["32", "40", "42", "45"],
            "answer": "42"
        },
        {
            "question": "Which organ pumps blood around the body?",
            "options": ["Brain", "Lung", "Heart", "Stomach"],
            "answer": "Heart"
        }
    ],


    # ========================================================
    #                         DIFFICULT
    # ========================================================

    "Difficult": [
        {
            "question": "What is 15 × 16?",
            "options": ["220", "230", "240", "250"],
            "answer": "240"
        },
        {
            "question": "What is the chemical symbol for gold?",
            "options": ["Ag", "Au", "Fe", "Go"],
            "answer": "Au"
        },
        {
            "question": "Which is the largest planet in our Solar System?",
            "options": ["Earth", "Saturn", "Jupiter", "Neptune"],
            "answer": "Jupiter"
        },
        {
            "question": "What is 144 ÷ 12?",
            "options": ["10", "11", "12", "14"],
            "answer": "12"
        },
        {
            "question": "Which country has the largest population?",
            "options": ["USA", "India", "Brazil", "Australia"],
            "answer": "India"
        },
        {
            "question": "What is the square root of 81?",
            "options": ["7", "8", "9", "10"],
            "answer": "9"
        },
        {
            "question": "Which part of a plant absorbs water from the soil?",
            "options": ["Leaves", "Flowers", "Roots", "Stem"],
            "answer": "Roots"
        },
        {
            "question": "How many degrees are in a triangle?",
            "options": ["90", "180", "270", "360"],
            "answer": "180"
        },
        {
            "question": "Which is the smallest prime number?",
            "options": ["0", "1", "2", "3"],
            "answer": "2"
        },
        {
            "question": "What is 25% of 200?",
            "options": ["25", "40", "50", "75"],
            "answer": "50"
        }
    ]
}


# ============================================================
#                         GAME VARIABLES
# ============================================================

score = 0
question_number = 0
quiz_questions = []
selected_level = ""


# ============================================================
#                         MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title("🌟 My Fun Quiz 🌟")

window.geometry("700x650")

window.config(
    bg="#ffeaa7"
)

window.resizable(
    False,
    False
)


# ============================================================
#                         TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="🌟 My Fun Quiz 🌟",
    font=("Arial", 32, "bold"),
    bg="#ffeaa7",
    fg="#6c5ce7"
)

title_label.pack(
    pady=(30, 10)
)


# ============================================================
#                         LEVEL SCREEN
# ============================================================

level_frame = tk.Frame(
    window,
    bg="#ffeaa7"
)

level_frame.pack(
    pady=20
)


level_title = tk.Label(
    level_frame,
    text="Choose Your Level",
    font=("Arial", 22, "bold"),
    bg="#ffeaa7",
    fg="#2d3436"
)

level_title.pack(
    pady=20
)


level_description = tk.Label(
    level_frame,
    text="How brave are you? 😊",
    font=("Arial", 15),
    bg="#ffeaa7",
    fg="#636e72"
)

level_description.pack(
    pady=(0, 20)
)


# ============================================================
#                         QUIZ FRAME
# ============================================================

quiz_frame = tk.Frame(
    window,
    bg="#ffeaa7"
)


# ============================================================
#                         SCORE
# ============================================================

score_label = tk.Label(
    quiz_frame,
    text="Score: 0",
    font=("Arial", 16, "bold"),
    bg="#ffeaa7",
    fg="#2d3436"
)

score_label.pack(
    anchor="ne",
    padx=30
)


# ============================================================
#                         LEVEL LABEL
# ============================================================

current_level_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 15, "bold"),
    bg="#ffeaa7",
    fg="#6c5ce7"
)

current_level_label.pack(
    pady=5
)


# ============================================================
#                         QUESTION NUMBER
# ============================================================

question_count_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 14),
    bg="#ffeaa7",
    fg="#636e72"
)

question_count_label.pack(
    pady=5
)


# ============================================================
#                         QUESTION
# ============================================================

question_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 21, "bold"),
    bg="#ffeaa7",
    fg="#2d3436",
    wraplength=600,
    justify="center"
)

question_label.pack(
    pady=30
)


# ============================================================
#                         FEEDBACK
# ============================================================

feedback_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 15, "bold"),
    bg="#ffeaa7",
    wraplength=600
)

feedback_label.pack(
    pady=15
)


# ============================================================
#                         ANSWER FUNCTION
# ============================================================

def answer_button_clicked(button):
    selected_answer = button.cget("text")

    check_answer(
        selected_answer
    )


# ============================================================
#                         ANSWER BUTTONS
# ============================================================

answer_buttons = []


for i in range(4):

    button = tk.Button(
        quiz_frame,
        text="",
        font=("Arial", 14, "bold"),
        width=30,
        height=2,
        bg="#74b9ff",
        fg="white",
        activebackground="#0984e3",
        activeforeground="white"
    )

    button.config(
        command=lambda b=button: answer_button_clicked(b)
    )

    answer_buttons.append(
        button
    )


# ============================================================
#                         GAME FUNCTIONS
# ============================================================

def choose_level(level):

    global selected_level
    global quiz_questions

    selected_level = level

    # Randomize the questions
    quiz_questions = random.sample(
        questions[level],
        len(questions[level])
    )

    # Hide level screen
    level_frame.pack_forget()

    # Show quiz screen
    quiz_frame.pack(
        fill="both",
        expand=True
    )

    current_level_label.config(
        text=f"Level: {selected_level}"
    )

    start_quiz()


def start_quiz():

    global score
    global question_number

    score = 0
    question_number = 0

    score_label.config(
        text="Score: 0"
    )

    feedback_label.config(
        text=""
    )

    # Show answer buttons
    for button in answer_buttons:

        button.pack(
            fill="x",
            padx=120,
            pady=5
        )

    show_question()


def show_question():

    global question_number

    feedback_label.config(
        text=""
    )

    if question_number >= len(quiz_questions):

        finish_game()

        return

    current_question = quiz_questions[question_number]

    question_count_label.config(
        text=f"Question {question_number + 1} "
             f"of {len(quiz_questions)}"
    )

    question_label.config(
        text=current_question["question"]
    )

    # Update buttons
    for i in range(4):

        answer_buttons[i].config(
            text=current_question["options"][i],
            state="normal",
            bg="#74b9ff"
        )


def check_answer(selected_answer):

    global score
    global question_number

    current_question = quiz_questions[question_number]

    # Disable buttons
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
            text="🎉 Correct! Fantastic!",
            fg="#00b894"
        )

    else:

        feedback_label.config(
            text=f"😊 Almost! The correct answer was "
                 f"{current_question['answer']}.",
            fg="#d63031"
        )

    question_number += 1

    # Wait before showing next question
    window.after(
        1200,
        show_question
    )


def finish_game():

    question_label.config(
        text="🎊 Quiz Complete! 🎊"
    )

    question_count_label.config(
        text=""
    )

    # Calculate percentage
    percentage = (
        score / len(quiz_questions)
    ) * 100

    if percentage == 100:

        message = (
            f"🏆 PERFECT SCORE! 🏆\n"
            f"You got {score} out of "
            f"{len(quiz_questions)}!"
        )

    elif percentage >= 70:

        message = (
            f"🌟 Excellent job! 🌟\n"
            f"You got {score} out of "
            f"{len(quiz_questions)}!"
        )

    elif percentage >= 50:

        message = (
            f"😊 Good job!\n"
            f"You got {score} out of "
            f"{len(quiz_questions)}!"
        )

    else:

        message = (
            f"💪 Keep practicing!\n"
            f"You got {score} out of "
            f"{len(quiz_questions)}!"
        )

    feedback_label.config(
        text=message,
        fg="#6c5ce7"
    )

    # Hide answer buttons
    for button in answer_buttons:

        button.pack_forget()

    # Show level buttons again
    show_level_buttons()


def show_level_buttons():

    # Hide quiz
    quiz_frame.pack_forget()

    # Show level selection
    level_frame.pack(
        pady=20
    )


# ============================================================
#                         LEVEL BUTTONS
# ============================================================

simple_button = tk.Button(
    level_frame,
    text="🟢 SIMPLE",
    font=("Arial", 16, "bold"),
    bg="#55efc4",
    fg="#2d3436",
    activebackground="#00b894",
    width=20,
    height=2,
    command=lambda: choose_level("Simple")
)

simple_button.pack(
    pady=8
)


middle_button = tk.Button(
    level_frame,
    text="🟡 MIDDLE",
    font=("Arial", 16, "bold"),
    bg="#ffeaa7",
    fg="#2d3436",
    activebackground="#fdcb6e",
    width=20,
    height=2,
    command=lambda: choose_level("Middle")
)

middle_button.pack(
    pady=8
)


difficult_button = tk.Button(
    level_frame,
    text="🔴 DIFFICULT",
    font=("Arial", 16, "bold"),
    bg="#ff7675",
    fg="white",
    activebackground="#d63031",
    width=20,
    height=2,
    command=lambda: choose_level("Difficult")
)

difficult_button.pack(
    pady=8
)


# ============================================================
#                         START APPLICATION
# ============================================================

window.mainloop()