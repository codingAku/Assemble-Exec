from collections import *
from typing import BinaryIO
#lets open a global boolean that holds if there is any runtime error or syntax error

#carry flag length ile bulunabilir. Normally, the operand is utilized always as 16 bit strings, but it becomes
#17 if there is any carry

class MyCPU:
    registers = [0,0,0,0,0,0]
    S = 65535 #will decrement with each call
    ZF = 0 #zero flag
    SF = 0 #sign flag
    CF = 0 #carry flag
    memory = ['00000000'] * 64 * 1024 #default values zero
    f = open("prog.asm", 'tw')


def int_to_twos_complement(number):
    if number>0:
        binary_number = "{0:016b}".format(int(number), '016b')
        return binary_number
    elif number < 0:
        binary_number = "{0:016b}".format(int(-number))
        binary_number = binary_number.replace("1",'x')
        binary_number = binary_number.replace("0","1")
        binary_number = binary_number.replace('x',"0")
        flipped_binary_number = "{0:016b}".format(int(int(binary_number,2) + 1))
        return flipped_binary_number
    else:
        binary_number = "{0:016b}".format(number)



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
        



#not sure if a whole string, not just a character will be able to get printed
def PRINT(addressing_mode, operand):
    num = ""
    if addressing_mode == 0: #immediate addressing
        num = twos_complement_to_int(operand)

    elif addressing_mode == 1 or addressing_mode == 2: #operand in register
        reg = twos_complement_to_int(operand)
        if reg > 6 or reg < 0:
            print("invalid register")
        
        num = twos_complement_to_int(MyCPU.registers[reg])

        if addressing_mode == 2: #memory adress in register
            num = twos_complement_to_int(MyCPU.memory[num] + MyCPU.memory[num+1])
    
    elif addressing_mode == 3: #operand is memory address
        index = twos_complement_to_int(operand)
        temp = MyCPU.memory[index] + MyCPU.memory[index+1]
        num = twos_complement_to_int(temp)
    else:
        print('invalid addressing mode')
        return
    
    MyCPU.f.write(chr(num))



def READ(addressing_mode, operand):
    string = input()
    if len(string) > 1:
        print('input error: a character expected, found a string')
    elif addressing_mode == 0:
        print('read error: reading cannot be stured as immediate data')
    elif addressing_mode == 1:
        s = ord(string)
        binary = int_to_twos_complement(s)
        reg = twos_complement_to_int(operand)
        if reg < 0 or reg > 6:
            print("invalid register")
        else:
            MyCPU.registers[reg] = binary


def JB(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JB instruction')
       return
    
    if MyCPU.CF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3 #goes to the specified instruction

def JBE(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JBE instruction')
        return
    
    if MyCPU.CF == 1 or MyCPU.ZF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3

def JAE(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JAE instruction')
        return
    
    if MyCPU.CF == 0:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3

def JA(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JA instruction')
        return
    
    if MyCPU.CF == 0 or MyCPU.ZF == 0:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3

def JNC(addressing_mode, operand):
    if addressing_mode != 0:
        print('wrong addressing mode: JNC instruction')
        return
    
    if MyCPU.CF == 0:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3


def JC(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JC instruction')
       return
    
    if MyCPU.CF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3

def JNZ(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JNZ instruction')
       return
    
    if MyCPU.ZF == 0:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3


def JNE(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JNE instruction')
       return
    
    if MyCPU.ZF == 0:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3

def JZ(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JC instruction')
       return
    
    if MyCPU.ZF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3
    
def JE(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JC instruction')
       return
    
    if MyCPU.ZF == 1:
        memory = twos_complement_to_int(operand)
        MyCPU.registers[0] = memory/3

def JMP(addressing_mode, operand):
    if addressing_mode != 0:
       print('wrong addressing mode: JMP instruction')
       return
    
    memory = twos_complement_to_int(operand)
    MyCPU.registers[0] = memory/3

def CMP(addressing_mode, operand):
    subtract = ""
    if operand == 0:
        subtract = operand
    elif operand == 1: #operand in register
        reg = twos_complement_to_int(operand)
        subtract = MyCPU.registers[reg]
    elif operand == 2: #memory address given in register
        reg = twos_complement_to_int(operand)
        regad = MyCPU.registers[reg]
        index = twos_complement_to_int(regad)
        subtract = MyCPU.memory[index]+MyCPU.memory[index+1]
    elif operand == 3: #is memory address
        index = twos_complement_to_int(operand)
        subtract = MyCPU.memory[index] + MyCPU.memory[index+1]

    SUB(A, subtract)


def POP(addressing_mode, operand):
    if addressing_mode != 1:
        print('wrong addressing mode: POP instruction')
        return
    if(MyCPU.S == 0):
        print('invalid operation, stack empty: POP instruction')
    data = MyCPU.memory[MyCPU.S]+MyCPU.memory[MyCPU.S+1]
    MyCPU.S += 2
    reg = twos_complement_to_int(operand)
    MyCPU.registers[reg] = data


def PUSH(addressing_mode, operand):
    reg = twos_complement_to_int(operand)
    if reg < 0 or reg > 6:
        print('invalid register: PUSH instruction')
    high = MyCPU.registers[reg][0:9]
    low = MyCPU.registers[reg][9:]
    MyCPU.memory[MyCPU.S] = low
    MyCPU.memory[MyCPU.S-1] = high
    MyCPU.memory -= 2

def NOP(addressing_mode, operand):
    return

def SHR(addressing_mode, operand):
    if addressing_mode != 1:
        print('invalid addressing mode: SHR instruction')
    reg = twos_complement_to_int(operand)
    if reg < 0 or reg > 6:
        print('invalid register: SHR instruction')
    data = MyCPU.registers[reg]
    value = int(data, 2) >> 1
    data = int_to_twos_complement(value)
    if data[15] == "1":
        MyCPU.SF = 1
    else:
        MyCPU.SF = 0

    if value == 0:
        MyCPU.ZF = 1
    else:
        MyCPU.ZF = 0

    MyCPU.registers[reg] = data


def SHL(addressimg_mode, operand): #I really am not sure about the flags here are set true, especially sign flag
    if addressing_mode != 1:
        print('invalid addressing mode: SHR instruction')
    reg = twos_complement_to_int(operand)
    if reg < 0 or reg > 6:
        print('invalid register: SHR instruction')
    data = MyCPU.registers[reg]
    value = int(data, 2) << 1
    data = int_to_twos_complement(value)
    if len(data) == 17:
        MyCPU.CF = 1
    
    if data[15] == "1":
        MyCPU.SF = 1
    else:
        MyCPU.SF = 0

    if value == 0:
        MyCPU.ZF = 1
    else:
        MyCPU.ZF = 0

    MyCPU.registers[reg] = data







#turns an integer to twos complement form of lenght 16 (if the number 
#excedes 16 bits it returns a binary string of that lenght). return type:string parameter type:int


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
    

    if opcode<1 or opcode >28 or addressing_mode < 0 or  addressing_mode > 3:
        print('undefined instruction error')
    elif opcode == 1:
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
