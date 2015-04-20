@30000
D=A
@0
A=M
M=D
@0
M=M+1

@0
D=A
@0
A=M
M=D
@0
M=M+1

@30000
D=A
@0
A=M
M=D
@0
M=M+1

@0
M=M-1
A=M

D=M
@0
M=M-1
A=M

D=M-D
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M

D=M
@15
M=D
@0
M=M-1
A=M

D=M
@14
M=D
@15
D=D-M
@13
M=D
@14
D=M
@_input_4_jgt_1lt
D; JLT
@15
D=M
@_input_4_jgt_fin
D; JGE
D=1
@_input_4_jgt_check
0; JMP
(_input_4_jgt_1lt)
@15
D=M
@_input_4_jgt_fin
D; JLT
D=-1
@_input_4_jgt_check
0; JMP
(_input_4_jgt_fin)
@13
D=M
(_input_4_jgt_check)
@_input_4_jgt_is
D; JGT
@_input_4_jgt_not
0; JMP
(_input_4_jgt_is)
D=-1
@_input_4_jgt_end
0; JMP
(_input_4_jgt_not)
D=0
(_input_4_jgt_end)
@0
A=M
M=D
@0
M=M+1
