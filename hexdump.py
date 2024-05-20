#!/bin/python3
''' A utility for dumping file information as hex
    by Arkadeien
'''

import argparse

# Bytes to grab for each line of a dump
CHUNK_SIZE = 16
# Byte sections when printing to screen.
BYTE_GROUP_SIZE = 4
# How many groups the ascii string .
ASCII_GROUP_SIZE = 8
# What to print to screen if byte chunks repeat.
SKIP_SYMBOL = '*'
# Place holder for values that aren't printable.
PLACEHOLDER = '.'
# Separator that goes between the hex and ascii strings.
SEPARATOR = '|'
# Just a empty byte.
EMPTY_BYTE = b''

HEX_PRINT_WIDTH = 39

def main():
    parser = argparse.ArgumentParser(prog='hexdump', epilog='Dumps file contents to the terminal in Location:hex | bytes:hex | bytes:ascii')
    
    parser.add_argument('file', help='File to hexdump')

    args = parser.parse_args()

    file = None
    try:
        with open(args.file, 'rb') as f:
            file = b''.join(f.readlines())
    except Exception as e:
        print(f'[!] Could not read file! => {e}')

    hex_dump(file)

def hex2chr(byte_string):
    ''' Converts a string of hex values into a string of printable chrs'''
    return ''.join([chr(int(b)) if len(repr(chr(b))) == 3 else PLACEHOLDER for b in byte_string])

def section_string(string, sections):
    ''' Take a string and put spaces in between characters. 
        string = aabbccdd
        sections = 2
        result = "aa bb cc dd"
    '''
    sectioned_string = ''
    for i in range(0,len(string),sections):
        sectioned_string += f'{string[i:i+sections]:{sections}} '
    
    return sectioned_string.strip()

def hex_dump(src):
    ''' Dump hex values of src as location in hex, hex, ascii.
        Unprintable values default to ".".
        If a chunk(s) of bytes repeat a * is printed instead.
    '''
    last_chunk = b''
    skipped = False
    for i in range(0,len(src), CHUNK_SIZE):
        chunk_string = src[i:i+CHUNK_SIZE].hex()
       
        location = f'0x{i:06X}'
        ascii_string = section_string(hex2chr(src[i:i+CHUNK_SIZE]), ASCII_GROUP_SIZE)
        hex_string = section_string(chunk_string, BYTE_GROUP_SIZE)
       
        if chunk_string == EMPTY_BYTE or chunk_string == last_chunk and skipped:
            continue
        if chunk_string == last_chunk:
            print(SKIP_SYMBOL)
            skipped = True
            continue

        print(f'{location} | {hex_string:{HEX_PRINT_WIDTH}} | {ascii_string}')

        last_chunk = chunk_string[:]

        skipped = False

if __name__ == '__main__':
    main()
