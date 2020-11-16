import csv
from urllib import request
from add import quiet_add
from combine import combine
from common import upstream, ignore_words


# guc = 'https://raw.github.cnpmjs.org'
guc = 'https://raw.githubusercontent.com'
upstream_link = [
    f'{guc}/{upstream}/master/%23-M%2C%20medical%20abbreviations.csv',
    f'{guc}/{upstream}/master/N-Z%2C%20medical%20abbreviations.csv'
]


if __name__ == '__main__':
    print('Get all words...')
    all_words = []
    with open(f'../ALL.csv', encoding='utf-8', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            all_words.append(row[1].lower())

    print('Get upstream...')
    upstream_content = []
    for item in upstream_link:
        result = request.urlopen(item)
        upstream_content.append([line.decode('utf-8') for line in result.readlines()])

    new_words = []
    for f in upstream_content:
        content = csv.reader(f)
        next(content)
        for row in content:
            if row[1].lower() not in all_words and row[1].lower() not in ignore_words:
                print(f'Adding {row[1]}...')
                new_words.append(row)

    print('Applying...')
    for word in new_words:
        quiet_add(abbr=word[0], mean=word[1], wp=word[2])

    combine()
