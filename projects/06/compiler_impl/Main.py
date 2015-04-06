import sys
from Parser import Parser, CommandType
from SymbolTable import SymbolTable
from Code import Code

class Main:
    def __init__(self):
        """

        """
        self._parser = None
        self._symbolTable = None
        self._code = Code()
        self._currentSymbolNum = 16
        self._currentCommandNum = 0

    def parseFile(self, filename):
        """
        parses a given ASM file into HACK language.
        :param filename: the ASM filename.
        :return:
        """
        self._symbolTable = SymbolTable()

        #first run.
        self._parser = Parser(filename)
        while self._parser.hasMoreCommands():
            self._parser.advance()
            if self._parser.commandType() == CommandType.L_COMMAND:
                if self._parser.isLabel():
                    self._symbolTable.addEntry(self._parser.symbol(), self._currentCommandNum)
                    self._currentCommandNum -= 1
            self._currentCommandNum += 1


        #second run.
        self._parser = Parser(filename)
        hackFileContent = ""
        while self._parser.hasMoreCommands():
            hackLine = ""
            self._parser.advance()
            if self._parser.commandType() == CommandType.A_COMMAND:
                hackLine = "{0:b}".format(int(self._parser.symbol()))
                while len(hackLine) < 16:
                    hackLine = "0" + hackLine
            elif self._parser.commandType() == CommandType.L_COMMAND:
                if self._parser.isLabel():
                    continue
                if not self._symbolTable.contains(self._parser.symbol()):
                    self._symbolTable.addEntry(self._parser.symbol(), self._currentSymbolNum)
                    self._currentSymbolNum += 1
                hackLine = "{0:b}".format(self._symbolTable.getAddress(self._parser.symbol()))
                while len(hackLine) < 16:
                    hackLine = "0" + hackLine
            else:   # CommandType.C_COMMAND
                comp = self._parser.comp()
                dest = self._parser.dest()
                jump = self._parser.jump()
                hackLine += "111"
                hackLine += self._code.comp(comp)
                hackLine += self._code.dest(dest)
                hackLine += self._code.jump(jump)

            hackFileContent += hackLine + "\n"
        # print(hackFileContent)
        outFilename = filename[: filename.find(".")] + ".hack"
        outFile = open(outFilename, "w")
        outFile.write(hackFileContent)
        outFile.close()


if __name__ == '__main__':
    main = Main()
    # TODO: go over all files.
    main.parseFile(sys.argv[1])