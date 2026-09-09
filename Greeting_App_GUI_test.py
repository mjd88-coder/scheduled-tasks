import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class GreetingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Greeting App")
        self.setMinimumSize(350, 200)

        # Name input
        self.name_label = QLabel("Enter your name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name")

        # City input
        self.city_label = QLabel("Enter your city:")
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Your city")

        # Button
        self.greet_button = QPushButton("Greet Me")
        self.greet_button.clicked.connect(self.greet_user)

        # Greeting label
        self.greeting_label = QLabel("")
        self.greeting_label.setWordWrap(True)

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)

        layout.addWidget(self.greet_button)
        layout.addWidget(self.greeting_label)

        self.setLayout(layout)

    def greet_user(self):
        name = self.name_input.text().strip()
        city = self.city_input.text().strip()

        if name and city:
            self.greeting_label.setText(
                f"Hello, {name}! Welcome to {city}!"
            )
        elif name:
            self.greeting_label.setText(
                f"Hello, {name}!"
            )
        elif city:
            self.greeting_label.setText(
                f"Hello! Greetings to everyone in {city}!"
            )
        else:
            self.greeting_label.setText(
                "Please enter your name and city."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GreetingApp()
    window.show()

    sys.exit(app.exec())