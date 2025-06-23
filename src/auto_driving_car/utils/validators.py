
VALID_COMMANDS = {'F', 'L', 'R'}
class Validators:

    def validate_commands(command_string: str):
        invalid_chars = {char for char in command_string if char not in VALID_COMMANDS}
        if invalid_chars:
            raise ValueError(f"Invalid command(s) detected: {', '.join(invalid_chars)}")
