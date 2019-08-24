import os
import shutil
import config as cfg
from send2trash import send2trash
import json


SPECIAL_COLON = '꞉' # windows does not allow real colons in file or folder names


def from_windows(filename: str or list):
    # converts special colons to colons for database storage/lookup
    if isinstance(filename, list): # handle being passed lists
        fixed = []
        for name in filename:
            fixed.append(name.replace(SPECIAL_COLON, ':'))
        return fixed
    elif isinstance(filename, str):
        return filename.replace(SPECIAL_COLON, ':')



def to_windows(filename: str):
    # converts colons to special colons for name windows files/folders
    return filename.replace(':', SPECIAL_COLON)



def scan(directories: [str]) -> dict:
    # returns a list of each folder inside of each directory given
    rdir = {} # return directories
    for directory in directories:
        rdir[directory] = from_windows(os.listdir(cfg.directory + 'Media\\' + directory))
    return rdir



def stringify(data) -> str:
    # main_table only accepts strings, so we convert non-strings datatypes to output to the table
    if type(data) is list:
        data = ', '.join(data)
    elif type(data) in [int, float, bool]:
        data = str(data)
    return data



def to_path(media_type: str, title: str):
    # dynamically creates a file location depending on what media type it is and what the title is
    return os.path.realpath(cfg.directory + 'Media\\' + to_windows(media_type) + '\\' + to_windows(title))



def move(old_path, new_path):
    # moves and/or renames a file if it's title or media type are changed
    shutil.move(old_path, new_path)



def open_file(path):
    # opens windows explorer to a movie selection
    os.startfile(path)



def copy_database(new):
    with open('configs.json', 'r') as file:
        x = json.load(file)
        original = x['database']
    shutil.copy(original, new)



def recycle(media_type: str, title: str):
    send2trash(to_path(media_type, title))