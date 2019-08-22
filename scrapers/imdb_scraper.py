import imdb
import db_handler as db



imdb = imdb.IMDb()



def search(title: str):
    # searches imdb for the first 3 most likely results and returns a list of processed info dictionaries
    search = imdb.search_movie(title)[:3]
    search_results = [imdb.get_movie(film.movieID) for film in search]
    fixed_results = []

    # mtm fields
    genres = db.get_all('Genres')
    directors = db.get_all('Directors')
    actors = db.get_all('Actors')
    studios = db.get_all('Studios')

    # convert the dicts gotten from scraper into readable dicts we can use
    for film in search_results:
        info = {
            'title': film.get('title'),
            'alt_title': '',
            'animated': True if 'Animation' in film.get('genres') else False,
            'year': str(film.get('year')),
            'genres': [g for g in film.get('genres') if g in genres],
            'plot': film.get('plot outline')
        }

        # Countries         we can only have one entry for this field and there can be more than one country in film.get, so we pick the first match
        if film.get('countries'):
            for country in film.get('countries'):
                if country in db.get_all('Countries'):
                    info['country'] = country
                    break

        if film.get('cast'):
            info['actors'] = [a for a in actors if a in [c['name'] for c in film.get('cast')]]

        if film.get('languages'): # might return None
            info['language'] = [lang for lang in film.get('languages') if lang in db.get_all('Languages')]

        # convert media types
        if 'Documentary' in film.get('genres'):
            info['media_type'] = 'Documentary'
        elif 'movie' == film.get('kind'):
            info['media_type'] = 'Movie'
        elif 'tv series' == film.get('kind'):
            info['media_type'] = 'TV Series'
        else:
            info['media_type'] = ''

        # directors
        if film.get('director'): # film.get('director') could return None
            for director in film.get('director'):
                if director['name'] in directors:
                    info['director'] = director['name']
                    break
        if 'director' not in info.keys():
            info['director'] = '' # make sure it's at least a blank string because we need it to display to create window

        # studio
        if film.get('production companies'):
            for studio in film.get('production companies'):
                if studio['name'] in studios:
                    info['studio'] = studio['name']
                    break


        fixed_results.append(info)

    return fixed_results