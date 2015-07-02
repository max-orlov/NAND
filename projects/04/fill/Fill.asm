// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

(Reset)
@SCREEN
D=A
@ptr
M=D

(loop)
	@color
	D=M
	@ptr
	A=M
	M=D
	@ptr
	M=M+1
	@KBD
	D=M
	@SetWhite
	D; JEQ
	@color
	M=-1
	@End
	0; JMP
	(SetWhite)
	@color
	M=0
	
(End)
@ptr
D=M
@24576
D=D-A
@Reset
D; JEQ
@loop
0; JMP
	


