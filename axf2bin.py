#!/usr/bin/env python

# Copyright (c) 2024 nixgnauhcuy
# All rights reserved.
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided
# that the following conditions are met:
#
# * Redistributions of source code must retain
#   the above copyright notice, this list of conditions
#   and the following disclaimer.
# * Redistributions in binary form must reproduce
#   the above copyright notice, this list of conditions
#   and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the author nor the names
#   of its contributors may be used to endorse
#   or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Convert .axf file to .bin file."""

import sys
import os
import getopt
import struct

VERSION = '1.0.2'

USAGE = '''Convert .axf file to .bin file.

Usage:
    axf2bin.exe [options] FILE

Options:
    -h, --help              this help message.
    -v, --version           version info.
        --header            output axf file header information.
        --program-headers   output program headers information.
    -o, --output=FILENAME   output file name(if option is not specified, use original name by default).

Arguments:
    FILE                    .axf file.
'''

class Elf_Struct(object):

    E_IDENT_MAG0 = 0
    E_IDENT_MAG1 = 1
    E_IDENT_MAG2 = 2
    E_IDENT_MAG3 = 3
    E_IDENT_CLASS = 4
    E_IDENT_DATA = 5
    E_IDENT_VERSION = 6
    E_IDENT_OSABI = 7
    E_IDENT_ABIVERSION = 8
    E_IDENT_PAD = 9
    E_IDENT_NIDENT = 16

    E_CLASS_32BIT = 0x01
    E_CLASS_64BIT = 0x02

    E_DATA_LSB = 0x01
    E_DATA_MSB = 0x02

    # @see https://docs.oracle.com/cd/E19683-01/816-1386/chapter6-43405/index.html
    def __init__(self, data) -> None:

        self.e_ident = data[:self.E_IDENT_NIDENT]

        # ELF Header:
        unpack_fmt = '<HHIIIIIHHHHHH' if self.e_ident[self.E_IDENT_CLASS] == self.E_CLASS_32BIT else '<HHIQQQIHHHHHH'
        (
            self.e_type, 
            self.e_machine, 
            self.e_version, 
            self.e_entry, 
            self.e_phoff, 
            self.e_shoff, 
            self.e_flags, 
            self.e_ehsize, 
            self.e_phentsize, 
            self.e_phnum, 
            self.e_shentsize, 
            self.e_shnum, 
            self.e_shstrndx 
        ) = struct.unpack(unpack_fmt, data[self.E_IDENT_NIDENT:self.E_IDENT_NIDENT+struct.calcsize(unpack_fmt)])

        # ELF Program Headers:
        if self.e_ident[self.E_IDENT_CLASS] == self.E_CLASS_32BIT:
            unpack_fmt = '<IIIIIIII'
            (
                self.p_type,
                self.p_offset,
                self.p_vaddr,
                self.p_paddr,
                self.p_filesz,
                self.p_memsz,
                self.p_flags,
                self.p_align
            ) = struct.unpack(unpack_fmt, data[self.e_phoff:self.e_phoff+struct.calcsize(unpack_fmt)])
        else:
            unpack_fmt = '<IIQQQQQQ'
            (
                self.p_type,
                self.p_flags,
                self.p_offset,
                self.p_vaddr,
                self.p_paddr,
                self.p_filesz,
                self.p_memsz,
                self.p_align
            ) = struct.unpack(unpack_fmt, data[self.e_phoff:self.e_phoff+struct.calcsize(unpack_fmt)])
    
    def Elf_Header_Print(self):
        print("ELF Header:")
        print("Magic:                                 ", " ".join(f"{byte:02x}" for byte in self.e_ident))
        print("Class:                                 ", "ELF32" if self.e_ident[self.E_IDENT_CLASS] == 1 else "ELF64")
        print("Data Encoding:                         ", "Specifies 2's complement values, " + ("ELFDATA2LSB" if self.e_ident[self.E_IDENT_DATA] == 1 else "ELFDATA2MSB"))
        print("Machine:                               ", self.e_machine)
        print("Version:                               ", hex(self.e_version))
        print("Entry point address:                   ", hex(self.e_entry))
        print("Program header table's file offset:    ", self.e_phoff, " (bytes into file)")
        print("Section header table's file offset:    ", self.e_shoff, " (bytes into file)")
        print("Flags:                                 ", hex(self.e_flags))
        print("Header size:                           ", self.e_ehsize, " (bytes)")
        print("Program header table size:             ", self.e_phentsize, " (bytes)")
        print("Number of program header entries:      ", self.e_phnum)
        print("Section header's size :                ", self.e_shentsize, " (bytes)")
        print("Number of section header entries:      ", self.e_shnum)
        print("Section header table index:            ", self.e_shstrndx)
    
    def Elf_Program_Header_Print(self):
        print("Program Header:")
        print("Type:                                   ", self.p_type)
        print("Flags:                                  ", hex(self.p_flags))
        print("Offset from the beginning of the file:  ", hex(self.p_offset))
        print("Virtual address:                        ", hex(self.p_vaddr))
        print("Segment's physical address:             ", hex(self.p_paddr))
        print("Number of bytes in the file image:      ", hex(self.p_filesz))
        print("Number of bytes in the memory image:    ", hex(self.p_memsz))
        print("Alignment:                              ", hex(self.p_align))

def is_valid_axf_file(filepath):
    if not os.path.exists(filepath) or not filepath.endswith('.axf'):
        return False
    return True

def main(args=None):

    output_file = ""
    print_header_flag = False
    print_program_headers_flag = False

    if args is None:
        args = sys.argv[1:]
    try:
        opts, args = getopt.gnu_getopt(args, 'hvo:',
                                       ['help', 'version', 'header', 'program-headers', 'output='])

        for o, a in opts:
            if o in ('-h', '--help'):
                print(USAGE)
                return 0
            elif o in ('-v', '--version'):
                print(VERSION)
                return 0
            elif o in ('--header'):
                print_header_flag = True
            elif o in ('--program-headers'):
                print_program_headers_flag = True
            elif o in ('-o', '--output'):
                output_file = a

        axf_file = args[0]
        if not is_valid_axf_file(axf_file):
            raise ValueError("Input file is not a valid .axf file.")
        
        with open(axf_file, 'rb') as input_file:
            input_data = input_file.read()
        
        elf_object = Elf_Struct(input_data)

        if print_header_flag:
            elf_object.Elf_Header_Print()
            return 0

        if print_program_headers_flag:
            elf_object.Elf_Program_Header_Print()
            return 0

        if not output_file:
            output_file = os.path.splitext(axf_file)[0] + '.bin'
        
        if os.path.exists(output_file):
            os.remove(output_file)
        
        output_data = input_data[elf_object.e_ehsize:elf_object.p_filesz+elf_object.e_ehsize]
        with open(output_file, 'wb') as output:
            output.write(output_data)
    except Exception as e:
        e = sys.exc_info()[1]     # current exception
        sys.stderr.write(str(e)+"\n\n")
        sys.stderr.write(USAGE+"\n")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
