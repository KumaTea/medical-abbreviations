import csv


ALL = []
ALL_file = '../ALL.csv'

split = ['../#.csv']
for i in range(97, 123):
    split.append(f'../{chr(i)}.csv')


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
    writer.writerow(['Abbreviation', 'Meaning', 'Translation', 'More'])
    writer.writerows(ALL)
