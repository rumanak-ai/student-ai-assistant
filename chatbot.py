import json
import os
import random
import re
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


class RuleBasedChatbot:
    """Enhanced Rule-Based Chatbot"""

    def __init__(self, name="Smart AI Assistant"):
        self.name = name
        self.user_name = ""
        self.history_file = "history.txt"

        # Statistics
        self.total_messages = 0
        self.greetings = 0
        self.ai_questions = 0
        self.math_questions = 0
        self.jokes = 0
        self.unknown = 0

        self.motivational_quotes = [
            "Dream big. Start small. Act now.",
            "Discipline beats motivation.",
            "Success is built one day at a time.",
            "Believe in yourself and never give up.",
            "Trust Allah and keep working hard.",
        ]

        self.study_tips = [
            "Study for 50 minutes and take a 10-minute break.",
            "Practice coding every day.",
            "Revision is the key to success.",
            "Understand concepts instead of memorizing.",
            "Solve one new problem daily.",
        ]

        self.programming_facts = self.load_facts()

        self.joke_list = [
            "Why do programmers hate nature? Because it has too many bugs!",
            "Why do Java developers wear glasses? Because they don't C#.",
            "Why did the AI cross the road? To optimize the other side!",
        ]

        self.rules = self.build_rules()

    def load_facts(self):
        """Loads facts from JSON file with a default fallback."""
        try:
            with open("ai_facts.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get(
                    "facts", ["Artificial Intelligence was founded as an academic discipline in 1956."]
                )
        except (FileNotFoundError, json.JSONDecodeError):
            return [
                "Python was named after Monty Python, not the snake!",
                "The first AI program was written in 1951.",
                "Algorithm comes from the name of 9th-century mathematician Al-Khwarizmi.",
            ]

    def build_rules(self):
        """Builds regex patterns mapping to response actions."""
        return {
            r"(hi|hello|hey|good morning|good evening|good afternoon).*": "GREETING",
            r"(bye|goodbye|exit|quit|see you).*": "GOODBYE",
            r"(what is your name|who are you|your name).*": "NAME",
            r"(help|commands).*": "HELP",
            r"(what can you do|capabilities).*": "CAPABILITIES",
            r"(calculate|compute|solve|what is)\s*([\d+\-*/().^ ]+)": "CALCULATE",
            r"(tell me about|what is|explain)\s+(ai|artificial intelligence).*": "AI",
            r"(machine learning).*": "ML",
            r"(deep learning).*": "DL",
            r"(python).*": "PYTHON",
            r"(motivate me|motivation).*": "MOTIVATE",
            r"(study tips|study tip).*": "STUDY",
            r"(fact|tell me a fact).*": "FACT",
            r"(joke|funny).*": "JOKE",
            r"(time).*": "TIME",
            r"(date).*": "DATE",
            r"(history).*": "HISTORY",
            r"(stats|statistics).*": "STATS",
        }

    def welcome_screen(self):
        print(Fore.CYAN + "=" * 60)
        print(Fore.GREEN + "        SMART AI ASSISTANT")
        print(Fore.CYAN + "=" * 60)

        self.user_name = input("Enter your name : ").strip()

        if not self.user_name:
            self.user_name = "User"

        print(Fore.YELLOW + f"\nWelcome {self.user_name}! 😊")
        print("Type HELP anytime to see available commands.")
        print("=" * 60)

    def save_history(self, user, bot):
        with open(self.history_file, "a", encoding="utf-8") as file:
            file.write(f"\nYou : {user}\n")
            file.write(f"Bot : {bot}\n")
            file.write("-" * 40 + "\n")

    def calculate(self, expression):
        try:
            allowed = set("0123456789+-*/().^ ")
            if not all(ch in allowed for ch in expression):
                return "Only basic mathematical expressions are allowed."

            # Safely evaluate standard math expressions
            result = eval(expression.replace("^", "**"))
            return f"Answer = {result}"
        except Exception:
            return "Invalid mathematical expression."

    def help_menu(self):
        return """
================== HELP MENU ==================
• Hi / Hello
• Who are you
• What is AI
• Machine Learning
• Deep Learning
• Python
• Calculate 20+30
• Joke
• Motivate me
• Study Tips
• Tell me a Fact
• Time
• Date
• History
• Stats
• Bye
===============================================
"""

    def show_history(self):
        if not os.path.exists(self.history_file):
            return "No chat history found."

        with open(self.history_file, "r", encoding="utf-8") as file:
            return file.read()

    def show_stats(self):
        return f"""
================ CHAT STATISTICS ================
User Name        : {self.user_name}
Total Messages   : {self.total_messages}
Greetings        : {self.greetings}
AI Questions     : {self.ai_questions}
Math Questions   : {self.math_questions}
Jokes Asked      : {self.jokes}
Unknown Questions: {self.unknown}
=================================================
"""

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        self.total_messages += 1

        if not user_input:
            return "Please enter a message."

        for pattern, action in self.rules.items():
            match = re.match(pattern, user_input)
            if match:
                if action == "GREETING":
                    self.greetings += 1
                    return random.choice([
                        f"Hello {self.user_name}! 😊",
                        f"Hi {self.user_name}! How are you today?",
                        f"Welcome back {self.user_name}!",
                    ])

                elif action == "GOODBYE":
                    return f"""
================================================
Thank you {self.user_name} 😊
It was nice chatting with you.
Keep learning.
Good Luck ❤️
================================================
"""

                elif action == "NAME":
                    return f"My name is {self.name}. I am your Rule-Based AI Assistant."

                elif action == "HELP":
                    return self.help_menu()

                elif action == "CAPABILITIES":
                    return """
I can help you with:
• AI, Machine Learning, Deep Learning, Python
• Math Calculations
• Current Time & Date
• Motivation & Study Tips
• Jokes & Facts
• Chat History & Statistics
"""

                elif action == "AI":
                    self.ai_questions += 1
                    return (
                        "Artificial Intelligence (AI) enables machines to "
                        "learn, reason, and solve problems similar to humans."
                    )

                elif action == "ML":
                    self.ai_questions += 1
                    return (
                        "Machine Learning is a subset of AI where computers "
                        "learn patterns from data without explicit programming."
                    )

                elif action == "DL":
                    self.ai_questions += 1
                    return (
                        "Deep Learning uses neural networks with multiple "
                        "layers to solve complex problems."
                    )

                elif action == "PYTHON":
                    return (
                        "Python is a high-level programming language used in "
                        "AI, Machine Learning, Data Science, Automation, and Web Development."
                    )

                elif action == "CALCULATE":
                    self.math_questions += 1
                    expression = match.group(2)
                    return self.calculate(expression)

                elif action == "MOTIVATE":
                    return random.choice(self.motivational_quotes)

                elif action == "STUDY":
                    return random.choice(self.study_tips)

                elif action == "FACT":
                    return random.choice(self.programming_facts)

                elif action == "JOKE":
                    self.jokes += 1
                    return random.choice(self.joke_list)

                elif action == "TIME":
                    return datetime.now().strftime("Current Time : %I:%M:%S %p")

                elif action == "DATE":
                    return datetime.now().strftime("Today's Date : %d %B %Y")

                elif action == "HISTORY":
                    return self.show_history()

                elif action == "STATS":
                    return self.show_stats()

        self.unknown += 1
        return "Sorry, I don't understand that.\nType HELP to see available commands."


def main():
    bot = RuleBasedChatbot()
    bot.welcome_screen()

    while True:
        user = input(Fore.CYAN + f"\n{bot.user_name}: ").strip()

        response = bot.get_response(user)
        print(Fore.GREEN + f"\n{bot.name}: {response}")

        bot.save_history(user, response)

        if user.lower() in ["bye", "quit", "exit"]:
            break


if __name__ == "__main__":
    main()