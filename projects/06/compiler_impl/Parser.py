from enum import Enum

class CommandType(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

# this class handles the parsing of a given file.
class Parser:
    # initializes the needed parameters.
    def __init__(self, filename):
        self._file = open(filename)
        self._fileLines = self._file.readlines()
        self._fileLinesIter = enumerate(self._fileLines)
        self._currentCommand = ''
        self._currentLine = ''

    # checks if there are more valid commands in the file (comments and empty lines are not valid).
    def hasMoreCommands(self):
        index, line = self._fileLinesIter.next()
        while line.strip().startswith("//") or len(line.strip()) == 0:
            index, line = str(self._fileLinesIter.next()).strip()
            if index == len(self._fileLines):   # reached the end..
                self._file.close()
                return False

        self._currentLine = line
        return True

    # sets the current command to the current valid line (without comments).
    def advance(self):
        self._currentCommand = self._currentLine[:self._currentLine.find("//")].strip()

    # returns the type of the current command from the CommandType enum.
    def commandType(self):
        if "=" in self._currentCommand or ";" in self.currentLine:
            return CommandType.C_COMMAND
        elif "(" in self.currentLine and ")" in self.currentLine:
            return CommandType.L_COMMAND
        else:
            return CommandType.A_COMMAND

    ###
    #  returns symbol or decimal number from command.
    #  Note: assumed that the command is L_COMMAND or A_COMMAND.
    ###
    def symbol(self):
        if self._currentCommand.startswith("@"):
            return self._currentCommand[1:]
        return self._currentCommand[1: self._currentCommand.find(")")]

    ###
    #  returns 'dest' part (mnemonic) from command.
    #  Note: assumed that the command is L_COMMAND or A_COMMAND.
    ###
    def dest(self):
        return self._currentCommand[: self._currentLine.find("=")].strip()

    ###
    #  returns 'comp' part (mnemonic) from command.
    #  Note: assumed that the command is L_COMMAND or A_COMMAND.
    ###
    def comp(self):
        if "=" in self._currentCommand:
            return self._currentCommand[self._currentLine.find("=") + 1: self._currentLine.find(";")].strip()
        return self._currentCommand[: self._currentLine.find(";")].strip()

    ###
    #  returns 'jump' part (mnemonic) from command.
    #  Note: assumed that the command is L_COMMAND or A_COMMAND.
    ###
    def jump(self):
        return self._currentCommand[self._currentLine.find(";") + 1:].strip()