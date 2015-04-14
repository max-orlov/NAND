__author__ = 'maxorlov'
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


def get_c_command(command):
    if command in VMCommandsArithmeticTypes:
        return VMCommandTypes.C_ARITHMETIC
    else:
        return {
            "push": VMCommandTypes.C_PUSH,
            "pop": VMCommandTypes.C_POP,
            "label": VMCommandTypes.C_PUSH,
            "goto": VMCommandTypes.C_GOTO,
            "if-goto": VMCommandTypes.C_GOTO,
            "function": VMCommandTypes.C_FUNCTION,
            "return": VMCommandTypes.C_RETURN,
            "call": VMCommandTypes.C_CALL
        }[command]

