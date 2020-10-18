import csv
from common import first_line, ALL_file


ALL = []

split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')


def combine():
    for item in split:
        tmp = []
        with open(item, encoding='utf-8', newline='') as f:
            content = csv.reader(f)
            next(content)
            for row in content:
                tmp.append(row)
        ALL.extend(sorted(tmp))

    with open(ALL_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(ALL)


if __name__ == '__main__':
    combine()
