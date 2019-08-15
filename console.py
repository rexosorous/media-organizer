# main driver program that will be replaced by a gui

import os
import db_handler as db




'''TODO
    implement some kind of sort and filter functions'''




# all fields sorted into different input processes
SIMPLE = ['title', 'alt_title', 'order', 'animated', 'subtitles', 'year', 'plot', 'rating', 'notes'] # basic data types
FOREIGN = ['series', 'media_type', 'country', 'director', 'studio'] # foreign key fields
MTM = ['language', 'genres', 'actors', 'tags'] # many to many fields


TABLES = {
    'series': 'Series',
    'media_type': 'MediaTypes',
    'country': 'Countries',
    'director': 'Directors',
    'studio': 'Studios',
    'language': 'Languages',
    'genres': 'Genres',
    'actors': 'Actors',
    'tags': 'Tags'
}


def view():
    os.system('cls')
    title = input('\n\nwhat is the title of the media? ')
    try:
        selection = db.Media.get(title=title)
        print_media(selection)
    except IndexError:
        print('could not find any media with that title. check your casing.')



def edit():
    # edits a media entry with title=title
    try:
        os.system('cls') # clear console
        title = input('\n\nwhat is the title of the media? ')
        selection = db.Media.get(title=title)
        print_media(selection)
        fields = input('which fields would you like to edit? ').split(', ')

        try:
            basic_info = {}
            mtm_info = {}
            for field in fields:
                values = (f'Enter value(s) for {field}: ').split(', ')
                if field in FOREIGN:
                    basic_info[field] = db.get(TABLES[field], {'name': values[0]})
                elif field in MTM:
                    mtm_info[field] = []
                    for v in values:
                        mtm_info[field].append(db.get(TABLES[field], {'name': v}))
                else:
                    basic_info[field] = values[0]
            db.edit(selection, basic_info, mtm_info)
            print('\n\nUpdated Entry:')
            print_media(selection)
            print('\n\n')
        except IndexError:
            print('could not find a value with that name in that field. check your casing.')
    except IndexError:
        print('could not find any media with that title. check your casing.')



def add():
    # adds a new media entry into the database
    os.system('cls') # clears console
    print('\n\nfill out the following info')
    basic_info = {}
    mtm_info = {}
    try:
        for field in SIMPLE:
            basic_info[field] = input(field + ': ')
            if field == 'title': # check to make sure we're not trying to add duplicate entries
                if db.check_exists('Media', basic_info['title']):
                    print('there is already an entry with that title\n\n')
                    return
        for field in FOREIGN:
            basic_info[field] = db.get(TABLES[field], {'name': input(field + ': ')})
        for field in MTM:
            mtm_info[field] = []
            values = input(field + ': ').split(', ')
            for v in values:
                mtm_info[field].append(db.get(TABLES[field], {'name': v}))
        db.enter(basic_info, mtm_info)
    except IndexError:
        print('could not find a value with that name in that field')



def create():
    # creates entries for non-media fields
    os.system('cls') # clears console
    print(f'\n\nfields: {", ".join(FOREIGN + MTM)}')
    field = input('which field do you want to create an entry for? ')

    if field not in SIMPLE + FOREIGN + MTM:
        print('incorrect field selection')
        return

    values = input('enter one or more entries: ').split(', ')
    for v in values:
        if db.check_exists(TABLES[field], v):
            print(f'{v} already exists in {field}') # if it exists, don't try to create a new entry
            continue
        db.create(TABLES[field], v)



def delete():
    # deletes an entry from media
    os.system('cls')
    title = input('what is the title of the media you want to delete? ')
    try:
        db.delete_media(db.get('Media', {'title': title}))
        print(f'successfully deleted {title}')
    except:
        print(f'unable to delete {title}')



def print_media(media):
    # prints all the info about the media, basically as it appears in the database
    output = db.get_dict(media)
    for key in output:
            print('{:12}- {:.100}'.format(key, ', '.join(output[key]) if type(output[key]) is list else output[key] if type(output[key]) is str else str(output[key])))



def stop():
    # exits the program gracefully-ish
    db.db.close()
    os._exit(1)





COMMANDS_DICT = { # used to call the right command function
    'view': view,
    'edit': edit,
    'add': add,
    'create': create,
    'delete': delete,
    'exit': stop
}

# main loop
while True:
    print(f"list of commands: {', '.join(COMMANDS_DICT.keys())}")
    command = input('enter a command: ')

    try:
        COMMANDS_DICT[command]()
    except IndexError:
        print('You entered an incorrect command')