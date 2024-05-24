#!/bin/python3
''' A utility for dumping file information as hex
    by Arkadeien
'''

import argparse


# Bytes to grab for each line of a dump
CHUNK_SIZE = 16

BYTE_GROUP_SIZE = 1

ASCII_GROUP_SIZE = 8

LOCATION_FIELD_WIDTH = 10 

BYTE_FIELD_WIDTH = (CHUNK_SIZE*2) + int(CHUNK_SIZE/BYTE_GROUP_SIZE) - 1

ASCII_FIELD_WIDTH = CHUNK_SIZE + int(CHUNK_SIZE/ASCII_GROUP_SIZE) - 1

TOTAL_FIELD_WIDTH = LOCATION_FIELD_WIDTH + BYTE_FIELD_WIDTH + ASCII_FIELD_WIDTH + 4
# What to print to screen if byte chunks repeat or empty byte.

FIELD_LABEL = f'| location | {'offset':^{BYTE_FIELD_WIDTH}} | {'ascii':^{ASCII_FIELD_WIDTH}}|'

OFFSET_LABEL = f'{'|':-<{LOCATION_FIELD_WIDTH+1}}| {''.join([f'{i:02X} ' for i in range(CHUNK_SIZE)]):{BYTE_FIELD_WIDTH}}|{'|':->{ASCII_FIELD_WIDTH+2}}'

SKIP_SYMBOL = '*'

EMPTY_BYTE = b''


def main():
    parser = argparse.ArgumentParser(prog='hexdump', epilog='Dumps file contents to the terminal as Location:hex | bytes:hex | bytes:ascii')
    
    parser.add_argument('file', help='File to hexdump')

    args = parser.parse_args()

    file = None
    try:
        with open(args.file, 'rb') as f:
            file = b''.join(f.readlines())
    except Exception as e:
        print(f'[!] Could not read file! => {e}')

    hex_dump(file)

def hex_dump(src):
    ''' Dump hex values of src as location in hex, hex, ascii.
        Unprintable values default to ".".
        If a chunk(s) of bytes repeat * is printed instead.
    '''
    last_chunk = b''
    skipped = False
    

    print(FIELD_LABEL)   
    print(OFFSET_LABEL)

    for i in range(0,len(src), CHUNK_SIZE):
        chunk = src[i:i+CHUNK_SIZE]

        if chunk == EMPTY_BYTE or chunk == last_chunk and skipped:
            continue
        if chunk == last_chunk:
            print(SKIP_SYMBOL)
            skipped = True
            continue

        ascii_chunk = hex2chr(chunk)
        ascii_str = ''.join([f'{ascii_chunk[i:i+ASCII_GROUP_SIZE]} ' for i in range(0,len(ascii_chunk),ASCII_GROUP_SIZE)]).strip()
        bytes_str = ''.join([f'{chunk[i:i+BYTE_GROUP_SIZE].hex()} ' for i in range(0, len(chunk), BYTE_GROUP_SIZE)]).strip()

        print(f' 0x{i:07X} | {bytes_str:{BYTE_FIELD_WIDTH}} | {ascii_str}')

        last_chunk = chunk[:]
        skipped = False

def hex2chr(byte_string):
    ''' Converts a string of hex values into a string of printable chrs'''
    return ''.join([chr(b) if len(repr(chr(b))) == 3 else '.' for b in byte_string])


if __name__ == '__main__':
    main()
