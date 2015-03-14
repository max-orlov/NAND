// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
	// we add R0 to R2 (starting from 0), R1 times
	
	@R2		// set R2 to 0.
	M=0
	
	@i		// set i to 0
	M=1
(LOOP)
	@i		// if (i - in2) >= 0 GOTO END
	D=M
	@R1
	D=D-M
	@END
	D;JGT
	@R0	// R2 = R2 + in1
	D=M
	@R2
	M=D+M
	@i		// i++
	M=M+1
	@LOOP	// GOTO LOOP
	0;JMP
(END)
