import csv

files = ['../ALL.csv']

abbr = {'#': []}
for i in range(97, 123):
    abbr[chr(i)] = []

first_line = ['Abbreviation', 'Meaning', 'Translation', 'Wikipedia', 'Verified']


def isnumber(item):
    item = str(item)[:1]
    return True if 47 < ord(item) < 58 else False


def split(source):
    assert isinstance(source, str)
    with open(source, encoding='utf-8', newline='') as f:
        source_csv = csv.reader(f)
        next(source_csv)
        current = '#'
        for row in source_csv:
            if current == '#' and isnumber(row[0]):
                abbr['#'].append([row[0], row[1], '', row[2]])
            else:
                current = row[0][:1].lower()
                abbr[current].append([row[0], row[1], '', row[2]])


for i in files:
    split(i)

for i in abbr:
    with open(f'../split/{i}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(sorted(abbr[i]))
