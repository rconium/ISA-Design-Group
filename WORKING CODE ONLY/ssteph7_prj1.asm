addi $8, $0, 65535		# test value setting
addi $9, $0, 1			# for incrementing
addi $19, $0, 0			# initialize total hamming weight

addi $16, $0, 15		# holds number of seeds to generate after s0
addi $14, $0, 0x2010		# initial memory location for storing seeds (register 14)
addu $15, $0, $8		# temporary variable holding s0
sw $8, ($14)			# store seed value in register at address in $14
addi $14, $14, 4		# increment storage address by one word
bne $16, $0, hamming_weight	# run the loop to generate random numbers


get_random:
	# square the seed value with square loop, by repeated addition
	square:		
		addu $11, $11, $15	# $11 will hold the sum/"multiplication"
		beq $8, $0, skip	# keeps zero from going into the negative values
		sub $8, $8, $9		# decrement initial seed value (it counts)
		skip:
		bne $8, $0, square	# repeat the repeated addition [seed number] of times
		
		# bitmask the most significant and lest significant 8 bits of the squared value, store in $17 and $18
		andi $17, $11, 0xFF
		lui, $1, 0xFF00
		ori $1, $1, 0
		and $18, $11, $1
		
		
		srl $18, $18, 16	# shift right by 16 bits the MSB's of the squared value stored in $18
		or $11, $17, $18	# merge $17 and $18 to get the new 16-bit number, this is seed-i
		sw $11 ($14)		# store this value in address stored in $14
		addi $14, $14, 4	# increment address by one word
		sub $16, $16, $9	# decrement the counter variable
		addu $15, $0, $11	# set the new seed value to be squared
		beq $15, $0, hamming_weight_average
		addu $8, $0, $11	# set the new counter register for squareing
		addi $11, $0, 0		# set sum for squareing to zero		
		j hamming_weight
	check:
		bne $16, $0, get_random 	# rerun the loop until tasks left is zero
		j hamming_weight_average
	hamming_weight:
		addu $10, $0, $15	#initialize a test value
		addi $13, $0, 0		#temporary variable to store result of and-ing 
		addi $12, $0, 0		#counter variable to hold number of 1's
		andi $12, $10, 1	#check the least significant bit, $12 = $10 and 1

		count_loop:
			srl $10, $10, 1		#logical shift the value in $10 right by one bit
			andi $13, $10, 1	#check the least significant bit, $13 = $10 and 1
			add $12, $12, $13	#add the result of the and operation to $12
			bne $10, $0, count_loop	#repeat loop while the value in $10 is not zero, when it reaches zero, the program ends
			addu $19, $19, $12	# add to total hamming weight count
			j check
	hamming_weight_average:
		addi $14, $0, 0x2050
		srl $19, $19, 4			# divide by 16 to get average hemming weight
		sw $19, -0x50($14)		# store average at address 0x2000
		addi $14, $14, -0x3C		# return the address to location of s0

	# all registers are available again because all previous data has been stored
	addi $23, $0, 0x200C	#stores register adress of S0 into $24; incrementing address
	addi $20, $0, 0x204C	#holds final values
	
	repeat:
	addi $23, $23, 4	#increments address by 4 to move onto the next number
	lw $21, ($23)		#takes word from memory and puts it into $21
	addu $22, $22, $21	# $22 holds the total
	bne $23, $20, repeat	#repeats until all values are stored
	srl, $22, $22, 4	#this divides by 16
	sw $22, -0x40($23)	# stores avg back into 0x200C
