#!/bin/python3
''' A utility for dumping file information as hex
    by Arkadeien
'''

import argparse
import sys

from typing import NamedTuple

CHUNK_SIZE = 16

LOCATION_FIELD_WIDTH = 10 

SKIP_SYMBOL = '*'

DONT_PAUSE = -1

HEX_LEN = 1

ASCII_LEN = CHUNK_SIZE//2

BYTE_FIELD_WIDTH = (CHUNK_SIZE*2) + CHUNK_SIZE//HEX_LEN - 1 


class ByteChunk(NamedTuple):
    bytes:bytes = b""
    ascii:str = ""
    location:int = 0
    end_location:int = 0


def main():
    parser = argparse.ArgumentParser(prog="hexdump", epilog=f"Dumps file contents to the terminal. Repeated byte chunks are replaced by {SKIP_SYMBOL}. Multiple bytes chunks that repeat are shrotened to a single {SKIP_SYMBOL}.")
    
    # Required arguments
    parser.add_argument("file_path", help="File to hexdump"),
    
    # Options
    parser.add_argument("-s", "--skip",
                        help="Bytes to skip",
                        type=int,
                        default=0
                        )
    parser.add_argument("-p", "--pause-every",
                        type=int,
                        help="Pauses dump n lines at a time. Waits <enter> press then continues",
                        default=DONT_PAUSE
                        )
    parser.add_argument("--chunk_length",
                        help="The amount of bytes read per chunk",
                        default=CHUNK_SIZE
                        )
    
    args = parser.parse_args()

    chunks = next_bytes(args.file_path, args.chunk_length, args.skip)
    hex_dump(chunks, args.pause_every)

def next_bytes(file_path:str, read_length:int, start) -> ByteChunk:
    try:
        with open(file_path, "rb") as f:
            location = 0
            chunk = b" "
            if start:
                f.seek(start)
            while chunk:     
                chunk = f.read(read_length)
                ascii = "".join([chr(b) if len(repr(chr(b))) == 3 else "." for b in chunk])
                start = location
                end = location + len(chunk)
                location = end
                if not chunk:
                    break
                yield ByteChunk(chunk, ascii, start, end)
    
    except FileNotFoundError as e:
        print(f"[!!] {e.strerror} => {file_path}")

        sys.exit(0)

def hex_dump(chunks:list[ByteChunk], pause_every:int) -> None:
    last_bytes = None
    skipped = False
    line = 0
    for chunk in chunks:
        if not pause_every == DONT_PAUSE and line%pause_every == 0 and chunk.location != 0:
            try:
                input()
            except KeyboardInterrupt:
                print("[I] Exiting dump")
                sys.exit(0)
        if chunk.location != 0 and chunk.bytes == last_bytes and not skipped:
            print(SKIP_SYMBOL)
            skipped = True
            continue
        if skipped and chunk.bytes == last_bytes:
            continue

        bytes = " ".join(chunk.bytes[v:v+HEX_LEN].hex() for v in range(0,len(chunk.bytes),HEX_LEN))
        ascii = " ".join(chunk.ascii[v:v+ASCII_LEN] for v in range(0,len(chunk.ascii),ASCII_LEN))
        print(f"{chunk.location:#08x} | {bytes:{BYTE_FIELD_WIDTH}} | {ascii}")
        last_bytes = chunk.bytes
        skipped = False
        line += 1

if __name__ == '__main__':
    #test_hexdump() 
    main()
