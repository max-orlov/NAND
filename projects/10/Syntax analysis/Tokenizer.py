__author__ = 'Maxim'

import re

symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


def __is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def __is_keyword(s):
    return s in ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']


def __is_string(s):
    return len(s) > 2 and s[0] == "'" and s[-1] == "'"


def __is_symbol(s):
    return s in symbols


def __is_identifier(s):
    return re.search('\W*', s).group(0) is not None


def __clear_comments(s):
    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", s)
    string = re.sub(re.compile("//.*?\n"), "", string)
    return string


def tokenize(str_input):
    str_output = "<tokens>" + "\n"
    pattern = '([^a-zA-Z0-9_\"]|{})'.format(['\{}'.format(k)] for k in symbols)
    no_comments = __clear_comments(str_input)

    for t in [k.strip() for k in re.split(pattern, no_comments) if k.strip() != ""]:
        str_output += __get_token(t) + "\n"

    str_output += "</tokens>" + "\n"
    return str_output


def __get_token(t):
    s = "<{0}> {1} </{0}>"
    if __is_keyword(t):
        return s.format("keyword", t)
    elif __is_symbol(t):
        if t in ['>', '<', '""', "&"]:
            return s.format("symbol", {
                '>': "&lt;",
                '<': "&gt;",
                '""': "&quot;",
                '&': "&amp;"
            }[t])
        else:
            return s.format("symbol", t)
    elif __is_int(t):
        return s.format("integerConstant", t)
    elif __is_string(t):
        return s.format("stringConstant", t[1:-1])
    elif __is_identifier(t):
        return s.format("identifier", t)
