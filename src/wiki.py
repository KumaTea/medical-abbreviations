import csv
import sys
import requests
from common import first_line
from bs4 import BeautifulSoup


split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')


def get_wiki(item, lang='en', variation='wiki'):
    result = requests.get(f'https://{lang}.wikipedia.org/{variation}/{item}')
    if result.status_code == 200:
        soup = BeautifulSoup(result.text)
        wiki_link = soup.find('link', rel='canonical')['href']
        return wiki_link
    return ''


def wiki():
    for item in split:
        tmp = []
        with open(item, encoding='utf-8', newline='') as f:
            content = csv.reader(f)
            next(content)
            for row in content:
                tmp.append(row)
        for j in tmp:
            if not j[5]:  # verified
                try:  # bad network
                    if not j[3]:
                        if result := get_wiki(j[1]):
                            j[3] = result
                            sys.stdout.write('\r' + f'Get: {j[1]}')
                except:
                    pass
        with open(item, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(first_line)
            writer.writerows(sorted(tmp))
        print(item, 'Done')


if __name__ == '__main__':
    wiki()
