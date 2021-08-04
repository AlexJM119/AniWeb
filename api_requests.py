import requests
import json

Ghibli_BASE = "https://ghibliapi.herokuapp.com/films"

sentiment = 'http://text-processing.com/api/sentiment/'

r = requests.get(Ghibli_BASE)
#print(r.status_code)
r = r.json()

query = 'Castle in the Sky'
senti = ''

for i in range(len(r)):
#    if r[i]['title'] == query:
    senti = requests.post(sentiment, data={'text' : r[i]['description']})
    print(r[i]['title']+' | ', end='')
    print(sent.json())
