from user_interface import UserInterface

class ConsoleUI(UserInterface):
    def print_message(self, message):
        print(message)

    def get_user_input(self, prompt):
        return input(prompt).strip()

    def display_menu(self, menu_options):
        max_option_length = max(len(item['option']) for item in menu_options)
        self.print_message("Options:".ljust(max_option_length + 5) + "Command:")
        self.print_message("-" * (max_option_length + 24))
        for _, item in enumerate(menu_options):
            self.print_message(f"{item['option'].ljust(max_option_length + 5)} {item['command']}")
        self.print_message("-" * (max_option_length + 24))