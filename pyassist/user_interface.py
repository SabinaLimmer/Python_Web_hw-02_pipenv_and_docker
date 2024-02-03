from abc import ABC, abstractmethod

class UserInterface(ABC):
    @abstractmethod
    def print_message(self, message):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass

    @abstractmethod
    def display_menu(self, menu_options):
        pass
