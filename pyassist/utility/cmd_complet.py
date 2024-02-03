import difflib
from prompt_toolkit.completion import Completer, Completion  # pip install prompt_toolkit


def similar_command(user_cmd: str, commands: list) -> str:
    """
    Check if a word is similar to any command in the list.

    Args:
        user_cmd (str): user command to check
        commands (list): list of valid commands

    Returns:
        str: hint to user with similar word or words and return empty string if nothing found
    """
    matches = difflib.get_close_matches(user_cmd, commands)
    if matches:
        return f"\nmaybe you meant: {' or '.join(matches)}"
    return ""


class CommandCompleter(Completer):
    def __init__(self, commands: list):
        self.commands = commands

    def get_completions(self, text, complete_event):
        word_before_cursor = text.get_word_before_cursor()
        matches = [cmd for cmd in self.commands if cmd.startswith(word_before_cursor)]
        if not matches:                                                                         # If no exact match was found
            close_matches = difflib.get_close_matches(word_before_cursor, self.commands) # Find the closest match
            if close_matches:                                                                   # If the closest match was found
                match = close_matches[0]
                yield Completion(match, start_position=-len(word_before_cursor))
            # else:
            #     yield Completion(f"Unknown command: {word_before_cursor}")                      # If there is no exact and closest match
        else:
            for match in matches:                                                               # If the exact match was found
                yield Completion(match, start_position=-len(word_before_cursor))