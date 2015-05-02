def get_address(key):
    return {
        "SP": "SP",     #0
        "LCL": "LCL",   #1
        "ARG": "ARG",   #2
        "THIS": "THIS", #3
        "THAT": "THAT", #4
        "local": "LCL", #5
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "pointer": 3,
        "temp": 5,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "static": 16,
        "constant": "CONSTANT"
    }[key]
