from collections import *


#carry flag length ile bulunabilir. Normally, the operand is utilized always as 16 bit strings, but it becomes
#17 if there is any carry

class MyCPU:
    PC = 0
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0
    S = 32767 #will decrement with each call
    ZF = 0 #zero flag
    SF = 0 #sign flag
    CF = 0 #carry flag
    memory = [0]*32768 #default values zero




#turns an integer to twos complement form of lenght 16 (if the number 
#excedes 16 bits it returns a binary string of that lenght). return type:string parameter type:int
def int_to_twos_complement(number):
    if number>0:
        binary_number = "{0:016b}".format(int(number), '016b')
        return binary_number
    elif number < 0:
        binary_number = "{0:016b}".format(int(-number))
        binary_number = binary_number.replace("1",'x')
        binary_number = binary_number.replace("0","1")
        binary_number = binary_number.replace('x',"0")
        flipped_binary_number = str(int(binary_number,2) + 1)
        return flipped_binary_number
    else:
        binary_number = "{0:016b}".format(0)


#turns a twos complement represenation to the corresponding integer. return type:int, parameter type:string
def twos_complement_to_int(string):
    if string[:1] == '1':
        string = string.replace("1",'x')
        string = string.replace("0","1")
        string = string.replace('x',"0")
        flipped_binary_number = str(int(string,2) + 1)
        return (-1*flipped_binary_number)
    else:
        return int(string,2)
        


def interprete(line):
    line = line[0:6]
    instruction = str(bin(int(line, 16)))
    operand =instruction[-16:]
    addressing_mode = int(instruction[-18:-16],2)
    opcode = int(instruction[:-18], 2)
    return opcode, addressing_mode,operand
#the stack will be implemented as a part of memory block through utilizing stack pointer
   



file = open("prog.asm", 'tr')
for line in file:
    MyCPU.A = 3
    opcode,addressing_mode, operand = interprete(line)
    if opcode == 1:
        HALT(addressing_mode,operand)
    elif opcode == 2:
        LOAD(addressing_mode,operand)
    elif opcode == 3:
        STORE(addressing_mode,operand)
    elif opcode == 4:
        ADD(addressing_mode,operand)
    elif opcode == 5:
        SUB(addressing_mode,operand)
    elif opcode == 6:
        INC(addressing_mode,operand)
    elif opcode == 7:
        DEC(addressing_mode,operand)
    elif opcode == 8:    
        XOR(addressing_mode,operand)
    elif opcode == 9:    
        AND(addressing_mode,operand)
    elif opcode == 10:
        OR(addressing_mode,operand)
    elif opcode == 11: 
        NOT(addressing_mode,operand)
    elif opcode == 12:
        SHL(addressing_mode,operand)
    elif opcode == 13:
        SHR(addressing_mode,operand)
    elif opcode == 14:
        NOP(addressing_mode,operand)
    elif opcode == 15:    
        PUSH(addressing_mode,operand)
    elif opcode == 16:
        POP(addressing_mode,operand)
    elif opcode == 17:
        CMP(addressing_mode,operand)
    elif opcode == 18:
        JMP(addressing_mode,operand)
    elif opcode == 19: #here there exists a zero flag check
        JZ(addressing_mode,operand)
        JE(addressing_mode,operand)
    elif opcode == 20: #here there exists a zero flag check
        JNZ(addressing_mode,operand)
        JNE(addressing_mode,operand)
    elif opcode == 21:
        JC(addressing_mode,operand)  
    elif opcode == 22:
        JNC(addressing_mode,operand)
    elif opcode == 23:    
        JA(addressing_mode,operand)
    elif opcode == 24:
        JAE(addressing_mode,operand)
    elif opcode == 25:
        JB(addressing_mode,operand) 
    elif opcode == 26:
        JBE(addressing_mode,operand)
    elif opcode == 27:    
        READ(addressing_mode,operand)
    elif opcode == 28:
        PRINT(addressing_mode,operand)
