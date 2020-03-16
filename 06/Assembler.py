import re
import os
import sys

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}

for i in range(0, 16):
    label = "R" + str(i)
    table[label] = i


variableCursor = 16
root = sys.argv[1]

# Remove whitespace & comments.


def strip(line):
    char = line[0]
    if char == "\n" or char == "/":
        return ""
    elif char == " ":
        return strip(line[1:])
    else:
        return char + strip(line[1:])

# Normalize instructions & jump fields.


def normalize(line):
    line = line[:-1]
    if not "=" in line:
        line = "null=" + line
    if not ";" in line:
        line = line + ";null"
    return line

# Memory allocation for new variables.


def addVariable(label):
    global variableCursor
    table[label] = variableCursor
    variableCursor += 1
    return table[label]


def aTranslate(line):
    if line[1].isalpha():
        label = line[1:-1]
        aValue = table.get(label, -1)
        if aValue == -1:
            aValue = addVariable(label)
    else:
        aValue = int(line[1:])
    bValue = bin(aValue)[2:].zfill(16)
    return bValue


def cTranslate(line):
    line = normalize(line)
    temp = line.split("=")
    destCode = dest.get(temp[0], "destFAIL")
    temp = temp[1].split(";")
    compCode = comp.get(temp[0], "compFAIL")
    jumpCode = jump.get(temp[1], "jumpFAIL")
    return compCode, destCode, jumpCode

# Separates A & C instructions.


def translate(line):
    if line[0] == "@":
        return aTranslate(line)
    else:
        codes = cTranslate(line)
        return "111" + codes[0] + codes[1] + codes[2]


def firstPass():
    infile = open(root + ".asm")
    outfile = open(root + ".tmp", "w")

    lineNumber = 0
    for line in infile:
        sline = strip(line)
        if sline != "":
            if sline[0] == "(":
                label = sline[1:-1]
                table[label] = lineNumber
                sline = ""
            else:
                lineNumber += 1
                outfile.write(sline + "\n")

    infile.close()
    outfile.close()


def assemble():
    infile = open(root + ".tmp")
    outfile = open(root + ".hack", "w")

    for line in infile:
        tline = translate(line)
        outfile.write(tline + "\n")

    infile.close()
    outfile.close()
    os.remove(root + ".tmp")


firstPass()
assemble()

