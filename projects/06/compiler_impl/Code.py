class Code:
    """
    this class handles parsing HACK mnemonics into C-instructions binary codes.
    """

    def dest(self, mnemonic):
        """
        returns the string representation of the destination bits.
        """
        if mnemonic == "null":
            return "000"
        if mnemonic == "M":
            return "001"
        if mnemonic == "D":
            return "010"
        if mnemonic == "MD":
            return "011"
        if mnemonic == "A":
            return "100"
        if mnemonic == "AM":
            return "101"
        if mnemonic == "AD":
            return "110"
        if mnemonic == "AMD":
            return "111"

    def comp(self, mnemonic):
        """
        returns the string representation of the comp bits.
        """
        if mnemonic == "0":
            return "0101010"
        if mnemonic == "1":
            return "0111111"
        if mnemonic == "-1":
            return "0111010"
        if mnemonic == "D":
            return "0001100"
        if mnemonic == "A":
            return "0110000"
        if mnemonic == "M":
            return "1110000"
        if mnemonic == "!D":
            return "0001101"
        if mnemonic == "!A":
            return "0110001"
        if mnemonic == "!M":
            return "1110001"
        if mnemonic == "-D":
            return "0001111"
        if mnemonic == "-A":
            return "0110011"
        if mnemonic == "-M":
            return "1110011"
        if mnemonic == "D+1":
            return "0011111"
        if mnemonic == "A+1":
            return "0110111"
        if mnemonic == "M+1":
            return "1110111"
        if mnemonic == "D-1":
            return "0001110"
        if mnemonic == "A-1":
            return "0110010"
        if mnemonic == "M-1":
            return "1110010"
        if mnemonic == "D+A":
            return "0000010"
        if mnemonic == "D+M":
            return "1000010"
        if mnemonic == "D-A":
            return "0010011"
        if mnemonic == "D-M":
            return "1010011"
        if mnemonic == "A-D":
            return "0000111"
        if mnemonic == "M-D":
            return "1000111"
        if mnemonic == "D&A":
            return "0000000"
        if mnemonic == "D&M":
            return "1000000"
        if mnemonic == "D|A":
            return "0010101"
        if mnemonic == "D|M":
            return "1010101"

    def jump(self, mnemonic):
        """
        returns the string representation of the jump bits.
        """
        if mnemonic == "null":
            return "000"
        if mnemonic == "JGT":
            return "001"
        if mnemonic == "JEQ":
            return "010"
        if mnemonic == "JGE":
            return "011"
        if mnemonic == "JLT":
            return "100"
        if mnemonic == "JNE":
            return "101"
        if mnemonic == "JLE":
            return "110"
        if mnemonic == "JMP":
            return "111"