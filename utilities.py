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

def stringify(data) -> str:
    # main_table only accepts strings, so we convert non-strings datatypes to output to the table
    if type(data) is list:
        data = ', '.join(data)
    elif type(data) in [int, float, bool]:
        data = str(data)
    return data

def to_path(media_type: str, title: str):
    # dynamically creates a file location depending on what media type it is and what the title is
    return os.path.realpath(cfg.directory + 'Media' + '\\' + util.to_windows(media_type) + '\\' + util.to_windows(title))

def move(old_path, new_path):
    # moves and/or renames a file if it's title or media type are changed
    os.rename(old_path, new_path)