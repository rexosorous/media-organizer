from jikanpy import Jikan # python wrapper for an unofficial myanimelist API        link: https://github.com/AWConant/jikanpy
import db_handler as db



mal = Jikan()



def search(anime: str):
    # searches myanimelist for the first 5 most likely results and returns a list of processed info dictionaries
    search = mal.search('anime', anime)['results'][:5] # get the first 5 entries that pop up
    search_results = [(mal.anime(anime['mal_id']), mal.anime(anime['mal_id'], extension='characters_staff')) for anime in search] # get more detailed info on each of those searches
    fixed_results = []
    # mtm fields
    genres = db.get_all('Genres')
    directors = db.get_all('Directors')
    actors = db.get_all('Actors')
    studios = db.get_all('Studios')


    # convert the dicts gotten from scraper into readable dicts we can use
    for anime in search_results:
        info = {
            'title': anime[0]['title'],
            'alt_title': anime[0]['title_english'],
            'animated': True,
            'country': 'Japan',
            'language': 'Japanese',
            'subtitles': True,
            'year': anime[0]['aired']['from'][:4],
            'genres': [g['name'] for g in anime[0]['genres'] if g['name'] in genres],
            'actors': [],
            'plot': anime[0]['synopsis']
        }

        # ignore other media types like OVA and ONA
        if anime[0]['type'] == 'Movie':
            info['media_type'] = 'Movie'
        elif anime[0]['type'] == 'TV': # convert 'TV' to 'TV Series'
            info['media_type'] = 'TV Series'

        # directors
        for director in [d['name'] for d in anime[1]['staff'] if 'Director' in d['positions']]:
            if name_fixer(director) in directors:
                info['director'] = name_fixer(director)
                break
        if 'director' not in info.keys():
            info['director'] = '' # make sure it's at least a blank string because we need it to display to create window

        # voice actors
        for character in anime[1]['characters']:
            for actor in character['voice_actors']:
                if name_fixer(actor['name']) in actors:
                    info['actors'].append(name_fixer(actor['name']))
        if not info['actors']:
            del info['actors']

        # studios
        for studio in [s['name'] for s in anime[0]['studios']]:
            if studio in studios:
                info['studio'] = studio
                break

        fixed_results.append(info)

    return fixed_results




def name_fixer(name: str) -> str:
    # japanese names are formatted like "[last name], [first name]"" so we need to change that
    name_split = name.split(', ')
    if len(name_split) == 1:
        return name
    return name_split[1] + ' ' + name_split[0]