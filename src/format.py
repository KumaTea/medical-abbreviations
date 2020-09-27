import os
import csv
import requests


def get_wiki(item, lang='en', variation='wiki'):
    result = requests.get(f'https://{lang}.wikipedia.org/{variation}/{item}')
    if result.status_code == 200:
        wiki_link = result.text.replace('<link rel="canonical" href="', 'r@ndom}-=||').split('r@ndom}-=||')[-1]
        return wiki_link[:wiki_link.find('"/>')]
    return ''
