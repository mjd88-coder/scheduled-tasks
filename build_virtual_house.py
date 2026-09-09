import turtle

# -------------------------
# SET UP THE SCREEN
# -------------------------

screen = turtle.Screen()
screen.title("🏠 My Virtual House")
screen.bgcolor("skyblue")
screen.setup(width=900, height=650)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()


# -------------------------
# HELPER FUNCTIONS
# -------------------------

def rectangle(x, y, width, height, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()

    pen.fillcolor(color)
    pen.begin_fill()

    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)

    pen.end_fill()


def triangle(x, y, size, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()

    pen.fillcolor(color)
    pen.begin_fill()

    for _ in range(3):
        pen.forward(size)
        pen.left(120)

    pen.end_fill()


def circle(x, y, radius, color):
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()

    pen.fillcolor(color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()


# -------------------------
# GRASS
# -------------------------

rectangle(-450, -325, 900, 150, "lightgreen")


# -------------------------
# HOUSE
# -------------------------

# House walls
rectangle(-250, -175, 500, 300, "peachpuff")

# Roof
pen.penup()
pen.goto(-300, 125)
pen.pendown()

pen.fillcolor("firebrick")
pen.begin_fill()

pen.goto(0, 350)
pen.goto(300, 125)
pen.goto(-300, 125)

pen.end_fill()


# -------------------------
# DOOR
# -------------------------

rectangle(-60, -175, 120, 180, "saddlebrown")

# Door knob
circle(35, -85, 8, "gold")


# -------------------------
# WINDOWS
# -------------------------

# Left window
rectangle(-210, -20, 100, 100, "lightblue")

# Window cross
pen.color("white")
pen.width(5)

pen.penup()
pen.goto(-160, -20)
pen.pendown()
pen.goto(-160, 80)

pen.penup()
pen.goto(-210, 30)
pen.pendown()
pen.goto(-110, 30)


# Right window
rectangle(110, -20, 100, 100, "lightblue")

pen.penup()
pen.goto(160, -20)
pen.pendown()
pen.goto(160, 80)

pen.penup()
pen.goto(110, 30)
pen.pendown()
pen.goto(210, 30)


# -------------------------
# CHIMNEY
# -------------------------

rectangle(150, 190, 60, 120, "darkred")


# -------------------------
# SUN
# -------------------------

circle(330, 260, 50, "yellow")


# -------------------------
# TREE
# -------------------------

# Tree trunk
rectangle(-380, -175, 50, 150, "saddlebrown")

# Tree leaves
circle(-355, 0, 70, "forestgreen")
circle(-410, 20, 55, "green")
circle(-300, 20, 55, "green")


# -------------------------
# FLOWERS
# -------------------------

circle(-180, -250, 10, "red")
circle(-130, -270, 10, "purple")
circle(180, -250, 10, "pink")
circle(230, -270, 10, "orange")


# -------------------------
# TITLE
# -------------------------

pen.penup()
pen.goto(-180, 270)
pen.color("black")
pen.write(
    "🏠 My Virtual House",
    font=("Arial", 28, "bold")
)


# -------------------------
# FINISH
# -------------------------

screen.mainloop()
