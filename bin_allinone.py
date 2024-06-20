#!/usr/bin/env python

# Copyright (c) 2023 nixgnauhcuy
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

"""Merge several bin files into one bin file."""

import sys
import os
import getopt

VERSION = '1.0.2'

USAGE = '''
Merge several bin files into one bin file.

Usage:
    bin_allinone.exe [options] FILES...

Options:
    -h, --help              this help message.
    -v, --version           version info.
    -p, --padding           padding bytes, default 0xff.
    -o, --output=FILENAME   output file name(if option is not 
                            specified, default output.bin).

Arguments:
    FILES                   list of bin files for merging.

Example:
    bin_allinone.exe -p 0x00 input1.bin 0x100 input2.bin 0x200 input3.bin 0x300
    bin_allinone.exe -o output.bin input1.bin 0x100 input2.bin 0x200 input3.bin 0x300
    bin_allinone.exe input1.bin 0x100 input2.bin 0x200 input3.bin 0x300 -p 0xff -o output.bin
'''

def is_valid_bin_file(filepath):
    if not os.path.exists(filepath) or not filepath.endswith('.bin'):
        return False
    else:
        return True

def is_valid_address(arg):
    try:
        address = int(arg, 16)
        if address < 0 or address > 0xFFFFFFFF:
            raise ValueError
        return True
    except ValueError:
        return False


def main(args=None):
    output = "output.bin"
    paddingbyte = 0xff

    if args is None:
        args = sys.argv[1:]
    try:
        opts, args = getopt.gnu_getopt(args, 'hvp:o:',
                                       ['help', 'version', 'padding=', 'output='])

        for o, a in opts:
            if o in ('-h', '--help'):
                print(USAGE)
                return 0
            elif o in ('-v', '--version'):
                print(VERSION)
                return 0
            elif o in ('-p', '--padding'):
                paddingbyte = int(a, 16)
            elif o in ('-o', '--output'):
                output = a

        if len(args) % 2 != 0:
            raise getopt.GetoptError('Error: You should check file list!')

    except getopt.GetoptError:
        e = sys.exc_info()[1]     # current exception
        sys.stderr.write(str(e)+"\n\n")
        sys.stderr.write(USAGE+"\n")
        return 1
    
    bin_files = {}
    for i in range(0, len(args), 2):
        try:
            if is_valid_bin_file(args[i]) and is_valid_address(args[i+1]):
                bin_file = args[i] 
                bin_file_addr = args[i + 1][2:] if args[i + 1].startswith("0x") else args[i + 1]
                bin_files[bin_file] = bin_file_addr
            else:
                raise ValueError("Input file is not a valid .bin file.")
        except Exception as e:
            e = sys.exc_info()[1]     # current exception
            sys.stderr.write(str(e)+"\n\n")
            sys.stderr.write(USAGE+"\n")
            return 1
        
    sort_bin_files = dict(sorted(bin_files.items(), key=lambda item: int(item[1], 16)))
    output_size = int(sort_bin_files.get(list(sort_bin_files.keys())[-1]), 16) + os.path.getsize(list(sort_bin_files.keys())[-1])

    if os.path.exists(output):
        os.remove(output)

    with open(output, 'wb') as output_file:
        output_data = bytearray([paddingbyte] * output_size)

        for file in sort_bin_files:
            file_offset = int(sort_bin_files[file], 16)
            
            with open(file, 'rb') as input_file:
                input_data = input_file.read()
            output_data[file_offset : file_offset+len(input_data)] = input_data

        output_file.write(output_data)
    return 0

if __name__ == '__main__':
    sys.exit(main())
