def get_address(segment, index=0, file_name=""):
    assembly_commands = [{
                             "SP": "@SP",  # 0
                             "LCL": "@LCL",  # 1
                             "ARG": "@ARG",  # 2
                             "THIS": "@THIS",  # 3
                             "THAT": "@THAT",  # 4
                             "local": "@LCL",  # 1
                             "argument": "@ARG",  # 2
                             "this": "@THIS",  # 3
                             "that": "@THAT",  # 4
                             "R13": "@R13",
                             "R14": "@R14",
                             "R15": "@R15",
                             "static": "@{}.{}".format(file_name, index),
                             "pointer": "@{}".format(3),
                             "temp": "@{}".format(5),
                             "constant": "@{}".format(index)
                         }[segment]]

    if segment not in ["static", "constant", "R13", "R14", "R15"]:
        # Deciding from where to run
        if segment not in ["temp", "pointer", "constant"]:
            assembly_commands.append("A=M")

        # find the right index
        for _ in range(0, index):
            assembly_commands.append("A=A+1")

    # returning this great string.
    return "\n".join(assembly_commands) + "\n"

