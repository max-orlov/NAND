__author__ = 'maxorlov'
from enum import Enum


class VMCommands(Enum):
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"


def get_c_command(command):
    if command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'] or command == "arithmetic":
        return VMCommands.C_ARITHMETIC
    else:
        return {
            "push": VMCommands.C_PUSH,
            "pop": VMCommands.C_POP,
            "label": VMCommands.C_PUSH,
            "goto": VMCommands.C_GOTO,
            "if-goto": VMCommands.C_GOTO,
            "function": VMCommands.C_FUNCTION,
            "return": VMCommands.C_RETURN,
            "call": VMCommands.C_CALL
        }[command]

