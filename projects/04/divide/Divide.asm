// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// The program input will be at R13,R14 
// while the result R13/R14 will be store at R15.

@R13
D = M
@RUNNER_ENU
M = D

@R14
D = M
@RUNNER_DEN
M = D

@RUNNER_DEG
M = 0

@R15
M = 0

// Finding the maximum Degree for 2 and the maximum value.
(FIND_MAX_DEG)
	@RUNNER_DEN
	D = M<<
	@RUNNER_ENU
	D = M - D
	@NEXT1
	D; JGE
	@PHASE_2
	0; JMP
	(NEXT1)
		@RUNNER_DEN
		M = M<<
		@RUNNER_DEG
		M = M + 1
		@FIND_MAX_DEG
		0; JMP

//Calculating the Result
(PHASE_2)
	@RUNNER_DEN			//Load the running denuminator into M
	D = M				//Push it into D
	@RUNNER_ENU			//Load the running enumerator into M
	D = M - D			//Subtract it from the current result
	@ADD				//Load the addition function into M 
	D; JGE				//If the current enumerator enumerator >= current denominator jump to add
	@NEXT2				//Load the Next function into M
	0; JMP				//if neither applies, jump to next
	
	(ADD)				//Add the 2^current_deg to F15
		@RUNNER_DEG		//Saving the old values in order to add to F15.
		D = M			// Load the current degree
		@index			// into the 
		M = D			// index
		@TMP_SUM		// set the mid sum 		
		M = 1			// to 1

	(LOOP)				//Calculating 2^current_deg into TMP_SUM
		@index
		D = M
		@FIN
		D; JEQ
		@TMP_SUM
		M = M<<
		@index
		M = M - 1
		@LOOP
		0; JMP
		
	(FIN)				
		@RUNNER_DEN		// Update the denominator by usage
		D = M
		@RUNNER_ENU		// Update the enumerator by usage
		M = M - D
		@TMP_SUM		// Adding the TMP_SUM value to F15
		D = M
		@R15		
		M = M + D
	
	(NEXT2)				
		@RUNNER_DEN		// Update the denomintor by step;
		M = M>>
		@RUNNER_DEG		// Update the degree by step 
		M = M - 1
		D = M
		@END			// End the algorithm if the degree is < 0
		D; JLT
		@PHASE_2		// Restart the loop
		0; JMP
(END)