SPECIAL_COLON = '꞉'

def from_windows(filename: str):
    return filename.replace(SPECIAL_COLON, ':')

def to_windows(filename: str):
    return filename.replace(':', SPECIAL_COLON)