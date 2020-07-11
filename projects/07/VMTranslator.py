"""Use: python3 VMTranslator.py <filename>.vm where file is stored in same
directory as .py file """
import sys
import re

vm_file = sys.argv[1]
vm_name = vm_file[:-3]

# Parser
parsed_list = []        # List of Lists containing commands broken in lexical
with open(vm_file, 'r') as vm:
    for line in vm:
        line = re.sub('\n|//.*', '', line)
        if line != '':
            parsed_list.append(line.split())


# Code Writer
with open(f"{vm_name}.asm", 'w') as asm:
    for command_list in parsed_list:
        print(f"// {' '.join(command_list)}") # Comment helps debug output
        # Arithmetic/Logical Implement
        if len(command_list) == 1:
            action = command_list[0]
