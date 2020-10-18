import csv
from wiki import get_wiki
from combine import combine
from common import first_line
try:
    from translate import translate_word
except:  # google.auth.exceptions.DefaultCredentialsError
    def translate_word(text): raise RuntimeError


ALL = []

split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')


def get_first(text):
    text = text[0].lower()
    if 47 < ord(text) < 58:
        return '#'
    elif 97 < ord(text) < 123:
        return text
    else:
        return ''


def add():
    abbr = mean = tr = wp = vf = first = ''
    tmp = []
    while not abbr:
        abbr = input(f'Please input the {first_line[0]}:')
    while not mean:
        mean = input(f'Please input the {first_line[1]}:')
    tr_auto = input("Auto translate? [Y/n]") or 'Y'
    if tr_auto.lower() == 'n':
        tr = input(f'Please input the {first_line[2]}:') or ''
    else:
        try:  # If no Google Translate API access
            tr = translate_word(mean)
        except:
            tr = 'Error: no Google Translate API access'
        tr = input(f'Accept \"{tr}\" (default) or input manually:') or tr
    print(f'Trying to get {first_line[3]} link...')
    wp = get_wiki(mean)
    wp = input(f'Result: {wp}\nAccept or input manually:') or wp
    vf = input("Mark as verified? [Y/n]") or 'Y'
    first = get_first(abbr)
    first = input(f'Accept \"{first}\" as the first letter or input manually:') or first
    if (input(f'\n\n\n\n----- VERIFICATION ------\n'
              f'{first_line[0]}: {abbr}\n{first_line[1]}: {mean}\n{first_line[2]}: {tr}\n{first_line[3]}: {wp}\n'
              f'{first_line[4]}: {vf}\n\nLooks good? [Y/n]') or 'Y') == 'n':
        raise RuntimeError

    print('Writing...')

    with open(f'../split/{first}.csv', encoding='utf-8', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            tmp.append(row)
    tmp.append([abbr, mean, tr, wp, vf])
    with open(f'../split/{first}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(sorted(tmp))

    combine()


if __name__ == '__main__':
    add()
