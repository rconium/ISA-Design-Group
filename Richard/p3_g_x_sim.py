# Function for converting hex to binary
def hex2bin(argument):
    switcher = {
        '0': "0000",
        '1': "0001",
        '2': "0010",
        '3': "0011",
        '4': "0100",
        '5': "0101",
        '6': "0110",
        '7': "0111",
        '8': "1000",
        '9': "1001",
        'A': "1010",
        'B': "1011",
        'C': "1100",
        'D': "1101",
        'E': "1110",
        'F': "1111",
    }
    return switcher.get(argument, "ERROR")

## Table for all instruction opcodes
def getInstr(argument):
    switcher = {
        "0000": "refresh",
        "0001": "addi",
        "0010": "addu",
        "0011": "store",
        "0100": "mult",
        "0101": "splice",
        "0110": "jne",
        "0111": "mark",
        "1000": "slti",
        "1001": "beq",
        "1010": "sll",
        "1011": "srl",
        "1100": "load",
    }
    return switcher.get(argument, "ERROR")

## Table for all general purpose registers
def bin2gregi(argument):
    switcher = {
        '00': "$0",
        '01': "$1",
        '10': "$2",
        '11': "$3",
    }
    return switcher.get(str(argument), "ERROR")

## Two's complement for 2 bits
def getTwosComp2(argument):
    if (argument[0] == '1'):
        num = int(argument,2)
        val = -2 + (num - 2)
    else:
        val = int(argument, 2)
    return int(val)

## Two's complement for 8 bits
def getTwosComp8(argument):
    if (argument[0] == '1'):
        num = int(argument,2)
        val = -128 + (num - 128)
    else:
        val = int(argument, 2)
    return int(val)

## Two's complement for 32 bits
def getTwosComp32(argument):
    if (argument[0] == '1'):
        num = int(argument,2)
        val = -2147483648 + (num - 2147483648)
    else:
        val = int(argument, 2)
    return int(val)

## Returns bit size of a non-negative number
def getBitSize(argument):
    sum = 0
    while argument >> sum:
        sum += 1

    return sum

## Inserts new instruction so long as there is no duplicates on the same PC
def insertList(pc, newline):
    check = False

    for a, b in printList:
        if (a == pc and b == newline):
            check = True

    if (check == False):
        printList.append((pc, newline))

## Returns a zero extended 16 bit number
def zeroExtend16(argument):
    zext = 16 - len(argument)

    while (zext != 0):
        argument = "0" + argument
        zext -= 1   
    
    return argument

## Returns a zero extended 8 bit number
def zeroExtend8(argument):
    zext = 8 - len(argument)

    while (zext != 0):
        argument = "0" + argument
        zext -= 1   
    
    return argument

Register = [0 for i in range(4)]
printList = []

def Simulate(I):
    oFile = open("p3_g_x_prpg_sim_out_251.txt.", "w")
    print("Welcome to the Simulation!")
    op =  ""
    rs = ""
    rt = ""
    rx = ""
    uno = 0
    dos = 0
    imm = ""
    newLine = ""

    Memory = [0 for i in range(64)]            # list for memory content
    PC = 0
    instructionCount = 0

    finished = False
    while(not(finished)):
        binary = I[PC]              # get instruction binary
        if (binary == "10011111"):   # END instruction
            finished = True

        op = binary[0:4]

        # refresh
        if (op == "0000"):
            rt = binary[4:6]
            imm = binary[6:8]

            Register[int(rt, 2)] = getTwosComp2(imm)

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + str(getTwosComp2(imm))
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # addi
        elif (op == "0001"):
            rt = binary[4:6]
            imm = binary[6:8]

            Register[int(rt, 2)] = Register[int(rt, 2)] + getTwosComp2(imm)

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + str(getTwosComp2(imm))
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # addu
        elif (op == "0010"):
            rt = binary[4:6]
            rs = binary[6:8]

            Register[int(rt, 2)] = Register[int(rt, 2)] + Register[int(rs, 2)]

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + bin2gregi(rs)
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # store
        elif (op == "0011"):
            rt = binary[4:6]
            rs = binary[6:8]

            Memory[abs(Register[int(rs, 2)])] = Register[int(rt, 2)]
            
            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + bin2gregi(rs)
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # mult
        elif (op == "0100"):
            rt = binary[4:6]
            rs = binary[6:8]

            temp16 = bin(Register[int(rt, 2)] * Register[int(rs, 2)])[2:]
            
            if (len(temp16) < 16):
                temp16 = zeroExtend16(temp16)   
            print("temp16 ", temp16)        

            Register[0] = int(temp16[8:16], 2)
            Register[1] = int(temp16[0:8], 2)

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + bin2gregi(rs)
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # splice
        elif (op == "0101"):
            rt = binary[4:6]
            rs = binary[6:8]
            r0 = zeroExtend8(str(bin(Register[0]))[2:])
            r1 = zeroExtend8(str(bin(Register[1]))[2:])

            r0 = r0[4:8]
            r1 = r1[0:4]

            Register[1] = int(r1 + r0, 2)  

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + bin2gregi(rs)
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # jne
        elif (op == "0110"):
            rt = binary[4:6]
            imm = binary[6]
            rx = binary[7]

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + str(int(imm, 2)) + " " + rx
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            if (Register[int(rt, 2)] != int(imm, 2)):
                if (rx == '0'):
                    PC = uno
                elif (rx == '1'):
                    PC = dos
            else:
                PC += 1

            insertList(PC, newLine)
            instructionCount += 1

        # mark
        elif (op == "0111"):
            rx = binary[7]

            if (rx == '0'):
                uno = PC + 1
            elif (rx == '1'):
                dos = PC + 1

            newLine = getInstr(op) + " " + rx
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # slti
        elif (op == "1000"):
            rt = binary[4:6]
            imm = binary[6:8]

            if (Register[int(rt, 2)] < int(imm, 2)):
                Register[3] = 1
            else:
                Register[3] = 0

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + str(int(imm))
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # beq
        elif (op == "1001"):
            rt = binary[4:6]
            imm = binary[6:8]

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + str(getTwosComp2(imm))
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            if (Register[int(rt, 2)] == 0):
                PC = PC + 1 + getTwosComp2(imm)
            else:
                PC += 1

            insertList(PC, newLine)
            instructionCount += 1
            
        # sll
        elif (op == "1010"):
            rt = binary[4:6]
            imm = binary[6:8]

            imm1 = Register[int(rt,2)] << int(imm,2)

            if (imm1 < -2147483648):
                hold = bin(imm1)[3:]

                imm1 = getTwosComp32(hold)
                Register[int(rt,2)] = -(imm1)

            elif (imm1 >= 2147483648):
                temp = bin(imm1)[2:]
                imm1 = getTwosComp32(temp)
                Register[int(rt,2)] = imm1

            else:
                Register[int(rt,2)] = imm1

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + str(int(imm))
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # srl
        elif (op == "1011"):
            rt = binary[4:6]
            rs = binary[6:8]

            Register[int(rt,2)] = Register[int(rt,2)] >> Register[int(rs,2)]
            temp = bin(Register[int(rt,2)])

            if (temp[0] == '-'):
                Register[int(rt,2)] = abs(Register[int(rt,2)])

                ogBitSize = getBitSize(Register[int(rt,2)])
                val = Register[int(rt,2)] ^ 255                         # get the
                val += 1                                                # two's complement

                if(ogBitSize > getBitSize(val)):                        # check if there are missing zeroes
                    zeroes = ogBitSize - getBitSize(val)
                    temp = bin(val)[2:]
                    while zeroes!=0:                                    # concatanate the missing zeroes
                        temp = '0' + temp
                        zeroes -= 1
                    temp = '1' + temp

                Register[int(rt,2)] = int(temp, 2)

            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + bin2gregi(rs)
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

        # load
        elif (op == "1100"):
            rt = binary[4:6]
            rs = binary[6:8]

            Register[int(rt, 2)] = Memory[abs(Register[int(rs, 2)])]
            
            newLine = getInstr(op) + " " + bin2gregi(rt) + " " + bin2gregi(rs)
            pr = "PC[" + str(PC) + "] " + newLine
            print(pr)

            insertList(PC, newLine)
            PC += 1
            instructionCount += 1

    print("\nSpecial Register Contents: [" + str(uno) + " " + str(dos) + "]")
    print("Register Contents: ", Register)
    print("Memory Array: ", Memory)
    print("Total Instructions Count: ",instructionCount)

    # Write all instructions to an output file
    printList.sort()
    for a, b in printList:
        oFile.write(b + "\n")

    oFile.close()

def main():
    iFile = open("p3_g_x_prpg_251.txt", "r")
    I  = []
    binary = ""
    word = ""

    for line in iFile:
        if (line == "\n" or line[0] == "#" ):
            continue
        if (line == "0x9F"):
            # prints the register contents
            print("Registers contents:", Register)
            print("\nThankYou")
            exit()
            
        word = word + line[2:4]        # get each line, but ignore 0x

        for i in word:
            binary = binary + hex2bin(i)    # convert to binary
        I.append(binary)
        word = ""
        binary =""
    Simulate(I)
    print("\n***SIMULATION FINISHED***")

if __name__== "__main__":
  main()
