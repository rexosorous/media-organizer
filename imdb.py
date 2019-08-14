import json
import os

def file_open(filename: str):
    with open(filename, 'r') as file:
        imdb = json.load(file)
    return imdb

def find(film_name: str):
    for movie in imdb:
        if movie['title'].lower() == film_name.lower():
            return movie

def owned_movies():
    owned = []
    for root, folder, file in os.walk('G:\Films\Movie'):
        owned.append(folder)
    owned = owned[0]
    return owned