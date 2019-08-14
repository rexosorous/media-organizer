# object that handles all database interactions


import peewee
import filename

SPECIAL_COLON_CHARACTER = '꞉'   # ASCII value: 42889

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
    media_type = peewee.ForeignKeyField(MediaTypes, backref='media') # movie | tv show | other?
    animated = peewee.BooleanField()
    country = peewee.ForeignKeyField(Countries, backref='media') # japanese | western | chinese | etc
    language = peewee.ManyToManyField(Languages, backref='media')
    subtitles = peewee.BooleanField(default=False)
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
exit

def create_director(director: str):
    Directors.insert(name=director)

def create_actors(actor: str):
    Actors.insert(name=actor)

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



def fix_imdb(batch: [dict]):
    directors_list = [d.name for d in Directors.select()]

    for film in batch:
        try:
            m = Media.get(title=film['title'])

            try:
                if film['directors'][0] in directors_list:
                    m.director = Directors.get(name=film['directors'][0])
            except:
                print(f"{film['title']} - error adding director")

            m.save()
        except:
            print(f"{film['title']} - error in initial setup")


# def wipe():
#     Media.get(id=1).language.clear()
#     Media.get(id=1).genres.clear()
#     Media.get(id=1).actors.clear()
#     Media.get(id=1).tags.clear()
#     Media.get(id=1).delete_instance()