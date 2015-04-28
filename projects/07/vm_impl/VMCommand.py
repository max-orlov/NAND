from enum import Enum


class VMCommandTypes(Enum):
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"

c_command_dictionary={
    "push": VMCommandTypes.C_PUSH,
    "pop": VMCommandTypes.C_POP,
    "label": VMCommandTypes.C_LABEL,
    "goto": VMCommandTypes.C_GOTO,
    "if-goto": VMCommandTypes.C_IF,
    "function": VMCommandTypes.C_FUNCTION,
    "return": VMCommandTypes.C_RETURN,
    "call": VMCommandTypes.C_CALL,
    "add":  VMCommandTypes.C_ARITHMETIC,
    "sub":  VMCommandTypes.C_ARITHMETIC,
    "neg":  VMCommandTypes.C_ARITHMETIC,
    "eq":  VMCommandTypes.C_ARITHMETIC,
    "gt":  VMCommandTypes.C_ARITHMETIC,
    "lt":  VMCommandTypes.C_ARITHMETIC,
    "and":  VMCommandTypes.C_ARITHMETIC,
    "or":  VMCommandTypes.C_ARITHMETIC,
    "not":  VMCommandTypes.C_ARITHMETIC
}

class VMCommandsArithmeticTypes(Enum):
    ADD = 'add',
    SUB = 'sub',
    NEG = 'neg',
    EQ = 'eq',
    GT = 'gt',
    LT = 'lt',
    AND = 'and',
    OR = 'or',
    NOT = 'not'

c_arithmetic_dictionary ={
    'add': VMCommandsArithmeticTypes.ADD,
    'sub': VMCommandsArithmeticTypes.SUB,
    'neg': VMCommandsArithmeticTypes.NEG,
    'eq': VMCommandsArithmeticTypes.EQ,
    'gt': VMCommandsArithmeticTypes.GT,
    'lt': VMCommandsArithmeticTypes.LT,
    'and': VMCommandsArithmeticTypes.AND,
    'or': VMCommandsArithmeticTypes.OR,
    'not': VMCommandsArithmeticTypes.NOT
}