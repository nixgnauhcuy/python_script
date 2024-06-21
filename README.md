# python_script

Package some personal Python scripts into an executable file for use.

# Quick Start

Download the latest release from [Releases](https://github.com/nixgnauhcuy/python_script/releases).

# script list

## bin_allinone

The script is used to merge multiple bin files into one bin file.

**Usage**

``` shell
bin_allinone.exe [options] FILES...
```

**Options**

```
    -h, --help              this help message.
    -v, --version           version info.
    -p, --padding           padding bytes, default 0xff.
    -o, --output=FILENAME   output file name(if option is not 
                            specified, dafault output.bin)
```

**Arguments**

```
    FILES                   list of bin files for merging
```

**Example Usage**

``` shell
bin_allinone.exe -p 0x00 input1.bin 0x100 input2.bin 0x200 input3.bin 0x300
bin_allinone.exe -o output.bin input1.bin 0x100 input2.bin 0x200 input3.bin 0x300
bin_allinone.exe input1.bin 0x100 input2.bin 0x200 input3.bin 0x300 -p 0xff -o output.bin
```

## bin_split

The script is Split a bin file into multiple bin files.

**Usage**

``` shell
bin_split.exe [options] FILE
```

**Options**

```
    -h, --help              this help message.
    -v, --version           version info.
    -s, --size=SIZE         size of each output file in bytes. [default: 0xFFFF].
    --symbol=SYMBOL         the symbol between the output filename and the output file sequence number.
    -o, --output=FILENAME   output file name(if option is not specified, default file name is "output").
```

**Arguments**

```
    FILE                    bin file for spliting.
```

**Example Usage**

``` shell
bin_split.exe test.bin
bin_split.exe -s 0x1000 test.bin
bin_split.exe -s 0x1000 -o output test.bin
bin_split.exe -s 0x1000 --symbol=_ -o output test.bin
```

## axf2bin

The script is used to convert .axf file to .bin file.

**Usage**

``` shell
axf2bin.exe [options] FILE
```

**Options**

```
    -h, --help              this help message.
    -v, --version           version info.
        --header            output axf file header information.
        --program-headers   output program headers information.
    -o, --output=FILENAME   output file name(if option is not specified, use original name by default).
```

**Arguments**

```
    FILES                   .axf file.
```

**Example Usage**

``` shell
axf2bin.exe input.axf
axf2bin.exe --header input.axf
axf2bin.exe --program-headers input.axf
axf2bin.exe -o output.bin input.axf
```

# Contribution

If you encounter any issues or have suggestions for improvements, please feel free to raise an issue or submit a pull request. Your contributions are highly valued!

# License

This project is licensed under the MIT License.