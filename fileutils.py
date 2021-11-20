import hashlib
import os
from dataclasses import dataclass

BLOCK_SIZE = 65536 # The size of each read from the file


@dataclass
class File:
    name: str
    path: str
    hash: str = None

    def full_filename(self):
        return self.path + "/" + self.name


def get_hash(file):
    file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file

    return file_hash.hexdigest()


def get_file_name(full_file_name: str):
    return full_file_name.split("/")[-1]


def get_files(directory: str):
    files = []

    for (path, dirname, filenames) in os.walk(directory):
        files += [File(f, path) for f in filenames]

    return files


def find_file(file: File, other_files: list):
    # For each file in the main dir, check for the file in all of the other dirs
    for other_file in other_files:
        if get_file_name(file.name) == get_file_name(other_file.name):
            return other_file
    return None