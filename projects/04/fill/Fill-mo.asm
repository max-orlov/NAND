// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.


//init color
@COLOR
M = 0

//init row
@255
D = A
@ROW
M = D

//init col
@31
D = A
@COL
M = D

//init screen
@SCREEN
D = A

@STARTINDEX
M = D

@curindex
    M = D

@colindex
    M = 0

@rowindex
    M = 0
// the infinite loop - always colors
(INFLOOP)
    @colindex
    D=M
    @COL
    D=D-M
    @INITCOL
	D;JGT
	
    @rowindex
    D=M
    @ROW
    D=D-M
    @INITROW
	D;JGT

    @KBD
    D=M
    @WHITE
    D;JEQ 
    @BLACK
    0;JMP
//color white
    (WHITE)
        @COLOR
        M = 0
        @UNBLACK
        0;JMP
//color black
    (BLACK)
    @COLOR
    M = -1
    
    (UNBLACK)

    @COLOR
    D=M

    @curindex
    A=M
    M=D
    
    @curindex
    M=M+1
    @colindex
    M=M+1
    @INFLOOP
    0;JMP

//Zero cols...
(INITCOL)
    @colindex
    M = 0
    @rowindex
    M = M + 1
    @INFLOOP
    0;JMP

(INITROW)
    @rowindex
    M = 0
    @STARTINDEX
    D = M
    @curindex
    M = D
    @INFLOOP
    0;JMP

@INFLOOP
0;JMP


