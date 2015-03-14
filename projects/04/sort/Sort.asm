// The program input will be at R14(starting address),R15(length of array).
// The program should sort the array starting at the address in R14 with length specified in R15.
// The sort is in descending order - the largest number at the head of the array.

@index		// the index of the array - set to 0.
M=0

(LOOP)
	@index				// if R15-index <= 0 GOTO END
	D=M
	@R15
	D=M-D
	@END
	D;JLE
	
	@R14				// start_location = R14+index
	D=M
	@start_location
	M=D
	D=M
	@index
	D=D+M
	@start_location
	M=D
	
	D=M
	@inner_location 	// set the location for the inner loop as the start location.
	M=D
	@max_location		// max_location = inner_location
	M=D
	
	@start_location		// max = RAM[start_location]
	A=M
	D=M
	@max
	M=D
	
	@index				// i = index (19)
	D=M
	@i
	M=D
	
	(INNER_LOOP)
		@i				// if R15-i <= 0 exit inner loop (19)
		D=M
		@R15
		D=M-D
		@END_INNER_LOOP
		D;JLE
		
		@inner_location	// elem = RAM[inner_location]
		A=M
		D=M
		@elem
		M=D
		D=M
		
		@max			// if temp_elem <= max move on.
		D=D-M
		@MOVE_ON
		D;JLE
		
			@elem				// max = elem
			D=M
			@max
			M=D
			@inner_location		// max_location = inner_location
			D=M
			@max_location
			M=D
		(MOVE_ON)
		
		@i				// i++
		M=M+1
		@inner_location	// inner_location++
		M=M+1
		
		@INNER_LOOP
		0;JMP
(END_INNER_LOOP)
	
	// Swap between max location and start location.
	@start_location
	A=M		// temp = RAM[start_location]
	D=M
	@temp	// (22)
	M=D
	
	@max	// RAM[start_location] = max (18)
	D=M
	@start_location
	A=M
	M=D
	
	@temp	// RAM[max_location] = temp (22)
	D=M
	@max_location
	A=M
	M=D
	
	@index	// index++ (16)
	M=M+1
	
	@LOOP	// GOTO LOOP
	0;JMP
(END)