#!/usr/bin/env python3

import subprocess
import sys
import glob
import zlib

def main():
    # Check if argument exists
    if len(sys.argv) < 3:
        print('convert-to-sav.py <uesave.exe> <save_path>')
        exit(1)
    # Take the first argument as the path to uesave.exe
    uesave_path = sys.argv[1]
    # Take the second argument as a path to the save directory
    save_path = sys.argv[2]
    # Find all .sav.json files in the directory, ignore backup files
    files = glob.glob(save_path + '/*.sav.json') + glob.glob(save_path + '/Players/*.sav.json')
    # Loop through all files
    for file in files:
        # Convert the file back to binary
        gvas_file = file.replace('.sav.json', '.sav.gvas')
        sav_file = file.replace('.sav.json', '.sav')
        uesave_run = subprocess.run(uesave_params(uesave_path, file, gvas_file))
        if uesave_run.returncode != 0:
            print(f'uesave.exe failed to convert {file} (return {uesave_run.returncode})')
            continue
        # Open the old sav file to get type
        with open(sav_file, 'rb') as f:
            data = f.read()
            save_type = data[11]
        # Open the binary file
        with open(gvas_file, 'rb') as f:
            # Read the file
            data = f.read()
            uncompressed_len = len(data)
            compressed_data = zlib.compress(data)
            compressed_len = len(compressed_data)
            if save_type == 0x32:
                compressed_data = zlib.compress(compressed_data)
            with open(sav_file, 'wb') as f:
                f.write(uncompressed_len.to_bytes(4, byteorder='little'))
                f.write(compressed_len.to_bytes(4, byteorder='little'))
                f.write(b'PlZ')
                f.write(bytes([save_type]))
                f.write(bytes(compressed_data))
        print(f'Converted {file} to {sav_file}')

def uesave_params(uesave_path, input_file, output_file):
    args = [
        uesave_path,
        'from-json',
        '--input', input_file,
        '--output', output_file,
    ]
    return args

if __name__ == "__main__":
    main()
