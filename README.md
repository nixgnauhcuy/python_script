# python_script

Save some personal Python scripts for personal use.

# script list

## bin_allinone.py

The script is used to merge multiple bin files into one bin file.

**Usage**

``` shell
python bin_allinone.py [options] FILES...
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
    FILES       list of bin files for merging
```

**Example Usage**

``` shell
python bin_allinone.py file1.bin addr1 file2.bin addr2 file3.bin addr3
python bin_allinone.py file1.bin addr1 file2.bin addr2 file3.bin addr3 -o out.bin
python bin_allinone.py file1.bin addr1 file2.bin addr2 file3.bin addr3 -p 0xff -o out.bin
```

# Contribution

If you encounter any issues or have suggestions for improvements, please feel free to raise an issue or submit a pull request. Your contributions are highly valued!

# License

This project is licensed under the MIT License.