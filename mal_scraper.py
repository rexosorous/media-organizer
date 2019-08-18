from jikanpy import Jikan # python wrapper for an unofficial myanimelist API        link: https://github.com/AWConant/jikanpy
import json
import os
import filename
from time import sleep

ADDRESS = r'G:\Films\TEMP\TV Shows'

mal = Jikan()

def owned():
    return os.listdir(ADDRESS)

def search(anime: str):
    search_results = mal.search('anime', anime)['results'][:5]
    search_dict = {0: mal.anime(search_results[0]['mal_id'])} # intialize the dict with one entry

    selection = 0
    if filename.from_windows(anime).lower() not in [search_dict[0]['title'].lower(), search_dict[0]['title_english']]: # if the title matches the first search result exactly, no need to prompt for user input
        print(f"Current Title: {anime}\n")
        print('Search Results:')
        for index, result in enumerate(search_results): # only now add the rest of the search results to the dict to cut down on amount of requests
            if index != 0:
                search_dict[index] = mal.anime(search_results[index]['mal_id'])
            print(f"     {index} || {search_dict[index]['title']} || {search_dict[index]['title_english']}")
        print('     5 || not listed')
        selection = int(input('choose one of the above: '))
        if selection > 4 or selection < 0: # if result not listed, manual intervention required
            return

    os.rename(ADDRESS+'\\'+anime, ADDRESS+'\\'+filename.to_windows(search_dict[selection]['title'])) # renames the folder to the title that appears on mal
    return (search_dict[selection], mal.anime(search_results[selection]['mal_id'], extension='characters_staff')['staff']) # returns a tuple of (anime entry, staff)

def batch_search(anime_list: [str]):
    output = []
    last = len(anime_list)
    for index, anime in enumerate(anime_list):
        print(f"{index} of {last}")
        sleep(1) # avoid timing out
        result = search(anime)
        if result:
            output.append(result)
        os.system('cls')
    print('task completed')
    return output