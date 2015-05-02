//NEW FUNCTION : Main.fibonacci
(Main.fibonacci)
D=0
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
@15
M=D
@SP
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
@_Main_3_jlt_1lt
D; JLT
@15
D=M
@_Main_3_jlt_fin
D; JGE
D=1
@_Main_3_jlt_check
0; JMP
(_Main_3_jlt_1lt)
@15
D=M
@_Main_3_jlt_fin
D; JLT
D=-1
@_Main_3_jlt_check
0; JMP
(_Main_3_jlt_fin)
@13
D=M
(_Main_3_jlt_check)
@_Main_3_jlt_is
D; JLT
@_Main_3_jlt_not
0; JMP
(_Main_3_jlt_is)
D=-1
@_Main_3_jlt_end
0; JMP
(_Main_3_jlt_not)
D=0
(_Main_3_jlt_end)

@SP
A=M
M=D
@0
M=M+1
@SP
M=M-1
A=M
D=M
@Main_IF_TRUE
D; JNE
@Main_IF_FALSE
0; JMP
(Main_Main.fibonacci_IF_TRUE)
@ARG
A=M

D=M
@SP
A=M
M=D
@0
M=M+1
@LCL
D=M
@13
M=D
@5
D=D-A
A=D
D=M
@14
M=D
@SP
M=M-1
A=M
D=M
@ARG
M=D
//SETTING SP

@ARG
D=M
@SP
M=D+1
//SETTING THAT

@13
D=M-1
A=D
D=M
@THAT
M=D
//SETTING THIS

@13
D=M-1
D=D-1
A=D
D=M
@THIS
M=D
//SETTING ARG

@13
D=M-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
//SETTING LCL

@13
D=M-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
//GOTO RET

@14
A=M
0; JMP
(Main_Main.fibonacci_IF_FALSE)
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
@Main.fibonacci_return
D=A
@SP
A=M
M=D
@0
M=M+1
@LCL
D=M
@SP
A=M
M=D
@0
M=M+1
@ARG
D=M
@SP
A=M
M=D
@0
M=M+1
@THIS
D=M
@SP
A=M
M=D
@0
M=M+1
@THAT
D=M
@SP
A=M
M=D
@0
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0; JMP
(Main.fibonacci_return)
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
@Main.fibonacci_return
D=A
@SP
A=M
M=D
@0
M=M+1
@LCL
D=M
@SP
A=M
M=D
@0
M=M+1
@ARG
D=M
@SP
A=M
M=D
@0
M=M+1
@THIS
D=M
@SP
A=M
M=D
@0
M=M+1
@THAT
D=M
@SP
A=M
M=D
@0
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0; JMP
(Main.fibonacci_return)
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
@LCL
D=M
@13
M=D
@5
D=D-A
A=D
D=M
@14
M=D
@SP
M=M-1
A=M
D=M
@ARG
M=D
//SETTING SP

@ARG
D=M
@SP
M=D+1
//SETTING THAT

@13
D=M-1
A=D
D=M
@THAT
M=D
//SETTING THIS

@13
D=M-1
D=D-1
A=D
D=M
@THIS
M=D
//SETTING ARG

@13
D=M-1
D=D-1
D=D-1
A=D
D=M
@ARG
M=D
//SETTING LCL

@13
D=M-1
D=D-1
D=D-1
D=D-1
A=D
D=M
@LCL
M=D
//GOTO RET

@14
A=M
0; JMP
//NEW FUNCTION : Sys.init
(Sys.init)
D=0
@4
D=A
@SP
A=M
M=D
@0
M=M+1
@Main.fibonacci_return
D=A
@SP
A=M
M=D
@0
M=M+1
@LCL
D=M
@SP
A=M
M=D
@0
M=M+1
@ARG
D=M
@SP
A=M
M=D
@0
M=M+1
@THIS
D=M
@SP
A=M
M=D
@0
M=M+1
@THAT
D=M
@SP
A=M
M=D
@0
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0; JMP
(Main.fibonacci_return)
(Sys_Sys.init_WHILE)
@Sys_WHILE
0; JMP
