################################################################# PART A
addi $8, $0, 3          # initial seed
addu $9, $0, $8        # tempS = seed

addi $10, $0, 0          # address counter
sw $10, 0x2000($0)       # store addresss counter to 0x2000
addi $10, $0, 16         # numS = 16
sw $10, 0x2004($0)       # store numS into 0x2004

do_loop: 
        sw $9, 0x2010($11)         # store value $9 into mem address
        addi $10, $0, 1            # odd = 1
        addi $11, $0, 0            # sq = 0

        loop:
            addu $11, $11, $10      # sq = sq + odd
            addi $10, $10, 2        # odd = odd + 2
            addi $8, $8, -1         # seed--
            bne $8, $0, loop        

        sw $11, 0x2008($0)          # store current sq into 0x2008

        addu $8, $0, 0x000000FF     # 00...0011111111
        and $8, $11, $8             # preserves right most byte 
        
        addu $9, $0, 0xFF000000    # 1111111100...00
        and $9, $11, $9            # preserves left most byte
        srl $9, $9, 16             # position left most byte into the right places i.e. 16...9
		
        addu $9, $9, $8            # merge both left and right most bits

        addu $10, $0, 0x0000FFFF    # 00...1111111111111111      
        and $9, $9, $10             # sign extend to 0
        addu $8, $0, $9             # seed = new 16 bit number

        lw $10, 0x2004($0)          # load numS into $10
        addi $10, $10, -1           # numS--
        sw $10, 0x2004($0)          # store numS into 0x2004

        lw $11, 0x2000($0)          # load address counter into $11
        addi $11, $11, 4            # increment adress counter by 4
        sw $11, 0x2000($0)          # store addresss counter to 0x2000

bne $10, $0, do_loop                # if $10 != 0 branch to do_loop 

################################################################# PART B i.

addi $8, $0, 0x2010		# point ot first address
addi $9, $0, 0			# sum = 0
sw $9, 0x2000($0)		# store sum into 0x2000
addi $10, $0, 16		# numS = 16
sw $10, 0x2004($0)       	# store numS into 0x2004
addi $11, $0, 0			# ctr = 0
sw $11, 0x2008($0)		# store ctr into 0x2008

loop1:	lw $9, ($8)		# load seed in current mem address
	addi $10, $0, 0		# i = 0
	
	loop2:	slt $11, $9, $0		# $9 value < 0?
		beq $11, $0, skip	# if $11 = 0 branch to skip
		addi $10, $10, 1 	# i++ when $9 is negative, Hamming weight of a seed
	skip:	sll $9, $9, 1		# logic shift to the left once for every loop
		bne $9, $0, loop2	# while($9 != 0)
		
	lw $11, 0x2000($0)		# load sum into $11
	addu $11, $11, $10		# sum of 1's in all 16 seeds, Total Hamming weight
	sw $11, 0x2000($0)		# store sum into 0x2000
	
	lw $11, 0x2004($0)		# load numS into $11
	addi $11, $11, -1		# decrement numS for each iteration by 1
	sw $11, 0x2004($0)		# store numS into 0x2004
	
	addi $8, $8, 4			# increment address counter by 4
	
bne $11, $0, loop1		# if $11 != 0 branch to loop1

lw $10, 0x2000($0)		# load sum into $10
srl $11, $10, 4			# Average Hamming Weight
sw $11, 0x2000			# store AHW into address 0x2000
