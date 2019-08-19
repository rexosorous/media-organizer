# handles all database interactions

import peewee
from playhouse import shortcuts
import config as cfg





########################################################
################# DATABASE TABLE STUFF #################
########################################################

db = peewee.SqliteDatabase('media.db', pragmas={
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
    alt_title = peewee.CharField(unique=True, null=True)
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
            basic[key] = data[key]
        elif key in cfg.FOREIGN:
            basic[key] = get(FIELD_TO_TABLE[key], data[key]) if data[key] else None
        elif key in cfg.MTM:
            mtm[key] = [get(FIELD_TO_TABLE[key], val) for val in data[key].split(', ')] if data[key] else None

    return [basic, mtm]



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
    if type(media) is str: # allows for passing by entry object or title
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
    return [x.name for x in globals()[table].select()]          # AHHHHHHHHHHHHHH



def get_table() -> [dict]:
    # gets information on every piece of media in the database and returns it as a list of dicts
    table = []
    for entry in Media.select():
        table.append(get_dict(entry))
    return table



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



def delete_media(media):
    # properly deletes a media entry
    clear_mtm(media)
    media.delete_instance()



def delete_field(field: dict, set_to: dict):
    # properly deletes a non-media entry
    pass



def enter(basic_info: dict, mtm_info = {}):
    # enters in a media entry using info dict to fill fields
    # note 1: info dict MUST have the following fields: title, media_type, animated, country, subtitles
    # note 2: info dict can have missing fields that are not in the above
    # note 3: info dict must have database gets as values
    # note 4: mtm_info dict is optional values must be lists of database gets

    # TODO
    #   find a better way to handle mtm fields

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



def create(table: str, name: str):
    # creates a non-media entry
    TABLES[table].insert(name=name).execute()



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








########################################################
##################### BATCH ENTRY ######################
########################################################
# TODO - don't repeat code and try to consolidate enter_imdb and enter_mal into one function

def enter_imdb(batch: [dict]):
    # for mass inputting movies scraped from imdb

    genres_list = [g.name for g in Genres.select()]
    directors_list = [d.name for d in Directors.select()]
    actors_list = [a.name for a in Actors.select()]

    for film in batch:
        try:
            m = Media.create(title=film['title'], media_type=MediaTypes.get(name='Movie'), animated=False, country=Countries.get(name='USA'),
                year=int(film['year']), plot=film['description'])
            m.language.add(Languages.get(Languages.name=='English'))

            try:
                for genre in film['genre']:
                    if genre in genres_list:
                        m.genres.add(Genres.get(Genres.name==genre))
            except:
                print(f"{film['title']} - error adding genres")

            try:
                if film['directors'][0] in directors_list:
                    m.director = Directors.get(name=film['directors'][0])
            except:
                print(f"{film['title']} - error adding director")

            try:
                for actor in film['actors']:
                    if actor in actors_list:
                        m.actors.add(Actors.get(Actors.name==actor))
            except:
                print(f"{film['title']} - error adding actors")

            m.save()
        except:
            print(f"{film['title']} - error in initial setup")



def enter_mal(batch: [list]):
    # for mass inputting anime scraped from myanimelist using mal_scraper.py
    # expected input: list of anime -> [basic info, staff]
    genres_list = [g.name for g in Genres.select()]
    directors_list = [d.name for d in Directors.select()]
    actors_list = [a.name for a in Actors.select()]
    studios_list = [s.name for s in Studios.select()]

    for anime in batch:
        basic = anime[0]
        staff = anime[1]
        try:
            m = Media.create(title=basic['title'], alt_title=basic['title_english'], media_type=MediaTypes.get(name='TV Series'), animated=True,
                country=Countries.get(name='Japan'), subtitles=True, year=int(basic['aired']['from'][:4]), plot=basic['synopsis'])
            m.language.add(Languages.get(Languages.name=='Japanese'))

            try:
                for genre in basic['genres']:
                    if genre['name'] in genres_list:
                        m.genres.add(Genres.get(Genres.name==genre['name']))
            except:
                print(f"{basic['title']} - error adding genres")

            try: # this section relies on the assumption that there aren't two directors of the film in directors_list
                for director in [d['name'] for d in staff if 'Director' in d['positions']]:
                    director = director.split(', ')
                    dname = director[1] + ' ' + director[0]
                    if dname in directors_list:
                        m.director = Directors.get(name=dname)
                        break
            except:
                print(f"{basic['title']} - error adding director")

            try: # this section relise on the assumption that there aren't two studios of the film in studios_list
                for studio in [s['name'] for s in basic['studios']]:
                    if studio in studios_list:
                        m.studio=Studios.get(name=studio)
                        break
            except:
                print(f"{basic['title']} - error adding studio")

            m.save()

        except:
            print(f"{basic['title']} - error in initial setup")


# def wipe():
#     Media.get(id=1).language.clear()
#     Media.get(id=1).genres.clear()
#     Media.get(id=1).actors.clear()
#     Media.get(id=1).tags.clear()
#     Media.get(id=1).delete_instance()