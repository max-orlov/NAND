import re
import xml.etree.ElementTree as ET

OPERATORS = {'+':    'add',
             '-':    'sub',
             '*':    'call Math.multiply 2',
             '/':    'call Math.divide 2',
             '&lt;': 'lt',
             '&gt;': 'gt',
             }

UNARY_OPERATORS = {'-': 'neg', '~': 'not'}

class Generator():
    def __init__(self):
        self.index = 0
        self.className = None
        self.currentFuncLocals = 0
        self.currentParamsTable = {}

    def _generate_class(self, root):
        out = ''
        self.className = root[1].text.strip()
        self.index += 3
        for var in root.findall('classVarDec'):
            out += self._generate_var_dec(var)
        for subroutine in root.findall('subroutineDec'):
            out += self._generate_function(subroutine)
        return out

    def _generate_var_dec(self, root):
        if 'field' in self.xml_lines[self.index]:
            pass

    def _generate_function(self, root):
        self.currentFuncLocals = 0
        functionType = root[0].text.strip()
        functionName = root[2].text.strip()
        paramList = root.find('parameterList')
        argNum = 0 if len(list(paramList)) == 0 else len(paramList.findall('symbol')) + 1
        out = functionType + ' ' + '.'.join([self.className, functionName]) + ' ' + str(argNum) + '\n'
        for statement in root.find('subroutineBody').find('statements'):
            out += self._generate_statement(statement)
        return out

    def _generate_statement(self, root):
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
        pass

    def _generate_if_statement(self, root):
        pass

    def _generate_while_statement(self, root):
        pass

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
        if root[0].tag == 'symbol' and root[0].text.strip() in UNARY_OPERATORS.keys():
            out = self._generate_term(root[1])
            out += UNARY_OPERATORS[root[0].text.strip()] + '\n'
        if root[0].tag == 'integerConstant':
            out = 'push constant ' + root[0].text.strip() + '\n'
        return out

    def generate_vm(self, xml):
        return self._generate_class(ET.fromstring(xml))
