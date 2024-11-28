#!/usr/bin/env python3

import subprocess
import sys
import glob
import zlib

UESAVE_TYPE_MAPS = [
    ".worldSaveData.CharacterSaveParameterMap.Key=Struct",
    ".worldSaveData.FoliageGridSaveDataMap.Key=Struct",
    ".worldSaveData.FoliageGridSaveDataMap.ModelMap.InstanceDataMap.Key=Struct",
    ".worldSaveData.MapObjectSpawnerInStageSaveData.Key=Struct",
    ".worldSaveData.ItemContainerSaveData.Key=Struct",
    ".worldSaveData.CharacterContainerSaveData.Key=Struct",
]

def main():
    # Check if argument exists
    if len(sys.argv) < 3:
        print('convert-to-json.py <uesave.exe> <save_path>')
        exit(1)
    # Take the first argument as the path to uesave.exe
    uesave_path = sys.argv[1]
    # Take the second argument as a path to the save directory
    save_path = sys.argv[2]
    # Find all .sav files in the directory, ignore backup files
    files = glob.glob(save_path + '/*.sav') + glob.glob(save_path + '/Players/*.sav')
    # Loop through all files
    for file in files:
        # Open the file
        with open(file, 'rb') as f:
            # Read the file
            data = f.read()
            uncompressed_len = int.from_bytes(data[0:4], byteorder='little')
            compressed_len = int.from_bytes(data[4:8], byteorder='little')
            magic_bytes = data[8:11]
            save_type = data[11]
            # Check for magic bytes
            if data[8:11] != b'PlZ':
                print(f'File {file} is not a save file, found {magic_bytes} instead of P1Z')
                continue
            # Valid save types
            if save_type not in [0x30, 0x31, 0x32]:
                print(f'File {file} has an unknown save type: {save_type}')
                continue
            # We only have 0x31 (single zlib) and 0x32 (double zlib) saves
            if save_type not in [0x31, 0x32]:
                print(f'File {file} uses an unhandled compression type: {save_type}')
                continue
            if save_type == 0x31:
                # Check if the compressed length is correct
                if compressed_len != len(data) - 12:
                    print(f'File {file} has an incorrect compressed length: {compressed_len}')
                    continue
            # Decompress file
            uncompressed_data = zlib.decompress(data[12:])
            if save_type == 0x32:
                # Check if the compressed length is correct
                if compressed_len != len(uncompressed_data):
                    print(f'File {file} has an incorrect compressed length: {compressed_len}')
                    continue
                # Decompress file
                uncompressed_data = zlib.decompress(uncompressed_data)
            # Check if the uncompressed length is correct
            if uncompressed_len != len(uncompressed_data):
                print(f'File {file} has an incorrect uncompressed length: {uncompressed_len}')
                continue
            # Save the uncompressed file
            with open(file + '.gvas', 'wb') as f:
                f.write(uncompressed_data)
            print(f'File {file} uncompressed successfully')
            # Convert to json with uesave
            # Run uesave.exe with the uncompressed file piped as stdin
            # Standard out will be the json string
            uesave_run = subprocess.run(uesave_params(uesave_path, file+'.json'), input=uncompressed_data, capture_output=True)
            # Check if the command was successful
            if uesave_run.returncode != 0:
                print(f'uesave.exe failed to convert {file} (return {uesave_run.returncode})')
                print(uesave_run.stdout.decode('utf-8'))
                print(uesave_run.stderr.decode('utf-8'))
                continue
            print(f'File {file} (type: {save_type}) converted to JSON successfully')

def uesave_params(uesave_path, out_path):
    args = [
        uesave_path,
        'to-json',
        '--output', out_path,
    ]
    for map_type in UESAVE_TYPE_MAPS:
        args.append('--type')
        args.append(f'{map_type}')
    return args

if __name__ == "__main__":
    main()
