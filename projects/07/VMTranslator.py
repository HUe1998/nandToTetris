"""Use: python3 VMTranslator.py <filename>.vm where file is stored in same
directory as .py file """
import sys
import re

vm_file = sys.argv[1]
vm_name = re.findall('/([^/]+)\.vm', vm_file)[0]

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


def if_else(condn, ind):  # condn(D = x-y)
    condn = condn.upper()
    return f"@{condn}{ind}\nD;J{condn}\n" + f"D=0\n@END{ind}\n0;JMP\n" \
           + f"({condn}{ind})\nD=-1\n" + f"(END{ind})\n"


asm_symbol_dict = {"local": "LCL", "argument": "ARG", "this": "THIS",
                   "that": "THAT"}
this_that_dict = {'0': 'THIS', '1': 'THAT'}

""" pointer => in: Memory Segment, number referred by Memory Segment,
               index of command
               out: asm code where @addr{ind} has value of (segmentPointer + i)
"""


def pointer(segm, num, ind):
    return f"@{segm}\nD=M\n@addr{ind}\nM=D\n" + f"@{num}\nD=A\n" \
           + f"@addr{ind}\nM=D+M\n"


# Code Writer
with open(f"{vm_file[:-3]}.asm", 'w') as asm:
    for index, command_list in enumerate(parsed_list):
        # Comment helps debug output
        asm.write(f"// {' '.join(command_list)}\n")
        # Arithmetic/Logical Implement
        if len(command_list) == 1:
            action = command_list[0]
            if action == 'add':
                asm.write(sp_minus() + sp_pointer_in_d() + sp_minus()
                          + "@SP\nA=M\nD=D+M\n" + d_in_sp_pointer()
                          + sp_plus())
            elif action == 'sub':
                asm.write(sp_minus() + sp_pointer_in_d() + sp_minus()
                          + "@SP\nA=M\nD=M-D\n" + d_in_sp_pointer()
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
                          + "@SP\nA=M\nD=M-D\n" + if_else(action, index)
                          + d_in_sp_pointer() + sp_plus())
        # Memory Segment Implement
        elif len(command_list) == 3:
            action, segment, i = command_list
            if segment in asm_symbol_dict:
                seg = asm_symbol_dict[segment]
                if action == 'push':
                    asm.write(pointer(seg, i, index)
                              + f"@addr{index}\nA=M\nD=M\n"
                              + d_in_sp_pointer() + sp_plus())
                elif action == 'pop':
                    asm.write(pointer(seg, i, index) + sp_minus()
                              + sp_pointer_in_d() + f"@addr{index}\nA=M\nM=D\n"
                              )
            elif segment == 'constant':
                asm.write(f"@{i}\nD=A\n" + d_in_sp_pointer() + sp_plus())
            elif segment == 'static':
                if action == 'push':
                    asm.write(f"@{vm_name}.{i}\nD=M\n" + d_in_sp_pointer()
                              + sp_plus())
                elif action == 'pop':
                    asm.write(sp_minus() + sp_pointer_in_d()
                              + f"@{vm_name}.{i}\nM=D\n")
            elif segment == 'temp':
                if action == 'push':
                    asm.write(f"@{5 + int(i)}\nD=M\n" + d_in_sp_pointer()
                              + sp_plus())
                elif action == 'pop':
                    asm.write(sp_minus() + sp_pointer_in_d()
                              + f"@{5 + int(i)}\nM=D\n")
            elif segment == 'pointer':
                if action == 'push':
                    asm.write(f"@{this_that_dict[i]}\nD=M\n"
                              + d_in_sp_pointer() + sp_plus())
                elif action == 'pop':
                    asm.write(sp_minus() + sp_pointer_in_d()
                              + f"@{this_that_dict[i]}\nM=D\n")
