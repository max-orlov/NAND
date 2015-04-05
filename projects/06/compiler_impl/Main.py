from Parser import Parser, CommandType
import SymbolTable

class Main:
    def __init__(self):
        self._parser = None
        self._symbolTable = None

    def parseFile(self, filename):
        self._symbolTable = SymbolTable()
        for i in range(16):
            self._symbolTable.addEntry("R" + i, i)

        self._currentSymbolNum = 16

        #first run.
        self._parser = Parser(filename)
        while self._parser.hasMoreCommands():
            self._parser.advance()
            if self._parser.commandType() == CommandType.L_COMMAND:
                self._symbolTable.addEntry(self._parser.symbol(), self._currentSymbolNum)
                self._currentSymbolNum += 1

        #second run.
        self._parser = Parser(filename)
        while self._parser.hasMoreCommands():
            self._parser.advance()
            # TODO: finish impl.