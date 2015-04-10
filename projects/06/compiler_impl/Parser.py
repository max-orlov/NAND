from enum import Enum


class CommandType(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3


class Parser:
    """
    this class handles the parsing of a given file.
    """

    def __init__(self, filename):
        """
        initializes the needed parameters.
        """
        self._file = open(filename)
        self._file_lines = self._file.readlines()
        self._file_lines_iter = enumerate(self._file_lines)
        self._current_command = ''
        self._current_line = ''

    def has_more_commands(self):
        """
        checks if there are more valid commands in the file (comments and empty lines are not valid).

        :return: True if there are more commands, False otherwise.
        """
        try:
            index, line = next(self._file_lines_iter)
            while line.strip().startswith("//") or len(line.strip()) == 0:
                index, line = next(self._file_lines_iter)

            self._current_line = line
            # print(index, line)
            return True
        except StopIteration:
            self._file.close()
            return False

    def advance(self):
        """
        sets the current command to the current valid line (without comments).

        :return: None.
        """
        self._current_command = self._current_line[:self._current_line.find("//")].strip()

    def command_type(self):
        """
        returns the type of the current command from the CommandType enum.

        :return: the command type.
        """
        if "=" in self._current_command or ";" in self._current_command:
            return CommandType.C_COMMAND
        elif self.is_label():
            return CommandType.L_COMMAND
        elif self._current_command.startswith("@"):
            # TODO: check if negative numbers allowed - if so find another method
            return CommandType.A_COMMAND if self._current_command[1:].isdecimal() else CommandType.L_COMMAND

    def is_label(self):
        """
        checks if the current command is a label, aka of type '(...)'.
        :return: True if the command is a label
        """
        if "(" in self._current_command and ")" in self._current_command:
            _left_par_index = self._current_command.index("(")
            _right_par_index = self._current_command.index(")", _left_par_index)
            return 0 <= _left_par_index < _right_par_index
        return False

    def symbol(self):
        """
        returns symbol or decimal number from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: the symbol or decimal number.
        """
        if self._current_command.startswith("@"):
            return self._current_command[1:]
        return self._current_command[1: self._current_command.find(")")]

    def dest(self):
        """
        returns 'dest' part (mnemonic) from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: 'dest' part.
        """
        if "=" in self._current_command:
            return self._current_command[: self._current_command.find("=")].strip()
        else:
            return "null"

    def comp(self):
        """
        returns 'comp' part (mnemonic) from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: 'comp' part.
        """
        if ";" in self._current_command:
            end = self._current_line.find(";")
        else:
            end = len(self._current_command)
        if "=" in self._current_command:
            return self._current_command[self._current_command.find("=") + 1: end].strip()
        return self._current_command[: self._current_command.find(";")].strip()

    def jump(self):
        """
        returns 'jump' part (mnemonic) from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: 'jump' part.
        """
        return self._current_command[self._current_command.find(";") + 1:].strip() if ";" in self._current_command else \
            "null"
