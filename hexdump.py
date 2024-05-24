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

FIELD_LABEL = f'| location | {'bytes/offset':^{BYTE_FIELD_WIDTH}} | {'ascii':^{ASCII_FIELD_WIDTH}}|'

OFFSET_LABEL = f'{'|':-<{LOCATION_FIELD_WIDTH+1}}| {''.join([f'{i:02X} ' for i in range(CHUNK_SIZE)]):{BYTE_FIELD_WIDTH}}|{'|':->{ASCII_FIELD_WIDTH+2}}'

# What to print to screen if byte chunks repeat or empty byte.
SKIP_SYMBOL = '*'

EMPTY_BYTE = b''


def main():
    parser = argparse.ArgumentParser(prog='hexdump', epilog='Dumps file contents to the terminal as Location:hex | bytes:hex | bytes:ascii')
    
    parser.add_argument('file', help='File to hexdump')
    parser.add_argument('-o','--output-file',help='File to output dump to as csv', default='')

    args = parser.parse_args()

    file = None
    try:
        with open(args.file, 'rb') as f:
            file = b''.join(f.readlines())
    except Exception as e:
        print(f'[!] Could not read file! => {e}')

    dump = hexdump(file)
    
    if args.output_file != '':
        try:
            output_to_file(args.output_file, dump)
        except Exception as e:
            print(f'[!] Could not write to file! => {e}')            

def hexdump(src:bytes) -> list[tuple[str, bytes, str]]:
    ''' Dump hex values of src as location in hex, hex, ascii.
        Unprintable values default to ".".
        If a chunk(s) of by
SKIP_SYMBOL = '*'tes repeat * is printed instead.
    '''
    print(FIELD_LABEL)   
    print(OFFSET_LABEL)
    
    dumped_hex = []
    last_chunk = b''
    skipped = False
    for i in range(0,len(src), CHUNK_SIZE):
        chunk = src[i:i+CHUNK_SIZE]
        ascii_chunk = hex2chr(chunk)
        
        location = f'0x{i:07X}'
        bytes_str = ''.join([f'{chunk[i:i+BYTE_GROUP_SIZE].hex()} ' for i in range(0, len(chunk), BYTE_GROUP_SIZE)]).strip()
        ascii_str = ''.join([f'{ascii_chunk[i:i+ASCII_GROUP_SIZE]} ' for i in range(0,len(ascii_chunk),ASCII_GROUP_SIZE)]).strip()
        
        if chunk == EMPTY_BYTE or chunk == last_chunk and skipped:
            continue
        if chunk == last_chunk:
            print(SKIP_SYMBOL)
            skipped = True
            continue

        print(f' {location} | {bytes_str:{BYTE_FIELD_WIDTH}} | {ascii_str}')
        
        dumped_hex.append((location,chunk,ascii_chunk))
        last_chunk = chunk[:]
        skipped = False

    return dumped_hex

def hex2chr(byte_string):
    ''' Converts a string of hex values into a string of printable chrs'''
    return ''.join([chr(b) if len(repr(chr(b))) == 3 else '.' for b in byte_string])

def output_to_file(file_path, data):
    with open(file_path, 'w') as f:
        f.write('location, bytes, ascii\n')
        for line in data:
            f.write(f'{line[0]},{line[1]},{line[2]}\n')

if __name__ == '__main__':
    main()
