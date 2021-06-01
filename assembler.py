import os
import sys
import re
from collections import *
from typing import BinaryIO

flag = True
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


f = open(sys.argv[1], 'tr')
count = 0
for line in f:
    if line[-1:] == "\n":
        line = line[:-1]
    found = re.search(r"\S+.\S+", line)
    if found:
        line = found.group(0)
    else:
        continue
    if line[-1:] == ":":
        if labels.get(line[:-1]) is not None:
                print("no multiple occurence of a label is allowed")
                flag = False
        labels[line[:-1]] = count
        count -= 3
    count += 3
f.close()


def my_format(string):
    zero = 6-len(string)
    prepend = "0"*zero
    string = prepend+string
    return string




file = open(sys.argv[1], 'tr')
output = open("program.bin", "wt")
counter = 0

for line in file:
    
    line = line.strip()
    counter += 1
    if len(line) == 0:
        continue
    tokens = re.findall('\S+', line)
    A = tokens[0]
    if A=="NOP":
        output.write("380000\n")
        continue
    if A not in instructions:
        if A[-1:] != ':': #my program doesn't allow space between label name and ':'
            print("invalid instruction")
            flag = False

            break # I not sure this will behave the way I want it 
    elif counter*3 >2545656:
        print("the memory available is exceded, program too large")    
        flag = False
    else:
        if A == "JNE":
            code = instructions.index("JNZ") + 1    
        elif (A == "JE"):
            code = instructions.index("JZ") + 1
        else:
            code = instructions.index(A) + 1
        hexadecimal = "{0:06b}".format(code)
        
        if code == 1 or code == 14:
            hexadecimal += "000000000000000000"
        else:
            if (len(tokens) != 2):
                print("not a valid instruction: too many variables")
                print(A)
                print(tokens[1])
                flag = False
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
                    hexadecimal += "11"
                    hexadecimal += "{0:016b}".format(int(B,16))
                
                #this part is fuzzy, write/add after proffessor gives answer
            else: #it is immediate data
                if B[0] == "'" and B[-1] == "'":
                    hexadecimal += "00" 
                    if len(B) != 3:
                        print("invalid operand, only caracter allowed")
                        flag = False
                    else:
                        ascii_value = ord(B[1:-1])
                        if ascii_value > 255:
                            print("ascii character out of range")
                            flag = False
                        hexadecimal += "{0:016b}".format(ascii_value)
                    
                elif labels.get(B) is not None: #if the operand is a label
                    
                    hexadecimal += "00"
                    hexadecimal += "{0:016b}".format(labels.get(B))
                elif (len(B) < 6) & (len(B)>0): #modify this according to proffessors answer
                    hexadecimal += "00"
                    for i in B:
                        if i not in ["A", "B", "C", "D", "E", "F", "0", "1","2","3","4","5","6","7","8","9"]:
                            print("not a valid immediate data: not a hex value")
                            flag = False
                        hexadecimal += hex_equivalent.get(i)
        output.write(my_format(hex(int(hexadecimal,2))[2:]).upper()+"\n")
        
        if not(flag):
            os.remove("program.bin")
            break
