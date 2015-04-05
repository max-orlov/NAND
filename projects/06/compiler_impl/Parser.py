from enum import Enum

class CommandType(Enum):
    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

# this class handles the parsing of a given file.
class Parser:
    def __init__(self, filename):
        self._fileLines = enumerate(open(filename).readlines())

        self._currentCommand = ''
        self._currentLine = ''
        self._hasCommands = False

    def hasMoreCommands(self):
        index, line = self._fileLines.next()
        while line.strip().startswith("#"):
            index, line = str(self._fileLines.next()).strip()
        self._currentLine = line
        return index < len(self._fileLines)

    def advance(self):
        self._currentCommand = self._currentLine[:self._currentLine.find("#")].strip()

    def commandType(self):
        if "=" in self._currentCommand or ";" in self.currentLine:
            return CommandType.C_COMMAND
        elif "(" in self.currentLine and ")" in self.currentLine:
            return CommandType.L_COMMAND
        else:
            return CommandType.A_COMMAND

    def symbol(self):
        if self._currentCommand.startswith("@"):
            return self._currentCommand[1:]
        return self._currentCommand[1: self._currentCommand.find(")")]

    def dest(self):
        return self._currentCommand[: self._currentLine.find("=")].strip()

    def comp(self):
        if "=" in self._currentCommand:
            return self._currentCommand[self._currentLine.find("=") + 1: self._currentLine.find(";")].strip()
        return self._currentCommand[: self._currentLine.find(";")].strip()

    def jump(self):
        return self._currentCommand[self._currentLine.find(";") + 1:].strip()