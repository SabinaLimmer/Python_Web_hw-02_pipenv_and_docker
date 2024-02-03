import sys
from pathlib import Path
import pyfiglet
import cowsay
from prompt_toolkit import prompt
from utility.addressbook import AddresBook
from utility.record_interaction import *
from utility.cmd_complet import CommandCompleter, similar_command
from consoleUI import ConsoleUI


# user interface
ui = ConsoleUI()


# paths to files with data # Because it's a simple program. The path is hard coded ;)
program_dir = Path(__file__).parent
ADDRESSBOOK_DATA_PATH = program_dir.joinpath("data/addresbook.dat") 


#objects storing data while the program is running
ADDRESSBOOK = AddresBook().load_addresbook(ADDRESSBOOK_DATA_PATH)
    

# function to handle with errors
def error_handler(func):
    def wrapper(*args):
        while True:
            try:
                return func(*args)
            except FileNotFoundError as e: 
                return f"I can't find folder."
            except KeyboardInterrupt:
                cli_pyassist_exit()
    return wrapper


# a function that parses user input commands
def parse_command(user_input: str) -> (str, tuple):
    """
    Parse user input command

    Args:
        user_input (str): user input command
    
    Returns:
        str: command
        tuple: arguments
    """
    tokens = user_input.split()
    command = tokens[0].lower()
    arguments = tokens[1:]
    return command, tuple(arguments)


# taking a command from the user
def user_command_input(completer: CommandCompleter, menu_name=""):
    user_input = ui.get_user_input(f"{menu_name} >>> ")
    if user_input:
        return parse_command(user_input)
    return "", ""
    
# exit / close program
def cli_pyassist_exit(*args):  
    ADDRESSBOOK.save_addresbook(ADDRESSBOOK_DATA_PATH)
    cowsay.tux("Your data has been saved.\nGood bye!") 
    sys.exit()


# function to show menus addressbook
def show_menu(menu_options):
    ui.display_menu(menu_options)


# function to handle addressbook command
def addressbook_commands(*args):
    menu_options = [
        {"option": "Show All Records", "command": "show"},
        {"option": "Show Specific Record", "command": "show <name>"},
        {"option": "Add Record", "command": "add"},
        {"option": "Edit Record", "command": "edit"},
        {"option": "Delete Record", "command": "delete"},
        {"option": "Search in Addressbook", "command": "search <query>"},
        {"option": "Upcoming Birthdays", "command": "birthday <days>"}, # (selected number of days ahead) - informacja do instrukcji 
        {"option": "Export Address Book", "command": "export"},
        {"option": "Import Address Book", "command": "import"},
        {"option": "Main Menu", "command": "up"}, 
        {"option": "Program exit", "command": "exit"},
        {"option": "Show this Menu", "command": "help"},
    ]
    show_menu(menu_options)
    completer = CommandCompleter(list(ADDRESSBOOK_MENU_COMMANDS.keys()) + list(ADDRESSBOOK.keys()))
    while True:
        cmd, arguments = user_command_input(completer, "address book")
        ui.print_message(execute_commands(ADDRESSBOOK_MENU_COMMANDS, cmd, ADDRESSBOOK, arguments))


# dict for main menu handler
MAIN_COMMANDS = {
    "exit": cli_pyassist_exit,
    "addressbook": addressbook_commands,
}


@error_handler
def pyassit_main_menu(*args):
    menu_options = [
        {"option": "Open your address book", "command": "addressbook"},
        {"option": "Program exit", "command": "exit"},
        {"option": "Show this Menu", "command": "help"},
    ]
    show_menu(menu_options)
    completer = CommandCompleter(MAIN_COMMANDS.keys())
    while True:
        cmd, arguments = user_command_input(completer, "main menu")
        ui.print_message(execute_commands(MAIN_COMMANDS, cmd, None, arguments))

# dict for addressbook menu
ADDRESSBOOK_MENU_COMMANDS = {
    "exit": cli_pyassist_exit,
    "add": add_record, #lambda *args: add_record(ADDRESSBOOK, *args),
    "edit": edit_record, #lambda *args: edit_record(ADDRESSBOOK, *args),
    "show": show, #lambda *args: show(ADDRESSBOOK, *args),
    "delete": del_record, #lambda *args: del_record(ADDRESSBOOK, *args),
    "export": export_to_csv, #lambda *args: export_to_csv(ADDRESSBOOK, *args),
    "import": import_from_csv, #lambda *args: import_from_csv(ADDRESSBOOK, *args),
    "birthday": show_upcoming_birthday, #lambda *args: show_upcoming_birthday(ADDRESSBOOK, *args),
    "search": search, #lambda *args: search(ADDRESSBOOK, *args),
    "up": pyassit_main_menu,
    "help": addressbook_commands,
}
    
    
def execute_commands(menu_commands: dict, cmd: str, data_to_use, arguments: tuple):
    """Function to execute user commands

    Args:
        menu_commands (dict): dict for menu-specific commands
        cmd (str): user command
        data_to_use: dict (for addressbook) or list (for notes) or None (for rest) to use in calling functions
        arguments (tuple): arguments from user input

    Returns:
        func: function with data_ti_use and arguments
    """
    if cmd not in menu_commands:
        return f"Command {cmd} is not recognized" + similar_command(cmd, menu_commands.keys())
    cmd = menu_commands[cmd]
    return cmd(data_to_use, *arguments)


def main():
    print(pyfiglet.figlet_format("PyAssist", font = "slant"))
    pyassit_main_menu()
    

if __name__ == "__main__":
    main()