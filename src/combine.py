import csv


ALL = []
ALL_file = '../ALL.csv'

split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')

first_line = ['Abbreviation', 'Meaning', 'Translation', 'Wikipedia', 'Verified']


for i in split:
    tmp = []
    with open(i, encoding='utf-8', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            tmp.append(row)
    ALL.extend(sorted(tmp))


with open(ALL_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(first_line)
    writer.writerows(ALL)
