from elftools.elf.elffile import ELFFile

with open('uaf32', 'rb') as file:
    e = ELFFile(file)
    header = e.header
    print header