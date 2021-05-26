from collections import *
from typing import BinaryIO


instructions = [ "HALT", "LOAD" , "STORE", "ADD", "SUB", "INC", "DEC", "XOR", "AND", "OR", 
    "NOT", "SHL", "SHR", "NOP", "PUSH", "POP", "CMP", "JMP", "JZ", "JNZ", "JC",
    "JNC", "JA", "JAE", "JB", "JBE", "READ", "PRINT", "JE","JNE"]
registers = ["A", "B", "C", "D", "E", "S", "PC"]
hex_equivalent = {"0": "0000", "1":"0001", "2": "0010", "3": "0011", "4":"0100", "5":"0101", "6":"0110", "7":"0111",
                "8": "1000", "9": "1001", "A":"1010", "B":"1011", "C":"1100", "D":"1101", "E": "1110", "F":"1111"}
labels = {} #stores an integer mapped to labels
hexadecimal = ""
reg_to_hex = {"PC":"0000000000000000", "A": "0000000000000001", "B":"0000000000000010", "C": "0000000000000011", 
            "D":"0000000000000100", "E":"0000000000000101","S":"0000000000000110"}
label_memory = ["JMP","JZ","JNZ","JC","JNC","JA","JAE","JB","JBE","JE","JNE"]


f = open("program.asm", 'tr')
count = 0
for line in f:
    if line[-1:] == "\n":
        line = line[:-1]
    if line[-1:] == ":":
        if labels.get(line[:-1]) is not None:
                print("no multiple occurence of a label is allowed")
        labels[line[:-1]] = count
        count -= 3
    count += 3
f.close()


def my_format(string):
    zero = 6-len(string)
    prepend = "0"*zero
    string = prepend+string
    return string




file = open("program.asm", 'tr')
output = open("program.bin", "wt")
counter = 0

for line in file:
    counter += 1
    if line[-1:] == "\n":
        line = line[:-1]
    tokens = line.split(" ")
    tokens = [i for i in tokens if i != ""]
    A = tokens[0]
    if A not in instructions:
        if A[-1:] != ':': #my program doesn't allow space between label name and ':'
            print("invalid instruction")
            break # I not sure this will behave the way I want it 
    elif counter*3 >255:
        print("the memory available is exceded, program too large")    
    else:
        if A == "JNE":
            code = instructions.index("JNZ") + 1    
        elif A == "JE":
            code = instructions.index("JZ") + 1
        else:
            code = instructions.index(A) + 1
        hexadecimal = "{0:06b}".format(code)
        
        if code == 1 or code == 13:
            hexadecimal += "000000000000000000"
        else:
            if len(tokens) != 2:
                print("not a valid instruction: too many variables")
            B = tokens[1]
            if B in registers: #operand is given in the register
                hexadecimal += "01"
                hexadecimal += reg_to_hex[B]
            elif B[-1] == "]" and B[0] == "[":
                B = B[1:-1]
                if B in registers: #operand is a memory address given in register
                    hexadecimal += "10"
                    hexadecimal += reg_to_hex[B]
                else: #operand is a memory address
                    address = B[1:-1]
                    hexadecimal += "11"
                    hexadecimal += bin(int(address, 16))[2:]
                #this part is fuzzy, write/add after proffessor gives answer
            else: #it is immediate data
                if B[0] == "'" and B[-1] == "'":
                    hexadecimal += "00"
                    if len(B) != 3:
                        print("invalid operand, only caracter allowed")
                    else:
                        ascii_value = ord(B[1:-1])
                        if ascii_value > 255:
                            print("ascii character out of range")
                        hexadecimal += bin(ascii_value)[2:]
                elif labels.get(B) is not None: #if the operand is a label
                    if label_memory.__contains__(A):
                        hexadecimal += "11"
                    else:
                        hexadecimal += "00"
                    hexadecimal += "{0:016b}".format(labels.get(B))
                elif len(B) == 4: #modify this according to proffessors answer
                    hexadecimal += "00"
                    for i in B:
                        if i not in ["A", "B", "C", "D", "E", "F", "0", "1","2","3","4","5","6","7","8","9"]:
                            print("not a valid immediate data: not a hex value")
                        hexadecimal += hex_equivalent.get(i)
        output.write(my_format(hex(int(hexadecimal,2))[2:]).upper()+"\n")