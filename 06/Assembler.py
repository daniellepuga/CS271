import re, os, sys

class Assembler:

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

    def __init__(self, file):
        self.file=file

    def read_and_remove_whitespace(self, file):
        file1 = open("myfile.txt", "r") 
        count = 0
        line = re.sub(r"\s+", "", line)
        print("Using for loop") 
        for line in file1: 
            count += 1
            print("Line{}: {}".format(count, line.strip())) 

    def main(file_name):
        file=Assembler(file_name)
        file.read(file_name)
        file.remove_white_space(file_name)

if __name__=="__main__":
    main("add/Add.asm")