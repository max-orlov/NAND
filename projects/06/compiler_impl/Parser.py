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
        self._fileLines = self._file.readlines()
        self._fileLinesIter = enumerate(self._fileLines)
        self._currentCommand = ''

    def hasMoreCommands(self):
        """
        checks if there are more valid commands in the file (comments and empty lines are not valid).

        :return: True if there are more commands, False otherwise.
        """
        try:
            index, line = next(self._fileLinesIter)
            while line.strip().startswith("//") or len(line.strip()) == 0:
                index, line = next(self._fileLinesIter)

            self._currentLine = line
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
        self._currentCommand = self._currentLine[:self._currentLine.find("//")].strip()

    def commandType(self):
        """
        returns the type of the current command from the CommandType enum.

        :return: the command type.
        """
        if "=" in self._currentCommand or ";" in self._currentCommand:
            return CommandType.C_COMMAND
        elif self.isLabel():
            return CommandType.L_COMMAND
        elif self._currentCommand.startswith("@"):
            if self._currentCommand[1:].isdecimal():    # TODO: check if negative numbers allowed - if so find another method
                return CommandType.A_COMMAND
            else:
                return CommandType.L_COMMAND

    def isLabel(self):
        """
        checks if the current command is a label, aka of type '(...)'.
        :return: True if the command is a label
        """
        return self._currentCommand.strip().startswith("(") and self._currentCommand.strip().endswith(")")

    def symbol(self):
        """
        returns symbol or decimal number from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: the symbol or decimal number.
        """
        if self._currentCommand.startswith("@"):
            return self._currentCommand[1:]
        return self._currentCommand[1: self._currentCommand.find(")")]

    def dest(self):
        """
        returns 'dest' part (mnemonic) from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: 'dest' part.
        """
        if "=" in self._currentCommand:
            return self._currentCommand[: self._currentCommand.find("=")].strip()
        else:
            return "null"

    def comp(self):
        """
        returns 'comp' part (mnemonic) from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: 'comp' part.
        """
        if ";" in self._currentCommand:
            end = self._currentLine.find(";")
        else:
            end = len(self._currentCommand)
        if "=" in self._currentCommand:
            return self._currentCommand[self._currentCommand.find("=") + 1: end].strip()
        return self._currentCommand[: self._currentCommand.find(";")].strip()

    def jump(self):
        """
        returns 'jump' part (mnemonic) from command.
        Note: assumed that the command is L_COMMAND or A_COMMAND.

        :return: 'jump' part.
        """
        if ";" in self._currentCommand:
            return self._currentCommand[self._currentCommand.find(";") + 1:].strip()
        else:
            return "null"