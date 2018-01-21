import sys
import os
import re

from pylibelf import pylibelf as libelf
from pylibelf import elfconstants, elfutils

COMMAND_LIST = [
    r"^(disass) ([\w\d_]+)$" # disassemble a function
]

def getSymbolTable(elf):
    symtabSection = elf.getSectionByName(elfconstants.ELF_SECTION_TYPES['SHT_SYMTAB'])
    return libelf.Elf_SymbolTable.parse(elfutils.ReadData(symtabSection.sectionRawData), elf.getType().value)

def printHelp():
    print "-h hihi"

def getParameter(command):
    for pattern in COMMAND_LIST:
        m = re.match(command, pattern)
        if (m is not None):
            return m.groups()
    return None

def handle(filePath):
    elf = libelf.ELF(filePath)
    arch = elf.elfHdr.e_machine
    
    if (arch == elfconstants.ELF_MACHINE_TYPES[])
    print "Welcome to BasicDisass, please type 'help' to get more information!"

    while True:
        command = raw_input(">> ")

def main():
    if len(sys.argv) == 2:
        if (os.path.isfile(sys.argv[1])):
            handle(sys.argv[1])
        else:
            print "File doesn't exist!"
    else:
        printHelp()