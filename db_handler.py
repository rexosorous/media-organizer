# handles all database interactions

import peewee
from playhouse import shortcuts
import config as cfg
# import json





########################################################
################# DATABASE TABLE STUFF #################
########################################################


# database_file = ''


# with open('configs.json', 'r') as file:
#     x = json.load(file)
#     database_file = x['database']



db = peewee.SqliteDatabase('database\\media.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,
    'foreign_keys': 1,
    'ignore_check_counstraints': 0,
    'synchronous': 0
    })



class BaseModel(peewee.Model):
    class Meta:
        database = db

# tables linked to Media
class Series(BaseModel):
    name = peewee.CharField(unique=True)
    alt_name = peewee.CharField(unique=True, null=True)

class MediaTypes(BaseModel):
    name = peewee.CharField(unique=True)

class Countries(BaseModel):
    name = peewee.CharField(unique=True)

class Languages(BaseModel):
    name = peewee.CharField(unique=True)

class Directors(BaseModel):
    name = peewee.CharField(unique=True)

class Studios(BaseModel):
    name = peewee.CharField(unique=True)

class Genres(BaseModel):
    name = peewee.CharField(unique=True)
    description = peewee.CharField(null=True)

class Actors(BaseModel):
    name = peewee.CharField(unique=True)

class Tags(BaseModel):
    name = peewee.CharField(unique=True)
    description = peewee.CharField(null=True)

class Media(BaseModel):
    # base table containing all media entries
    title = peewee.CharField(unique=True)
    alt_title = peewee.CharField(null=True)
    series = peewee.ForeignKeyField(Series, backref='sequels', null=True)
    order = peewee.DecimalField(max_digits=2, null=True) # the story's chronological order ex: Star Wars Ep. 1, 2, 3, 4, 5, 6 | NOT 4, 5, 6, 1, 2, 3
    media_type = peewee.ForeignKeyField(MediaTypes, backref='media') # movie | tv show | etc
    animated = peewee.BooleanField()
    country = peewee.ForeignKeyField(Countries, backref='media') # USA | UK | Japan | etc
    language = peewee.ManyToManyField(Languages, backref='media')
    subtitles = peewee.BooleanField(null = True)
    year = peewee.IntegerField(constraints=[peewee.Check('year > 1900')], null=True) # release year
    genres = peewee.ManyToManyField(Genres, backref='media')
    director = peewee.ForeignKeyField(Directors, backref='media', null=True)
    studio = peewee.ForeignKeyField(Studios, backref='media', null=True)
    actors = peewee.ManyToManyField(Actors, backref='media') # ManyToManyField does not support null=True
    plot = peewee.CharField(null=True)
    rating = peewee.IntegerField(constraints=[peewee.Check('rating >= 1 AND rating <=10')], null=True) # 1 to 10
    tags = peewee.ManyToManyField(Tags, backref='media') # ManyToManyField does not support null=True
    notes = peewee.CharField(null=True)



def create_tables():
    # tables created for the ManyToManyField
    MediaLanguage = Media.language.get_through_model()
    MediaGenres = Media.genres.get_through_model()
    MediaActors = Media.actors.get_through_model()
    MediaTags = Media.tags.get_through_model()
    with db:
        db.create_tables([Media, Series, MediaTypes, Countries, Languages, Directors, Studios, Genres, Actors, Tags, MediaLanguage, MediaGenres, MediaActors, MediaTags])














########################################################
################### USABLE FUNCTIONS ###################
########################################################

TABLES = { # used to select the right field class
    'Series': Series,
    'MediaTypes': MediaTypes,
    'Countries': Countries,
    'Languages': Languages,
    'Directors': Directors,
    'Studios': Studios,
    'Genres': Genres,
    'Actors': Actors,
    'Tags': Tags,
    'Media': Media
}

FIELD_TO_TABLE = {
    'series': 'Series',
    'media_type': 'MediaTypes',
    'country': 'Countries',
    'language': 'Languages',
    'director': 'Directors',
    'studio': 'Studios',
    'genres': 'Genres',
    'actors': 'Actors',
    'tags': 'Tags',
}





def dict_fixer(data: dict) -> [dict, dict]:
    # splits up a dictionary into basic and mtm dicts and sets the values to entry objects
    basic = {}
    mtm = {}

    for key in data:
        if key in cfg.SIMPLE:
            basic[key] = data[key] if data[key] != '' else None
        elif key in cfg.FOREIGN:
            basic[key] = get(FIELD_TO_TABLE[key], data[key]) if data[key] else None
        elif key in cfg.MTM:
            mtm[key] = [get(FIELD_TO_TABLE[key], val) for val in data[key].split(', ')] if data[key] else None

    return [basic, mtm]



def to_expression(data: dict) -> list:
    # converts a dict to a list of expressions
    # ex. {'media_type': 'Movie'} -> [db.Media.media_type == db.MedaTypes.get(name='Movie')]
    # requires that the input dicts get run through dict_fixer first
    # i couldn't figure out how to do this without hard coding
    expr = []
    for key in data:
        if key == 'year':
            symbol = data['year'][0]
            year = int(data['year'][1:])
            if symbol == '<':
                expr.append(Media.year < year)
            elif symbol == '>':
                expr.append(Media.year > year)
            elif symbol == '=':
                expr.append(Media.year == year)
        elif key == 'subtitles':
            expr.append(Media.subtitles == data['subtitles'])
        elif key == 'animated':
            expr.append(Media.animated == data['animated'])
    return expr



def to_list(data) -> list:
    # if something isn't a list, make it into a list with one element
    if isinstance(data, list):
        return data
    return [data]



def get(table: str, torn: str): # torn = Title OR Name
    # returns an entry object from table = table with title or name = torn
    try:
        if table == 'Media':
            return Media.get(title=torn)
        return globals()[table].get(name=torn)
    except:
        print(f'could not find {torn} in {table}, setting to None')
        return None



def get_detailed(table: str, kwargs: dict):
    # returns an entry object from table=table with name=name
    # kwargs is a dict where keys are keywords

    # NOTE: this will probably be removed because the GUI portion will take care of this
    return TABLES[table].get(**kwargs)



def get_dict(media) -> dict:
    # finds a media entry and converts its info into a readable dictionary
    if isinstance(media, str): # allows for passing by entry object or title
        media = get('Media', media)

    d = shortcuts.model_to_dict(media, manytomany=True)
    foreign = ['series', 'media_type', 'country', 'director', 'studio']
    mtm = ['language', 'genres', 'actors', 'tags']
    for field in foreign:
        if d[field]:
            d[field] = d[field]['name']
    for field in mtm:
        if d[field]:
            d[field] = [f['name'] for f in d[field]]
    if d['order']:
        d['order'] = float(d['order'])

    del d['id']
    return d



def get_all(table: str) -> [str]:
    # returns all names of every entry in a given table
    return [x.name for x in globals()[table].select()]



def get_by_media_type() -> dict:
    # returns all media names sorted by their media type in a dictionary
    rdict = {} # return dict
    for media_type in MediaTypes.select():
        rdict[media_type.name] = [media.title for media in Media.select().where(Media.media_type==media_type)]
    return rdict



def get_table() -> [dict]:
    # gets information on every piece of media in the database and returns it as a list of dicts
    table = []
    for entry in Media.select():
        table.append(get_dict(entry))
    return table



def get_filtered_table(basic_data: dict, and_data: dict, not_data: dict, or_data: dict) -> [dict]:
    filtered = [] # return list

    if basic_data:
        expr = to_expression(basic_data) # convert basic_data dict into expressions to use in where() statement
        initial = Media.select().where(*expr) # get all media entries where data matches and_basic
    else:
        initial = Media.select()

    for media in initial: # convert to dictionaries because they're easier to work with
        filtered.append(get_dict(media)) # fix this so all relevent data is a list?

    filtered_copy = filtered.copy() # we make a copy so we can iterate over the copy and edit the original. because removing things while iterating "skips" entries
    for media in filtered_copy:
        if media in filtered: # prevents us from deleting something twice
            for key in and_data:
                media_data = to_list(media[key]) # we have to make this conversion for the next if statement, but we don't want to alter the media dict directly
                if not all(item in media_data for item in and_data[key]): # if everything in and_data[key] is not in media_data, invalidate
                    filtered.remove(media)
                    break
        if media in filtered:
            for key in not_data:
                media_data = to_list(media[key])
                if any(item in not_data[key] for item in media_data): # if any item in not_data[key] is in media_data, invalidate
                    filtered.remove(media)
                    break
        if media in filtered:
            for key in or_data:
                media_data = to_list(media[key])
                if not any(item in media_data for item in or_data[key]): # if media_data does not contain any items in or_data[key], invalidate
                    filtered.remove(media)
                    break

    return filtered



def check_exists(table: str, torn: str) -> bool: # torn = Title OR Name
    # checks if a media entry with title already exists
    if len(TABLES[table].select().where(
        (TABLES[table].title if table == 'Media' else TABLES[table].name) # decide whether to use title or name
        ==torn)) == 0:
        return False
    return True



def clear_mtm(media):
    # clears relationships between media and manytomany fields
    media.language.clear()
    media.genres.clear()
    media.actors.clear()
    media.tags.clear()



def delete_media(titles: [str]):
    # properly deletes a media entry
    for title in titles:
        media = Media.get(title=title)
        clear_mtm(media)
        media.delete_instance()



def delete_field(field: str, name: str):
    # properly deletes a non-media entry
    entry = get(FIELD_TO_TABLE[field], name)
    media_vars = vars(Media)
    if field in cfg.FOREIGN:
        Media.update(**{field: None}).where(media_vars[field]==entry).execute()
    elif field in cfg.MTM:
        for media in entry.media:
            fields = {
                'language': media.language,
                'genres': media.genres,
                'actors': media.actors,
                'tags': media.tags
            }
            fields[field].remove(entry)
    entry.delete_instance()



def enter(info: dict):
    # enters in a media entry using info dict to fill fields
    # note 1: info dict MUST have the following fields: title, media_type, animated, country, subtitles
    # note 2: info dict can have missing fields that are not in the above
    # note 3: info dict must have database gets as values
    # note 4: mtm_info dict is optional values must be lists of database gets

    basic_info, mtm_info = dict_fixer(info)

    try:
        m = Media.create(**basic_info)

        mtm_fields = { # many to many fields
            'language': m.language,
            'genres': m.genres,
            'actors': m.actors,
            'tags': m.tags
        }

        for key in mtm_info:
            mtm_fields[key].add(mtm_info[key])

        m.save()
    except peewee.IntegrityError:
        # used to catch instances where media is created without the required fields
        required = ['Title', 'Media Type', 'Animated', 'Country', 'Subtitles']
        print(f"The following fields were left empty:\n {[field for field in required if required not in basic_info.keys()]}")



def create(field: str, name: str):
    # creates a non-media entry
    globals()[FIELD_TO_TABLE[field]].insert(name=name).execute()



def update(title: str, info: dict):
    # updates a selected piece of media and updates it with new info
    # see notes about info dict and mtm_info dict in the above enter function
    basic_info, mtm_info = dict_fixer(info)
    Media.update(**basic_info).where(Media.title==title).execute() # is this the best way to to do this?
    selected = get('Media', info['title'])

    mtm_fields = {
        'language': selected.language,
        'genres': selected.genres,
        'actors': selected.actors,
        'tags': selected.tags
    }

    clear_mtm(selected)
    for field in mtm_info:
        mtm_fields[field].add(mtm_info[field])

    selected.save()



def update_set(title: str, info: dict):
    basic_info, mtm_info = dict_fixer(info)
    if basic_info:
        Media.update(**basic_info).where(Media.title==title).execute()
    selected = get('Media', title)

    mtm_fields = {
        'language': selected.language,
        'genres': selected.genres,
        'actors': selected.actors,
        'tags': selected.tags
    }

    for field in mtm_info:
        for val in mtm_info[field]:
            if val not in mtm_fields[field]:
                mtm_fields[field].add(val)

    selected.save()



def update_remove(title: str, info: dict):
    basic_info, mtm_info = dict_fixer(info)
    selected = get('Media', title)

    for field in basic_info:
        var = vars(selected)['__data__']
        if field in cfg.FOREIGN:
            if var[field] == basic_info[field].id:
                var[field] = None
        else:
            if var[field] == basic_info[field]:
                var[field] = None

    mtm_fields = {
        'language': selected.language,
        'genres': selected.genres,
        'actors': selected.actors,
        'tags': selected.tags
    }

    for field in mtm_info:
        for val in mtm_info[field]:
            if val in mtm_fields[field]:
                mtm_fields[field].remove(val)

    selected.save()