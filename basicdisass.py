# Author: Nguyen Trung Khanh - 15520359

import sys
import os
import re

from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from elftools.elf.sections import SymbolTableSection
from capstone import *

COMMAND_LIST = [
    r"^(disass) ([\w\d_]+)$", # disassemble a function
    r"(quit)", # exit
]

def printHelp():
    print "basicdisass.py FILE"

def get_parameter(command):
    for pattern in COMMAND_LIST:
        m = re.match(pattern, command)
        if (m is not None):
            return m.groups()
    return None

def handle(filePath):
    file = open(filePath, "rb")
    try:
        elf = ELFFile(file)
        arch = elf.get_machine_arch()
        
        # determine architecture
        if arch == 'x86':
            cs_arch = CS_ARCH_X86
            cs_mode = CS_MODE_32
        elif arch == 'x64':
            cs_arch = CS_ARCH_X86
            cs_mode = CS_MODE_64
        elif arch == 'ARM':
            cs_arch = CS_ARCH_ARM
            cs_mode = CS_MODE_ARM
        elif arch == 'AArch64':
            cs_arch = CS_ARCH_ARM64
            cs_mode = CS_MODE_ARM
        else:
            sys.stderr.write("Don't support ELF format machine\n")
            file.close()
            sys.exit(1)

        # get .text section
        code_section = elf.get_section_by_name('.text')
        # get .text section's data
        code = code_section.data()
        # get .text section virtual address
        addr = code_section['sh_addr']
        # get symbol table from .symtab section or .dynsym section
        symbol_tables = [s for s in elf.iter_sections() if isinstance(s, SymbolTableSection)]
    except ELFError as ex:
        sys.stderr.write("ELF error: %s\n" % ex)
        file.close()
        sys.exit(1)

    # initialize Capstone engine
    md = Cs(cs_arch, cs_mode)

    while True:
        flag = False
        command = raw_input(">> ")
        param = get_parameter(command)

        if (param is None):
            print "Invalid command!"
        elif (param[0] == "disass"):
            # disassemble function
            for section in symbol_tables:
                for s in section.iter_symbols():
                    # find the given symbol in symbol table
                    if s.name == param[1]:
                        flag = True
                        symbol = s
                        break
                if flag:
                    break
            if flag:
                sp = symbol['st_value'] - addr
                for (address, size, mnemonic, op_str) in md.disasm_lite(code[sp: sp + symbol['st_size'] + 1], symbol['st_value']):
                    print("0x%x:\t%s\t%s" % (address, mnemonic, op_str))
            else:
                print "Can't not find symbol!"
        elif (param[0] == "quit"):
            break

    file.close()
    

def main():
    if len(sys.argv) == 2:
        if (os.path.isfile(sys.argv[1])):
            handle(sys.argv[1])
        else:
            print "File doesn't exist!"
    else:
        printHelp()


main()