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
        'a': "1010",
        'b': "1011",
        'c': "1100",
        'd': "1101",
        'e': "1110",
        'f': "1111",
    }
    return switcher.get(argument, "nothing")

## Table for all instruction opcodes
def getInstr(argument):
    switcher = {
        "0000": "refresh",
        "0001": "addi",
        "0010": "addu",
        "0011": "store",
        "101010": "slt",
        "100100": "and",
        "100101": "or",
        "000000": "sll",
        "000010": "srl",
        "100110": "xor",
        "000100": "beq",
        "000101": "bne",
        "100011": "lw",
        "100010": "sub",
        "001101": "ori",
        "001111": "lui",
    }
    return switcher.get(argument, "nothing")

## Table for all instruction registers
def dec2regi(argument):
    switcher = {
        '0': "$0",
        '1': "$1",
        '2': "$2",
        '3': "$3",
        '4': "$4",
        '5': "$5",
        '6': "$6",
        '7': "$7",
        '8': "$8",
        '9': "$9",
        '10': "$10",
        '11': "$11",
        '12': "$12",
        '13': "$13",
        '14': "$14",
        '15': "$15",
        '16': "$16",
        '17': "$17",
        '18': "$18",
        '19': "$19",
        '20': "$20",
        '21': "$21",
        '22': "$22",
        '23': "$23",
    }
    return switcher.get(str(argument), "nothing")

## Two's complement for 16 bits
def getTwosComp16(argument):
    if (argument[0] == '1'):
        num = int(argument,2)
        val = -32768 +(num - 32768)
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

## Returns the proper memory index of the memory address
def memoryIndex(val,offset1):
    val = val + (offset1)
    index = (val - 8192)/4
    return int (index)

Register = [0 for i in range(24)]
printList = []
