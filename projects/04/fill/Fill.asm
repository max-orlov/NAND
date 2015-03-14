// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

@i
M=0
@SWITCH
M=0
(LOOP)
	@24576		//Listen to keyboard
	D=M
	@WHITEN
	D; JEQ
	@BLACKEN
	D; JGT
	(BLACKEN)		//Blacken the screen
		@SWITCH		// Check for swith from white to black
		D=M
		M=1
		@CLEAR_COUNT
		D; JEQ
		
		@SCREEN		// Fill the screen with black dots
		D=A
		@i
		A=D+M
		M=1
		@CONTINUE
		0; JMP
	(WHITEN)		//Whiten the screen
		@SWITCH		// Check for a switch from black to white
		D=M-1
		M=0
		@CLEAR_COUNT
		D; JEQ
		
		@SCREEN		// Clear the screen
		D=A
		@i
		A=D+M
		M=0
	(CONTINUE)
		@i
		M=M+1
		@LOOP
		0; JMP
	(CLEAR_COUNT)
		@i
		M=0
		@LOOP
		0; JMP
(END)