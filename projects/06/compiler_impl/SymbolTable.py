class SymbolTable:
    """
    this is the symbols table of the compiler.
    """

    def __init__(self):
        """
        this is the ctor which initializes an empty table.
        """
        self._table = {}

        # predefined symbols:
        # adds R0 - R15.
        for i in range(16):
            self.add_entry("R" + str(i), i)
        # SP, LCL, ARG, THIS, THAT, SCREEN, KBD
        self.add_entry("SP", 0)
        self.add_entry("LCL", 1)
        self.add_entry("ARG", 2)
        self.add_entry("THIS", 3)
        self.add_entry("THAT", 4)
        self.add_entry("SCREEN", 16384)
        self.add_entry("KBD", 24576)

    def add_entry(self, symbol, address):
        """
        adds a new entry with 'symbol' key and 'address' value to the table.
        Note: it is assumed the symbol does not exist.

        :param symbol: the key.
        :param address: the value.
        :return: None.
        """
        self._table[symbol] = address

    def contains(self, symbol):
        """
        checks if a given symbol is already in the table.

        :param symbol: the key.
        :return: True if the symbol is already in the table, False otherwise
        """
        return symbol in self._table.keys()

    def get_address(self, symbol):
        """
        returns the address of a given symbol.
        Note: it is assumed the symbol is at the table.

        :param symbol: the key.
        :return: the address of the symbol.
        """
        return self._table[symbol]