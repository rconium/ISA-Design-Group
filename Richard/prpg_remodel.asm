# PART A
addi $8, $0, 3 # initial seed
addi $9, $0, 16 # numS = 16
addi $10,$0, 0 # increment address by 4 bytes
addi $13, $0, 0 # ctr = 0
addu $14, $0, $8 # tempS = seed
addu $11, $0, 0x000000FF # 00...0011111111
addu $17, $0, 0xFF000000 # 1111111100...00
addu $18, $0, 0x0000FFFF # 00...1111111111111111

do_loop: 	addi $12, $0, 0 # i = 0
		sw $14, 0x2010($10) # store value $14 into mem address

	for_loop:	addi $15, $8, -1 # seed - 1	
			slt $16, $12, $15 # i < seed - 1?
			beq $16, $0, for_end # if $16 = 0 jump to for_end
			addu $14, $14, $8 # tempS += seed, add current number n - 1 times
			addi $12, $12, 1 # i++
			beq $0, $0, for_loop
			#j for_loop
	
	for_end:	addi $13, $13, 1 # ctr++		
			addi $10, $10, 4 # increment address incrementer by 4 
			and $12, $14, $11 # preserves right most bits
			and $15, $14, $17 # preserves left most bits
			srl $15, $15, 16 # position left most bits into the right places i.e. 16...9
			addu $14, $15, $12 # merge both left and right most bits
			and $14, $14, $18 # sign extend to 0 
			addu $8, $0, $14 # seed = new 16 bit number
	
slt $16, $13, $9 # ctr < numS
bne $16,$0, do_loop # if $16 != 0 jump to do_loop 
