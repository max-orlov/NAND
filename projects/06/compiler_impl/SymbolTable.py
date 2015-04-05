# this is the symbols table of the compiler.

class SymbolTable:
    # this is the ctor which initializes an empty table.
    def __init__(self):
        self._table = {}

    ###
    #  adds a new entry with 'symbol' key and 'address' value to the table.
    #  Note: it is assumed the symbol does not exist.
    ###
    def addEntry(self, symbol, address):
        self._table[symbol] = address

    ###
    #  checks if a given symbol is already in the table.
    ###
    def contains(self, symbol):
        return symbol in self._table.keys()

    ###
    #  returns the address of a given symbol.
    #  Note: it is assumed the symbol is at the table.
    ###
    def getAddress(self, symbol):
        return self._table[symbol]