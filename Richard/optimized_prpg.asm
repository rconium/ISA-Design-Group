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