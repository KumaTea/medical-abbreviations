import csv
from wiki import get_wiki
from combine import combine
from common import first_line
try:
    from translate import translate_word
except:  # ImportError or google.auth.exceptions.DefaultCredentialsError
    # Check README for possible solution
    def translate_word(text): raise RuntimeError


ALL = []

split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')


def get_first(text):
    text = text[0].lower()
    if 48 <= ord(text) < 58:
        return '#'
    elif 97 <= ord(text) < 123:
        return text
    else:
        return ''


def write(item, first):
    tmp = []
    with open(f'../split/{first}.csv', encoding='utf-8', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            if row[0].lower() == item[0].lower() and row[1].lower() == item[1].lower():
                raise ValueError('Duplicated word with same abbreviation.')
            tmp.append(row)
    tmp.append(item)
    with open(f'../split/{first}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(sorted(tmp))
    return True


def add():
    abbr = mean = tr = wp = sj = vf = first = ''
    while not abbr:
        abbr = input(f'Please input the {first_line[0]}:')
    while not mean:
        mean = input(f'Please input the {first_line[1]}:')
    print(f'Trying to get {first_line[3]} link...')
    wp = get_wiki(mean)
    wp = input(f'Result: {wp}\nAccept or input manually:') or wp
    tr_auto = input("Auto translate? [Y/n]") or 'Y'
    if tr_auto.lower() == 'n':
        tr = input(f'Please input the {first_line[2]}:') or ''
    else:
        tr_type = 'n'
        try:  # If no Google Translate API access
            tr, tr_type = translate_word(mean, wiki=wp, return_type=True)
        except:
            tr = 'Error: no Google Translate API access'
        tr_src = 'Wikipedia' if tr_type == 'w' else 'Google Translate'
        tr = input(f'Accept \"{tr}\" ({tr_src}) or input manually:') or tr
    sj = input(f'Please input the {first_line[4]}:') or ''
    vf = input(f'Mark as {first_line[5]}? [Y/n]') or 'Y'
    first = get_first(abbr)
    first = input(f'Accept \"{first}\" as the first letter or input manually:') or first
    if (input(f'\n\n\n\n----- VERIFICATION ------\n'
              f'{first_line[0]}: {abbr}\n{first_line[1]}: {mean}\n{first_line[2]}: {tr}\n{first_line[3]}: {wp}\n'
              f'{first_line[4]}: {sj}\n{first_line[5]}: {vf}\n\nLooks good? [Y/n]') or 'Y') == 'n':
        exit('Abort.')

    print('Writing...')
    write([abbr, mean, tr, wp, sj, vf], first)

    cb = input('End adding? [Y/n]') or 'Y'
    if cb.lower() == 'n':
        add()
    return True


def quiet_add(abbr, mean, tr='', wp='', sj='', vf='', first='', cb=False):
    wp = wp or get_wiki(mean)  # or get_wiki(abbr)
    tr = tr or translate_word(mean, wiki=wp)
    first = first or get_first(abbr)
    if not first:
        first = input(f'Unable to detect the first letter of {abbr}: {mean}. '
                      f'Input manually or use \"#\":') or '#'
    write([abbr, mean, tr, wp, sj, vf], first)
    if cb:
        combine()


if __name__ == '__main__':
    add()
