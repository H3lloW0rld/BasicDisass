from elftools.elf.elffile import ELFFile

import os

print os.getcwd()

with open('uaf32', 'rb') as file:
    e = ELFFile(file)
    print e.get_section_by_name('.symtab').get_symbol_by_name('main')