import os


SPECIAL_COLON = '꞉' # windows does not allow real colons in file or folder names

def from_windows(filename: str):
    # converts special colons to colons for database storage/lookup
    return filename.replace(SPECIAL_COLON, ':')

def to_windows(filename: str):
    # converts colons to special colons for name windows files/folders
    return filename.replace(':', SPECIAL_COLON)

def scan(directory: str) -> [str]:
    # returns a list of all folders in directory
    # TODO change to read from multiple directories
    return os.listdir(directory)