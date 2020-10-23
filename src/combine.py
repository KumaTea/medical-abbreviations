import os
import csv
import sqlite3
from common import first_line, ALL_file


split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')


def get_all():
    all_words = []
    for item in split:
        tmp = []
        with open(item, encoding='utf-8', newline='') as f:
            content = csv.reader(f)
            next(content)
            for row in content:
                tmp.append(row)
        all_words.extend(sorted(tmp))
    return all_words


def combine():
    with open(ALL_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(get_all())


def gen_db(name='ALL.db'):
    file_path = f'../{name}'
    table_name = 'MedAbbr'

    all_words = get_all()
    if os.path.isfile(file_path):
        os.remove(file_path)
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()

    cursor.execute(f'CREATE TABLE \"{table_name}\" ('
                   f'\"{first_line[0]}\" TEXT, \"{first_line[1]}\" TEXT,'
                   f'\"{first_line[2]}\" TEXT, \"{first_line[3]}\" TEXT,'
                   f'\"{first_line[4]}\" TEXT, \"{first_line[5]}\" TEXT)')
    for word in all_words:
        cursor.execute(f'INSERT INTO \"{table_name}\" VALUES (' + str(word)[1:-1] + ')')
    connection.commit()
    connection.close()
    return True


if __name__ == '__main__':
    combine()
    gen_db()
