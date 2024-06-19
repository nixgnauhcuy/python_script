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

"""Split a bin file into multiple bin files."""

import sys
import os
import getopt
VERSION = '1.0.0'

USAGE = '''Split a bin file into multiple bin files.

Usage:
    bin_split.exe [options] FILE

Options:
    -h, --help              this help message.
    -v, --version           version info.
    -s, --size=SIZE         size of each output file in bytes. [default: 0xFFFF].
    --symbol=SYMBOL         the symbol between the output filename and the output file sequence number.
    -o, --output=FILENAME   output file name(if option is not specified, default file name is "output").

Arguments:
    FILE                    bin file for spliting.
'''

def is_valid_file(filepath):
    if not os.path.exists(filepath):
        return False
    else:
        return True

def main(args=None):
    import getopt

    split_size = 0xFFFF
    output = "output"
    symbol = ""

    if args is None:
        args = sys.argv[1:]
    try:
        opts, args = getopt.gnu_getopt(args, 'hvs:o:',
                                       ['help', 'version', 'size=', 'symbol=', 'output='])

        for o, a in opts:
            if o in ('-h', '--help'):
                print(USAGE)
                return 0
            elif o in ('-v', '--version'):
                print(VERSION)
                return 0
            elif o in ('-s', '--size'):
                split_size = int(a, 16)
            elif o in ('--symbol'):
                symbol = a
            elif o in ('-o', '--output'):
                output = a
    except getopt.GetoptError:
        e = sys.exc_info()[1]     # current exception
        sys.stderr.write(str(e)+"\n\n")
        sys.stderr.write(USAGE+"\n")
        return 1

    try:
        if is_valid_file(args[0]):
            bin_file = args[0]
            with open(bin_file, 'rb') as input_file:
                input_data = input_file.read()

            file_size = len(input_data)
            num_parts = (file_size + split_size - 1) // split_size
            for i in range(num_parts):
                part_data = input_data[i*split_size:(i+1)*split_size]
                output_filename = f"{output}{symbol}{i+1}.bin"
                if os.path.exists(output_filename):
                    os.remove(output_filename)
                with open(output_filename, 'wb') as output_file:
                    output_file.write(part_data)
    except Exception as e:
        e = sys.exc_info()[1]     # current exception
        sys.stderr.write(str(e)+"\n\n")
        sys.stderr.write(USAGE+"\n")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
