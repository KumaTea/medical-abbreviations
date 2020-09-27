import csv
import sys
import requests

split = ['../#.csv']
for i in range(97, 123):
    split.append(f'../{chr(i)}.csv')

first_line = ['Abbreviation', 'Meaning', 'Translation', 'More']


def get_wiki(item, lang='en', variation='wiki'):
    result = requests.get(f'https://{lang}.wikipedia.org/{variation}/{item}')
    if result.status_code == 200:
        wiki_link = result.text.replace('<link rel="canonical" href="', 'r@ndom}-=||').split('r@ndom}-=||')[-1]
        return wiki_link[:wiki_link.find('"/>')]
    return ''


for i in split:
    tmp = []
    with open(i, encoding='utf-8', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            tmp.append(row)
    for j in tmp:
        try:  # bad network
            if not j[3]:
                if result := get_wiki(j[1]):
                    j[3] = result
                    sys.stdout.write('\r' + f'Get: {j[1]}')
                elif result := get_wiki(j[0]):
                    if 'disambiguation' not in result.lower():
                        j[3] = result
                        sys.stdout.write('\r' + f'Get: {j[1]}')
        except:
            pass
    with open(i, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(sorted(tmp))
    print(i, 'Done')
