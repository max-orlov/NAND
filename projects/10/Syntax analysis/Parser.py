import re

BASIC_INDENT = "  "

###### Lexical Elements: ######

def parseBase(tList, startIndex, indent):
    return BASIC_INDENT * indent + tList[startIndex] + "\n", startIndex + 1

def parseKeyword(tList, startIndex, indent):
    return parseBase(tList, startIndex, indent)

def parseSymbol(tList, startIndex, indent):
    return parseBase(tList, startIndex, indent)

def parseInteger(tList, startIndex, indent):
    return parseBase(tList, startIndex, indent)

def parseString(tList, startIndex, indent):
    return parseBase(tList, startIndex, indent)

def parseIdentifier(tList, startIndex, indent):
    return parseBase(tList, startIndex, indent)

###### Program Structure: ######

def parseClass(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    idOut, index = parseIdentifier(tList, index, indent + 1)
    symOpenOut, index = parseSymbol(tList, index, indent + 1)
    varOutA = []
    while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ["static", "field"]:
        out, index = parseClassVarDec(tList, index, indent + 1)
        varOutA.append(out)
    subOutA = []
    while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ["constructor", "function", "method"]:
        out, index = parseSubroutineDec(tList, index, indent + 1)
        varOutA.append(out)
    symCloseOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<class>\n" + \
           keyOut + idOut + symOpenOut + ''.join(varOutA) + ''.join(subOutA) + symCloseOut +\
           BASIC_INDENT * indent + "</class>\n", index

def parseClassVarDec(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    typeOut, index = parseType(tList, index, indent + 1)
    varOut, index = parseVarName(tList, index, indent + 1)
    varOutA = []
    while "," in tList[index]:
        symOut, index = parseSymbol(tList, index, indent + 1)
        out, index = parseVarName(tList, index, indent + 1)
        varOutA.extend([symOut, out])
    symOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<classVarDec>\n" + \
           keyOut + typeOut + varOut + ''.join(varOutA) + symOut +\
           BASIC_INDENT * indent + "</classVarDec>\n", index

def parseType(tList, startIndex, indent):
    if re.search("<.+> (.+) <.+>", tList[startIndex]).group(1) in ["int", "char", "boolean"]:
        return parseKeyword(tList, startIndex, indent)
    else:
        return parseClassName(tList, startIndex, indent)

def parseSubroutineDec(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    if "void" in tList[index]:
        typeOut, index = parseKeyword(tList, index, indent + 1)
    else:
        typeOut, index = parseType(tList, index, indent + 1)
    nameOut, index = parseSubroutineName(tList, index, indent + 1)
    symOpenOut, index = parseSymbol(tList, index, indent + 1)
    paramOut, index = parseParameterList(tList, index, indent + 1)
    symCloseOut, index = parseSymbol(tList, index, indent + 1)
    subOut, index = parseSubroutineBody(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<subroutineDec>\n" + \
           keyOut + typeOut + nameOut + symOpenOut + paramOut + symCloseOut + subOut +\
           BASIC_INDENT * indent + "</subroutineDec>\n", index

def parseParameterList(tList, startIndex, indent):
    if ")" in tList[startIndex]:
        return BASIC_INDENT * indent + "<parameterList>\n" + \
               BASIC_INDENT * indent + "</parameterList>\n", startIndex

    typeOut, index = parseType(tList, startIndex, indent + 1)
    varOut, index = parseVarName(tList, index, indent + 1)
    typeOutA = []
    while "," in tList[index]:
        symOut, index = parseSymbol(tList, index, indent + 1)
        tOut, index = parseType(tList, index, indent + 1)
        vOut, index = parseVarName(tList, index, indent + 1)
        typeOutA.extend([symOut, tOut, vOut])
    return BASIC_INDENT * indent + "<parameterList>\n" + \
           typeOut + varOut + ''.join(typeOutA) +\
           BASIC_INDENT * indent + "</parameterList>\n", index

def parseSubroutineBody(tList, startIndex, indent):
    symOpenOut, index = parseSymbol(tList, startIndex, indent + 1)
    varOutA = []
    while "var" in tList[index]:
        out, index = parseVarDec(tList, index, indent + 1)
        varOutA.append(out)
    statOut, index = parseStatements(tList, index, indent + 1)
    symCloseOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<subroutineBody>\n" + \
           symOpenOut + ''.join(varOutA) + statOut + symCloseOut +\
           BASIC_INDENT * indent + "</subroutineBody>\n", index

def parseVarDec(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    typeOut, index = parseType(tList, index, indent + 1)
    varOut, index = parseVarName(tList, index, indent + 1)
    varOutA = []
    while "," in tList[index]:
        symOut, index = parseSymbol(tList, index, indent + 1)
        out, index = parseVarName(tList, index, indent + 1)
        varOutA.extend([symOut, out])
    symOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<varDec>\n" + \
           keyOut + typeOut + varOut + ''.join(varOutA) + symOut +\
           BASIC_INDENT * indent + "</varDec>\n", index

def parseClassName(tList, startIndex, indent):
    return parseIdentifier(tList, startIndex, indent)

def parseSubroutineName(tList, startIndex, indent):
    return parseIdentifier(tList, startIndex, indent)

def parseVarName(tList, startIndex, indent):
    return parseIdentifier(tList, startIndex, indent)

###### Statements: ######

def parseStatements(tList, startIndex, indent):
    index = startIndex
    statOutA = []
    while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ["let", "if", "while", "do", "return"]:
        out, index = parseStatement(tList, index, indent + 1)
        statOutA.append(out)
    return BASIC_INDENT * indent + "<statements>\n" + \
           ''.join(statOutA) +\
           BASIC_INDENT * indent + "</statements>\n", index

def parseStatement(tList, startIndex, indent):
    if "let" in tList[startIndex]:
        return parseLetStatement(tList, startIndex, indent)
    elif "if" in tList[startIndex]:
        return parseIfStatement(tList, startIndex, indent)
    elif "while" in tList[startIndex]:
        return parseWhileStatement(tList, startIndex, indent)
    elif "do" in tList[startIndex]:
        return parseDoStatement(tList, startIndex, indent)
    elif "return" in tList[startIndex]:
        return parseReturnStatement(tList, startIndex, indent)

def parseLetStatement(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    varOut, index = parseVarName(tList, index, indent + 1)
    exOut = ''
    if "[" in tList[index]:
        symOpenOut, index = parseSymbol(tList, index, indent + 1)
        out, index = parseExpression(tList, index, indent + 1)
        symCloseOut, index = parseSymbol(tList, index, indent + 1)
        exOut = symOpenOut + out + symCloseOut
    eqSymOut, index = parseSymbol(tList, index, indent + 1)
    ex2Out, index = parseExpression(tList, index, indent + 1)
    endSymOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<letStatement>\n" + \
           keyOut + varOut + exOut + eqSymOut + ex2Out + endSymOut +\
           BASIC_INDENT * indent + "</letStatement>\n", index

def parseIfStatement(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    symOpenIfOut, index = parseSymbol(tList, index, indent + 1)
    exOut, index = parseExpression(tList, index, indent + 1)
    symCloseIfOut, index = parseSymbol(tList, index, indent + 1)
    symOpenStatOut, index = parseSymbol(tList, index, indent + 1)
    statOut, index = parseStatements(tList, index, indent + 1)
    symCloseStatOut, index = parseSymbol(tList, index, indent + 1)
    elseOut = ""
    if "else" in tList[index]:
        elseKeyOut, index = parseKeyword(tList, index, indent + 1)
        openStatOut, index = parseSymbol(tList, index, indent + 1)
        out, index = parseStatements(tList, index, indent + 1)
        closeStatOut, index = parseSymbol(tList, index, indent + 1)
        elseOut = elseKeyOut + openStatOut + out + closeStatOut

    return BASIC_INDENT * indent + "<ifStatement>\n" + \
           keyOut + symOpenIfOut + exOut + symCloseIfOut + symOpenStatOut + statOut + symCloseStatOut + elseOut +\
           BASIC_INDENT * indent + "</ifStatement>\n", index

def parseWhileStatement(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    symOpenIfOut, index = parseSymbol(tList, index, indent + 1)
    exOut, index = parseExpression(tList, index, indent + 1)
    symCloseIfOut, index = parseSymbol(tList, index, indent + 1)
    symOpenStatOut, index = parseSymbol(tList, index, indent + 1)
    statOut, index = parseStatements(tList, index, indent + 1)
    symCloseStatOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<whileStatement>\n" + \
           keyOut + symOpenIfOut + exOut + symCloseIfOut + symOpenStatOut + statOut + symCloseStatOut +\
           BASIC_INDENT * indent + "</whileStatement>\n", index

def parseDoStatement(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    subOut, index = parseSubroutineCall(tList, index, indent + 1)
    symOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<doStatement>\n" + \
           keyOut + subOut + symOut +\
           BASIC_INDENT * indent + "</doStatement>\n", index

def parseReturnStatement(tList, startIndex, indent):
    keyOut, index = parseKeyword(tList, startIndex, indent + 1)
    exOut = ""
    if ";" not in tList[index]:
        exOut, index = parseExpression(tList, index, indent + 1)
    symOut, index = parseSymbol(tList, index, indent + 1)
    return BASIC_INDENT * indent + "<returnStatement>\n" + \
           keyOut + exOut + symOut +\
           BASIC_INDENT * indent + "</returnStatement>\n", index

###### Expressions: ######

def parseExpression(tList, startIndex, indent):
    termOut, index = parseTerm(tList, startIndex, indent + 1)
    termOutA = []
    while re.search("<.+> (.+) <.+>", tList[index]).group(1) in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']:
        symOut, index = parseSymbol(tList, index, indent + 1)
        out,index = parseTerm(tList, index, indent + 1)
        termOutA.extend([symOut, out])
    return BASIC_INDENT * indent + "<expression>\n" + \
           termOut + ''.join(termOutA) +\
           BASIC_INDENT * indent + "</expression>\n", index

def parseTerm(tList, startIndex, indent):
    termOut = ""
    if "(" in tList[startIndex]:
        symOpenOut, index = parseSymbol(tList, startIndex, indent + 1)
        out, index = parseExpression(tList, index, indent + 1)
        symCloseOut, index = parseSymbol(tList, index, indent + 1)
        termOut = symOpenOut + out + symCloseOut
    elif re.search("<.+> (.+) <.+>", tList[startIndex]).group(1) in ['~', '-']:
        symOut, index = parseSymbol(tList, startIndex, indent + 1)
        out, index = parseTerm(tList, index, indent + 1)
        termOut = symOut + out
    elif "[" in tList[startIndex + 1]:
        varOut, index = parseVarName(tList, startIndex, indent + 1)
        symOpenOut, index = parseSymbol(tList, index, indent + 1)
        out, index = parseExpression(tList, index, indent + 1)
        symCloseOut, index = parseSymbol(tList, index, indent + 1)
        termOut = varOut + symOpenOut + out + symCloseOut
    elif "(" in tList[startIndex + 1] or "." in tList[startIndex + 1]:
        termOut, index = parseSubroutineCall(tList, startIndex, indent + 1)
    else:
        termOut, index = parseBase(tList, startIndex, indent + 1)

    return BASIC_INDENT * indent + "<term>\n" + \
           termOut +\
           BASIC_INDENT * indent + "</term>\n", index

def parseSubroutineCall(tList, startIndex, indent):
    index = startIndex
    classNameOut = ""
    if "." in tList[startIndex + 1]:
        nameOut, index = parseClassName(tList, index, indent)
        symOut, index = parseSymbol(tList, index, indent)
        classNameOut = nameOut + symOut
    subOut, index = parseSubroutineName(tList, index, indent)
    symOpenOut, index = parseSymbol(tList, index, indent)
    exListOut, index = parseExpressionList(tList, index, indent)
    symCloseOut, index = parseSymbol(tList, index, indent)
    return classNameOut + subOut + symOpenOut + exListOut + symCloseOut, index


def parseExpressionList(tList, startIndex, indent):
    if ")" in tList[startIndex]:
        return BASIC_INDENT * indent + "<expressionList>\n" + \
               BASIC_INDENT * indent + "</expressionList>\n", startIndex

    exOut, index = parseExpression(tList, startIndex, indent + 1)
    exOutA = []
    while "," in tList[index]:
        symOut, index = parseSymbol(tList, index, indent + 1)
        out, index = parseExpression(tList, index, indent + 1)
        exOutA.extend([symOut, out])
    return BASIC_INDENT * indent + "<expressionList>\n" + \
           exOut + ''.join(exOutA) +\
           BASIC_INDENT * indent + "</expressionList>\n", index


def parseTokens(tokens):
    str, index = parseClass(tokens.split("\n")[1:-1], 0, 0)
    return str