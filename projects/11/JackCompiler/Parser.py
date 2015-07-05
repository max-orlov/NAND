import re

BASIC_INDENT = "  "

class Parser():
    def __init__(self):
        pass

    ###### Lexical Elements: ######
    
    def _parseBase(self, tList, startIndex, indent):
        return BASIC_INDENT * indent + tList[startIndex] + "\n", startIndex + 1
    
    def _parseKeyword(self, tList, startIndex, indent):
        return self._parseBase(tList, startIndex, indent)
    
    def _parseSymbol(self, tList, startIndex, indent):
        return self._parseBase(tList, startIndex, indent)
    
    def _parseInteger(self, tList, startIndex, indent):
        return self._parseBase(tList, startIndex, indent)
    
    def _parseString(self, tList, startIndex, indent):
        return self._parseBase(tList, startIndex, indent)
    
    def _parseIdentifier(self, tList, startIndex, indent):
        return self._parseBase(tList, startIndex, indent)
    
    ###### Program Structure: ######
    
    def _parseClass(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        idOut, index = self._parseIdentifier(tList, index, indent + 1)
        symOpenOut, index = self._parseSymbol(tList, index, indent + 1)
        varOutA = []
        while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ["static", "field"]:
            out, index = self._parseClassVarDec(tList, index, indent + 1)
            varOutA.append(out)
        subOutA = []
        while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ["constructor", "function", "method"]:
            out, index = self._parseSubroutineDec(tList, index, indent + 1)
            varOutA.append(out)
        symCloseOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<class>\n" + \
               keyOut + idOut + symOpenOut + ''.join(varOutA) + ''.join(subOutA) + symCloseOut +\
               BASIC_INDENT * indent + "</class>\n", index
    
    def _parseClassVarDec(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        typeOut, index = self._parseType(tList, index, indent + 1)
        varOut, index = self._parseVarName(tList, index, indent + 1)
        varOutA = []
        while "," in tList[index]:
            symOut, index = self._parseSymbol(tList, index, indent + 1)
            out, index = self._parseVarName(tList, index, indent + 1)
            varOutA.extend([symOut, out])
        symOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<classVarDec>\n" + \
               keyOut + typeOut + varOut + ''.join(varOutA) + symOut +\
               BASIC_INDENT * indent + "</classVarDec>\n", index
    
    def _parseType(self, tList, startIndex, indent):
        if re.search("<.+> (.+) <.+>", tList[startIndex]).group(1) in ["int", "char", "boolean"]:
            return self._parseKeyword(tList, startIndex, indent)
        else:
            return self._parseClassName(tList, startIndex, indent)
    
    def _parseSubroutineDec(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        if "void" in tList[index]:
            typeOut, index = self._parseKeyword(tList, index, indent + 1)
        else:
            typeOut, index = self._parseType(tList, index, indent + 1)
        nameOut, index = self._parseSubroutineName(tList, index, indent + 1)
        symOpenOut, index = self._parseSymbol(tList, index, indent + 1)
        paramOut, index = self._parseParameterList(tList, index, indent + 1)
        symCloseOut, index = self._parseSymbol(tList, index, indent + 1)
        subOut, index = self._parseSubroutineBody(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<subroutineDec>\n" + \
               keyOut + typeOut + nameOut + symOpenOut + paramOut + symCloseOut + subOut +\
               BASIC_INDENT * indent + "</subroutineDec>\n", index
    
    def _parseParameterList(self, tList, startIndex, indent):
        if ")" in tList[startIndex]:
            return BASIC_INDENT * indent + "<parameterList>\n" + \
                   BASIC_INDENT * indent + "</parameterList>\n", startIndex

        self.nextArgumentId = 0
        typeOut, index = self._parseType(tList, startIndex, indent + 1)
        varOut, index = self._parseVarName(tList, index, indent + 1)
        typeOutA = []
        while "," in tList[index]:
            symOut, index = self._parseSymbol(tList, index, indent + 1)
            tOut, index = self._parseType(tList, index, indent + 1)
            vOut, index = self._parseVarName(tList, index, indent + 1)
            typeOutA.extend([symOut, tOut, vOut])
        return BASIC_INDENT * indent + "<parameterList>\n" + \
               typeOut + varOut + ''.join(typeOutA) +\
               BASIC_INDENT * indent + "</parameterList>\n", index
    
    def _parseSubroutineBody(self, tList, startIndex, indent):
        self.nextVarId = 0
        symOpenOut, index = self._parseSymbol(tList, startIndex, indent + 1)
        varOutA = []
        while "var" in tList[index]:
            out, index = self._parseVarDec(tList, index, indent + 1)
            varOutA.append(out)
        statOut, index = self._parseStatements(tList, index, indent + 1)
        symCloseOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<subroutineBody>\n" + \
               symOpenOut + ''.join(varOutA) + statOut + symCloseOut +\
               BASIC_INDENT * indent + "</subroutineBody>\n", index
    
    def _parseVarDec(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        typeOut, index = self._parseType(tList, index, indent + 1)
        varOut, index = self._parseVarName(tList, index, indent + 1)
        varOutA = []
        while "," in tList[index]:
            symOut, index = self._parseSymbol(tList, index, indent + 1)
            out, index = self._parseVarName(tList, index, indent + 1)
            varOutA.extend([symOut, out])
        symOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<varDec>\n" + \
               keyOut + typeOut + varOut + ''.join(varOutA) + symOut +\
               BASIC_INDENT * indent + "</varDec>\n", index
    
    def _parseClassName(self, tList, startIndex, indent):
        parts = re.search("(<.+> )(.+)( <.+>)", tList[startIndex])
        return BASIC_INDENT * indent + parts.group(1) + parts.group(2) + ',' + parts.group(3) + "\n", startIndex + 1
    
    def _parseSubroutineName(self, tList, startIndex, indent):
        return self._parseIdentifier(tList, startIndex, indent)
    
    def _parseVarName(self, tList, startIndex, indent):
        return self._parseIdentifier(tList, startIndex, indent)

    ###### Statements: ######
    
    def _parseStatements(self, tList, startIndex, indent):
        index = startIndex
        statOutA = []
        while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ["let", "if", "while", "do", "return"]:
            out, index = self._parseStatement(tList, index, indent + 1)
            statOutA.append(out)
        return BASIC_INDENT * indent + "<statements>\n" + \
               ''.join(statOutA) +\
               BASIC_INDENT * indent + "</statements>\n", index
    
    def _parseStatement(self, tList, startIndex, indent):
        if "let" in tList[startIndex]:
            return self._parseLetStatement(tList, startIndex, indent)
        elif "if" in tList[startIndex]:
            return self._parseIfStatement(tList, startIndex, indent)
        elif "while" in tList[startIndex]:
            return self._parseWhileStatement(tList, startIndex, indent)
        elif "do" in tList[startIndex]:
            return self._parseDoStatement(tList, startIndex, indent)
        elif "return" in tList[startIndex]:
            return self._parseReturnStatement(tList, startIndex, indent)
    
    def _parseLetStatement(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        varOut, index = self._parseVarName(tList, index, indent + 1)
        exOut = ''
        if "[" in tList[index]:
            symOpenOut, index = self._parseSymbol(tList, index, indent + 1)
            out, index = self._parseExpression(tList, index, indent + 1)
            symCloseOut, index = self._parseSymbol(tList, index, indent + 1)
            exOut = symOpenOut + out + symCloseOut
        eqSymOut, index = self._parseSymbol(tList, index, indent + 1)
        ex2Out, index = self._parseExpression(tList, index, indent + 1)
        endSymOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<letStatement>\n" + \
               keyOut + varOut + exOut + eqSymOut + ex2Out + endSymOut +\
               BASIC_INDENT * indent + "</letStatement>\n", index
    
    def _parseIfStatement(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        symOpenIfOut, index = self._parseSymbol(tList, index, indent + 1)
        exOut, index = self._parseExpression(tList, index, indent + 1)
        symCloseIfOut, index = self._parseSymbol(tList, index, indent + 1)
        symOpenStatOut, index = self._parseSymbol(tList, index, indent + 1)
        statOut, index = self._parseStatements(tList, index, indent + 1)
        symCloseStatOut, index = self._parseSymbol(tList, index, indent + 1)
        elseOut = ""
        if "else" in tList[index]:
            elseKeyOut, index = self._parseKeyword(tList, index, indent + 1)
            openStatOut, index = self._parseSymbol(tList, index, indent + 1)
            out, index = self._parseStatements(tList, index, indent + 1)
            closeStatOut, index = self._parseSymbol(tList, index, indent + 1)
            elseOut = elseKeyOut + openStatOut + out + closeStatOut
    
        return BASIC_INDENT * indent + "<ifStatement>\n" + \
               keyOut + symOpenIfOut + exOut + symCloseIfOut + symOpenStatOut + statOut + symCloseStatOut + elseOut +\
               BASIC_INDENT * indent + "</ifStatement>\n", index
    
    def _parseWhileStatement(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        symOpenIfOut, index = self._parseSymbol(tList, index, indent + 1)
        exOut, index = self._parseExpression(tList, index, indent + 1)
        symCloseIfOut, index = self._parseSymbol(tList, index, indent + 1)
        symOpenStatOut, index = self._parseSymbol(tList, index, indent + 1)
        statOut, index = self._parseStatements(tList, index, indent + 1)
        symCloseStatOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<whileStatement>\n" + \
               keyOut + symOpenIfOut + exOut + symCloseIfOut + symOpenStatOut + statOut + symCloseStatOut +\
               BASIC_INDENT * indent + "</whileStatement>\n", index
    
    def _parseDoStatement(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        subOut, index = self._parseSubroutineCall(tList, index, indent + 1)
        symOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<doStatement>\n" + \
               keyOut + subOut + symOut +\
               BASIC_INDENT * indent + "</doStatement>\n", index
    
    def _parseReturnStatement(self, tList, startIndex, indent):
        keyOut, index = self._parseKeyword(tList, startIndex, indent + 1)
        exOut = ""
        if ";" not in tList[index]:
            exOut, index = self._parseExpression(tList, index, indent + 1)
        symOut, index = self._parseSymbol(tList, index, indent + 1)
        return BASIC_INDENT * indent + "<returnStatement>\n" + \
               keyOut + exOut + symOut +\
               BASIC_INDENT * indent + "</returnStatement>\n", index
    
    ###### Expressions: ######
    
    def _parseExpression(self, tList, startIndex, indent):
        termOut, index = self._parseTerm(tList, startIndex, indent + 1)
        termOutA = []
        while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']:
            symOut, index = self._parseSymbol(tList, index, indent + 1)
            out,index = self._parseTerm(tList, index, indent + 1)
            termOutA.extend([symOut, out])
        return BASIC_INDENT * indent + "<expression>\n" + \
               termOut + ''.join(termOutA) +\
               BASIC_INDENT * indent + "</expression>\n", index
    
    def _parseTerm(self, tList, startIndex, indent):
        termOut = ""
        if "stringConstant" in tList[startIndex]:
            termOut, index = self._parseString(tList, startIndex, indent + 1)
        elif "(" in tList[startIndex]:
            symOpenOut, index = self._parseSymbol(tList, startIndex, indent + 1)
            out, index = self._parseExpression(tList, index, indent + 1)
            symCloseOut, index = self._parseSymbol(tList, index, indent + 1)
            termOut = symOpenOut + out + symCloseOut
        elif re.search("<.+> (.+) <.+>", tList[startIndex]).group(1) in ['~', '-']:
            symOut, index = self._parseSymbol(tList, startIndex, indent + 1)
            out, index = self._parseTerm(tList, index, indent + 1)
            termOut = symOut + out
        elif "[" in tList[startIndex + 1]:
            varOut, index = self._parseVarName(tList, startIndex, indent + 1)
            symOpenOut, index = self._parseSymbol(tList, index, indent + 1)
            out, index = self._parseExpression(tList, index, indent + 1)
            symCloseOut, index = self._parseSymbol(tList, index, indent + 1)
            termOut = varOut + symOpenOut + out + symCloseOut
        elif "(" in tList[startIndex + 1] or "." in tList[startIndex + 1]:
            termOut, index = self._parseSubroutineCall(tList, startIndex, indent + 1)
        else:
            termOut, index = self._parseBase(tList, startIndex, indent + 1)
    
        return BASIC_INDENT * indent + "<term>\n" + \
               termOut +\
               BASIC_INDENT * indent + "</term>\n", index
    
    def _parseSubroutineCall(self, tList, startIndex, indent):
        index = startIndex
        classNameOut = ""
        if "." in tList[startIndex + 1]:
            nameOut, index = self._parseClassName(tList, index, indent)
            symOut, index = self._parseSymbol(tList, index, indent)
            classNameOut = nameOut + symOut
        subOut, index = self._parseSubroutineName(tList, index, indent)
        symOpenOut, index = self._parseSymbol(tList, index, indent)
        exListOut, index = self._parseExpressionList(tList, index, indent)
        symCloseOut, index = self._parseSymbol(tList, index, indent)
        return classNameOut + subOut + symOpenOut + exListOut + symCloseOut, index
    
    
    def _parseExpressionList(self, tList, startIndex, indent):
        if ")" in tList[startIndex] and "<stringConstant>" not in tList[startIndex]:
            return BASIC_INDENT * indent + "<expressionList>\n" + \
                   BASIC_INDENT * indent + "</expressionList>\n", startIndex
    
        exOut, index = self._parseExpression(tList, startIndex, indent + 1)
        exOutA = []
        while "," in tList[index]:
            symOut, index = self._parseSymbol(tList, index, indent + 1)
            out, index = self._parseExpression(tList, index, indent + 1)
            exOutA.extend([symOut, out])
        return BASIC_INDENT * indent + "<expressionList>\n" + \
               exOut + ''.join(exOutA) +\
               BASIC_INDENT * indent + "</expressionList>\n", index
    
    
    def parseTokens(self, tokens):
        str, index = self._parseClass(tokens.split("\n")[1:-1], 0, 0)
        return str