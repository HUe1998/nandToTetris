"""Use: python3 VMTranslator.py <filename>.vm where file is stored in same
directory as .py file """
import sys
import re

vm_file = sys.argv[1]
vm_name = vm_file[:-3]

# Parser
parsed_list = []  # List of Lists containing commands broken in lexical
with open(vm_file, 'r') as vm:
    for line in vm:
        line = re.sub('\n|//.*', '', line)
        if line != '':
            parsed_list.append(line.split())


# Common functions
def sp_plus():  # SP++
    return "@SP\nM=M+1\n"


def sp_minus():  # SP--
    return "@SP\nM=M-1\n"


def d_in_sp_pointer():  # *SP = D
    return "@SP\nA=M\nM=D\n"


def sp_pointer_in_d():  # D = *SP
    return "@SP\nA=M\nD=M\n"


def if_else(condn, index):  # condn(D = x-y)
    condn = condn.upper()
    return f"@{condn}{index}\nD;J{condn}\n" + f"D=0\n@END{index}\n0;JMP\n" \
           + f"({condn}{index})\nD=-1\n" + f"(END{index})\n"


# Code Writer
with open(f"{vm_name}.asm", 'w') as asm:
    for index, command_list in enumerate(parsed_list):
        print(f"// {' '.join(command_list)}")  # Comment helps debug output
        # Arithmetic/Logical Implement
        if len(command_list) == 1:
            action = command_list[0]
            if action == 'add':
                asm.write(sp_minus() + sp_pointer_in_d() + sp_minus()
                          + "@SP\nA=M\nD=D+M\n" + d_in_sp_pointer()
                          + sp_plus())
            elif action == 'sub':
                asm.write(sp_minus() + sp_pointer_in_d() + sp_minus()
                          + "@SP\nA=M\nD=D-M\n" + d_in_sp_pointer()
                          + sp_plus())
            elif action == 'neg':
                asm.write(sp_minus() + sp_pointer_in_d() + "D=-D\n"
                          + d_in_sp_pointer() + sp_plus())
            elif action == 'and':
                asm.write(sp_minus() + sp_pointer_in_d() + sp_minus()
                          + "@SP\nA=M\nD=D&M\n" + d_in_sp_pointer()
                          + sp_plus())
            elif action == 'or':
                asm.write(sp_minus() + sp_pointer_in_d() + sp_minus()
                          + "@SP\nA=M\nD=D|M\n" + d_in_sp_pointer()
                          + sp_plus())
            elif action == 'not':
                asm.write(sp_minus() + sp_pointer_in_d() + "D=!D\n"
                          + d_in_sp_pointer() + sp_plus())
            else:
                asm.write(sp_minus() + sp_pointer_in_d() + sp_minus()
                          + "@SP\nA=M\nD=D-M\n" + if_else(action, index)
                          + d_in_sp_pointer() + sp_plus())
        # Memory Segment Implement
        else:
            pass