import requests
import json

Ghibli_BASE = "https://ghibliapi.herokuapp.com/films"

sentiment = 'http://text-processing.com/api/sentiment/'


def display_all():
    r = requests.get(Ghibli_BASE)
    print(r.status_code)
    r = r.json()
    print(r)


def get_title(query):
    r = requests.get(Ghibli_BASE)
    r = r.json()
    for i in range(len(r)):
        if r[i]['title'] == query:
            return(r[i])
