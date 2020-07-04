import sys
import re

asm_file = sys.argv[1]
asm_name = re.findall('/([^/]+)\.asm', asm_file)[0]
symbol_dict = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
               'SCREEN': 16384, 'KBD': 24576}
for i in range(16):
    symbol_dict.setdefault(f'R{i}', i)

# filter out whitespaces and comments
input_list = []
with open(asm_file, 'r') as asm:
    for line in asm:
        line = re.sub('\n| |//.*', '', line)
        if line != '':
            input_list.append(line)

# add labels to symbol dictionary
y = 0
for index, item in enumerate(input_list):
    label = item[1:-1]
    if item[0] == '(' and label not in symbol_dict:
        symbol_dict[label] = index - y
        y += 1

# add vars to symbol dict and remove labels
instruction_list = []
free_memory = 16
for item in input_list:
    first_char = item[0]
    var = item[1:]
    if first_char == '@' and (not var.isnumeric()) and var not in symbol_dict:
        symbol_dict[var] = free_memory
        free_memory += 1
        instruction_list.append(item)
    elif first_char != '(':
        instruction_list.append(item)

comp_dict = {'0': '101010', '1': '111111', '-1': '111010', 'D': '001100',
             'A': '110000', '!D': '001101', '!A': '110001', '-D': '001111',
             '-A': '110011', 'D+1': '011111', 'A+1': '110111', 'D-1': '001110',
             'A-1': '110010', 'D+A': '000010', 'D-A': '010011',
             'A-D': '000111', 'D&A': '000000', 'D|A': '010101'}

jump_dict = {'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100',
             'JNE': '101', 'JLE': '110', 'JMP': '111'}


# return (a, c-binary) tuple
def comp_to_binary(comp):
    a = 0
    if 'M' in comp:
        a = 1
    comp = comp.replace('M', 'A')
    return a, comp_dict[comp]


def dest_to_binary(dest):
    ans = ['0', '0', '0']
    if 'A' in dest:
        ans[0] = '1'
    if 'D' in dest:
        ans[1] = '1'
    if 'M' in dest:
        ans[2] = '1'
    return ''.join(ans)


def jump_to_binary(jump):
    return jump_dict[jump]


# Main Loop
with open(f'{asm_name}.hack', 'w') as hack:
    for instruction in instruction_list:
        if instruction[0] == '@':  # A-instruction
            variable = instruction[1:]
            if variable.isnumeric():
                hack.write(f'{int(variable):016b}\n')
            else:
                hack.write(f'{symbol_dict[variable]:016b}\n')
        else:  # C-instruction
            c_list = (instruction.replace('=', ';')).split(';')
            if len(c_list) == 3:
                dest = c_list[0]
                comp = c_list[1]
                jump = c_list[2]
                a, c = comp_to_binary(comp)
                d = dest_to_binary(dest)
                j = jump_to_binary(jump)
                hack.write(f'111{a}{c}{d}{j}\n')
            elif '=' in instruction:
                c_list = instruction.split('=')
                dest = c_list[0]
                comp = c_list[1]
                a, c = comp_to_binary(comp)
                d = dest_to_binary(dest)
                hack.write(f'111{a}{c}{d}000\n')
            else:
                c_list = instruction.split(';')
                comp = c_list[0]
                jump = c_list[1]
                a, c = comp_to_binary(comp)
                j = jump_to_binary(jump)
                hack.write(f'111{a}{c}000{j}\n')
