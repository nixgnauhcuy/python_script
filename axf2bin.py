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

"""Convert .axf file to .bin file."""

import sys
import os
import getopt

VERSION = '1.0.0'

USAGE = '''Convert .axf file to .bin file.

Usage:
    axf2bin.exe [options] FILE

Options:
    -h, --help              this help message.
    -v, --version           version info.
    -o, --output=FILENAME   output file name(if option is not specified, use original name by default).

Arguments:
    FILE                    .axf file.
'''

AXF_HEAD_SIZE = 0x34
BIN_END_MARK = b'\x01\x21\x00\x2F\x0F\x00\x00\x02\x21\x00\x00\x00\x03\x01\x01\x01'

def is_valid_axf_file(filepath):
    if not os.path.exists(filepath) or not filepath.endswith('.axf'):
        return False
    return True

def main(args=None):

    output_file = ""

    if args is None:
        args = sys.argv[1:]
    try:
        opts, args = getopt.gnu_getopt(args, 'hvo:',
                                       ['help', 'version', 'output='])

        for o, a in opts:
            if o in ('-h', '--help'):
                print(USAGE)
                return 0
            elif o in ('-v', '--version'):
                print(VERSION)
                return 0
            elif o in ('-o', '--output'):
                output_file = a
    except getopt.GetoptError:
        e = sys.exc_info()[1]     # current exception
        sys.stderr.write(str(e)+"\n\n")
        sys.stderr.write(USAGE+"\n")
        return 1

    try:
        axf_file = args[0]
        if not is_valid_axf_file(axf_file):
            raise ValueError("Input file is not a valid .axf file.")

        if not output_file:
            output_file = os.path.splitext(axf_file)[0] + '.bin'
        
        if os.path.exists(output_file):
            os.remove(output_file)
        
        with open(axf_file, 'rb') as input_file:
            input_data = input_file.read()

        start_index = AXF_HEAD_SIZE
        end_index = input_data.find(BIN_END_MARK, AXF_HEAD_SIZE)
        if end_index == -1:
            raise ValueError("Convert data failed, can't find BIN_END_MARK.")
        
        output_data = input_data[start_index:end_index]
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
