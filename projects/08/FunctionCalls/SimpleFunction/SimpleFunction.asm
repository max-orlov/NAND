//NEW FUNCTION : SimpleFunction.test
(SimpleFunction.test)
D=0
//PUSHING
@SP
A=M
M=D
@0
M=M+1
//PUSHING
@SP
A=M
M=D
@0
M=M+1
@LCL
A=M

D=M
@SP
A=M
M=D
@0
M=M+1
@LCL
A=M
A=A+1

D=M
@SP
A=M
M=D
@0
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M+D
@SP
A=M
M=D
@0
M=M+1
@SP
M=M-1
A=M
D=!M
@SP
A=M
M=D
@0
M=M+1
@ARG
A=M

D=M
@SP
A=M
M=D
@0
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M+D
@SP
A=M
M=D
@0
M=M+1
@ARG
A=M
A=A+1

D=M
@SP
A=M
M=D
@0
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@0
M=M+1
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
D=M-1
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0; JMP
