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
@3
A=A+1

M=D
@0

D=A
@SP
A=M
M=D
@0
M=M+1
@SP
M=M-1
A=M
D=M
@THAT
A=M

M=D
@1

D=A
@SP
A=M
M=D
@0
M=M+1
@SP
M=M-1
A=M
D=M
@THAT
A=M
A=A+1

M=D
@ARG
A=M

D=M
@SP
A=M
M=D
@0
M=M+1
@2

D=A
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
@SP
M=M-1
A=M
D=M
@ARG
A=M

M=D
(FibonacciSeries_first_MAIN_LOOP_START)
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
@FibonacciSeries_first_COMPUTE_ELEMENT
D; JNE
@FibonacciSeries_first_END_PROGRAM
0; JMP
(FibonacciSeries_first_COMPUTE_ELEMENT)
@THAT
A=M

D=M
@SP
A=M
M=D
@0
M=M+1
@THAT
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
D=M
@THAT
A=M
A=A+1
A=A+1

M=D
@3
A=A+1

D=M
@SP
A=M
M=D
@0
M=M+1
@1

D=A
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
D=M
@3
A=A+1

M=D
@ARG
A=M

D=M
@SP
A=M
M=D
@0
M=M+1
@1

D=A
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
@SP
M=M-1
A=M
D=M
@ARG
A=M

M=D
@FibonacciSeries_first_MAIN_LOOP_START
0; JMP
(FibonacciSeries_first_END_PROGRAM)
