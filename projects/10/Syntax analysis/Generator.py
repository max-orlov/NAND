import xml.etree.ElementTree as ET

OPERATORS = {'+':     'add',
             '-':     'sub',
             '*':     'call Math.multiply 2',
             '/':     'call Math.divide 2',
             '=':     'eq',
             '&lt;':  'lt', '<': 'lt',
             '&gt;':  'gt', '>': 'gt',
             '&amp;': 'and', '&': 'and',
             '|':     'or'
             }

UNARY_OPERATORS = {'-': 'neg', '~': 'not'}

KEYWORDS = {'true': 'push constant 0\n' + 'not\n',
            "false": 'push constant 0\n'}

class Generator():
    def __init__(self):
        self.className = None
        self.nextWhileNum = 0
        self.nextIfNum = 0
        self.classFieldsNum = 0
        self.classStaticsNum = 0
        self.classFields = {}
        self.classStatics = {}
        self.currentLocalsTable = {}
        self.currentArgsTable = {}

    def _generate_class(self, root):
        out = ''
        self.className = root[1].text.strip()
        for var in root.findall('classVarDec'):
            self._update_var_dec_table(var)
        for subroutine in root.findall('subroutineDec'):
            out += self._generate_function(subroutine)
        return out

    def _update_var_dec_table(self, root):
        for identifier in root.findall('identifier'):
            if root[0].text.strip() == 'field':
                self.classFields[identifier.text.strip()] = self.classFieldsNum
                self.classFieldsNum += 1
            else: # static
                self.classStatics[identifier.text.strip()] = self.classStaticsNum
                self.classStaticsNum += 1

    def _generate_function(self, root):
        functionType = root[0].text.strip()
        functionName = root[2].text.strip()

        paramList = root.find('parameterList')
        # fill args table.
        argId = 0
        for param in paramList:
            if param.tag == 'identifier':# and not is_keyword(param.text.strip()):
                self.currentArgsTable[param.text.strip()] = argId
                argId += 1

        body = root.find('subroutineBody')
        # fill locals table.
        localId = 0
        for varDec in body.findall('varDec'):
            for param in varDec:
                if param.tag == 'identifier':# and not is_keyword(param.text.strip()):
                    self.currentLocalsTable[param.text.strip()] = localId
                    localId += 1

        out = functionType + ' ' + '.'.join([self.className, functionName]) + ' ' + str(localId) + '\n'
        for statement in body.find('statements'):
            out += self._generate_statement(statement)
        return out

    def _generate_statement(self, root):
        out = ''
        if root.tag == 'letStatement':
            out = self._generate_let_statement(root)
        if root.tag == 'ifStatement':
            out = self._generate_if_statement(root)
        if root.tag == 'whileStatement':
            out = self._generate_while_statement(root)
        if root.tag == 'doStatement':
            out = self._generate_do_statement(root)
        if root.tag == 'returnStatement':
            out = self._generate_return_statement(root)
        return out

    def _generate_let_statement(self, root):
        expNum = len(root.findall('expression'))
        out = self._generate_expression(root.findall('expression')[expNum - 1])
        varName = root[1].text.strip()
        if varName in self.currentArgsTable:
            type = 'argument ' + str(self.currentArgsTable[varName])
        else: #varName in self.currentLocalsTable
            type = 'local ' + str(self.currentLocalsTable[varName])
        # TODO: add fields and static handling.
        if '[' in [element.text for element in root]:
            # this is an array call.
            out += self._generate_expression(root.findall('expression')[0])
            out += '\n'.join('push ' + type, 'add', 'pointer 1', 'pop that 0') + '\n'
        else:
            out += 'pop ' + type + '\n'
        return out

    def _generate_if_statement(self, root):
        ifNum = self.nextIfNum
        self.nextIfNum += 1
        out = self._generate_expression(root.find('expression'))
        out += 'if-goto IF_TRUE' + str(ifNum) + '\n'
        out += "goto IF_FALSE" + str(ifNum) + '\n'
        out += "label IF_TRUE" + str(ifNum) + '\n'
        for statement in root.findall('statements')[0]:
            out += self._generate_statement(statement)
        out += "goto IF_END" + str(ifNum) + '\n'
        out += "label IF_FALSE" + str(ifNum) + '\n'
        hasElse = len(root.findall('keyword')) > 1
        if hasElse:
            for statement in root.findall('statements')[1]:
                out += self._generate_statement(statement)
        out += 'label IF_END' + str(ifNum) + '\n'
        return out

    def _generate_while_statement(self, root):
        whileNum = self.nextWhileNum
        self.nextWhileNum += 1
        out = "label WHILE_EXP" + str(whileNum) + '\n'
        out += self._generate_expression(root.find('expression'))
        out += 'not\n'
        out += 'if-goto WHILE_END' + str(whileNum) + '\n'
        for statement in root.find('statements'):
            out += self._generate_statement(statement)
        out += 'goto WHILE_EXP' + str(whileNum) + '\n'
        out += 'label WHILE_END' + str(whileNum) + '\n'
        return out

    def _generate_do_statement(self, root):
        out = self._generate_expression_list(root.find('expressionList'))
        functionName = '.'.join([identifier.text.strip() for identifier in root.findall('identifier')])
        argNum = len(root.find('expressionList').findall('symbol')) + 1
        out += 'call ' + functionName + ' ' + str(argNum) + '\n'
        out += 'pop temp 0\n'
        return out

    def _generate_return_statement(self, root):
        if root.find('expression') is not None:
            out = self._generate_expression(root.find('expression'))
        else:
            out = 'push constant 0\n'
        out += 'return\n'
        return out

    def _generate_expression_list(self, root):
        out = ''
        for exp in root:
            out += self._generate_expression(exp)
        return out

    def _generate_expression(self, root):
        out = ''
        for term in root.findall('term'):
            out += self._generate_term(term)
        if root.find('symbol') is not None:
            out += OPERATORS[root.find('symbol').text.strip()] + '\n'
        return out

    def _generate_term(self, root):
        if root.find('expression') is not None:
            out = self._generate_expression(root.find('expression'))
        elif root[0].tag == 'symbol' and root[0].text.strip() in UNARY_OPERATORS.keys():
            out = self._generate_term(root[1])
            out += UNARY_OPERATORS[root[0].text.strip()] + '\n'
        elif root[0].tag == 'integerConstant':
            out = 'push constant ' + root[0].text.strip() + '\n'
        elif root.find('symbol') is not None and root.find('symbol').text.strip() in ['.', '(']:
            out = self._generate_expression_list(root.find('expressionList'))
            functionName = '.'.join([identifier.text.strip() for identifier in root.findall('identifier')])
            argNum = len(root.find('expressionList').findall('symbol')) + 1
            out += 'call ' + functionName + ' ' + str(argNum) + '\n'
        elif root[0].tag == 'identifier':
            if root[0].text.strip() in self.classFields:
                out = 'push field ' + str(self.classFields[root[0].text.strip()]) + '\n'
            elif root[0].text.strip() in self.classStatics:
                out = 'push static ' + str(self.classStatics[root[0].text.strip()]) + '\n'
            elif root[0].text.strip() in self.currentArgsTable:
                out = 'push argument ' + str(self.currentArgsTable[root[0].text.strip()]) + '\n'
            elif root[0].text.strip() in self.currentLocalsTable:
                out = 'push local ' + str(self.currentLocalsTable[root[0].text.strip()]) + '\n'
            else:
                out = ''
        elif root[0].tag == 'keyword':
            out = KEYWORDS[root[0].text.strip()]
        else:
            out = root[0].text

        return out

    def generate_vm(self, xml):
        return self._generate_class(ET.fromstring(xml))
