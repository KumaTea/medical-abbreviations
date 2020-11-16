import csv
import time
import sqlite3
from add import get_first
from common import first_line
from combine import format_query


db_path = f'../ALL.db'
table_name = 'MedAbbr'


def query():
    t0 = time.time()
    match = []
    word = input('Input your query word: ') or None
    if not word:
        exit('No word provided.')
    first = get_first(word)
    with open(f'../split/{first}.csv', encoding='utf-8', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            if row[0].lower() == word.lower():
                match.append(row)
    print('\n\n----- RESULTS ------\n')
    for item in match:
        print(f'{first_line[0]}: {item[0]}\n{first_line[1]}: {item[1]}\n{first_line[2]}: {item[2]}\n'
              f'{first_line[3]}: {item[3]}\n{first_line[4]}: {item[4]}\n{first_line[5]}: {item[5]}\n\n')
    print('Time cost:', f'{int((time.time()-t0))}ms')
    return True


def query_sql():
    t0 = time.time()
    word = input('Input your query word: ') or None
    if not word:
        exit('No word provided.')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query_word = (format_query(word),)
    cursor.execute(f'SELECT * FROM {table_name} WHERE Query=?', query_word)
    match = cursor.fetchall()
    connection.close()
    print('\n\n----- RESULTS ------\n')
    for item in match:
        print(f'{first_line[0]}: {item[0]}\n{first_line[1]}: {item[1]}\n{first_line[2]}: {item[2]}\n'
              f'{first_line[3]}: {item[3]}\n{first_line[4]}: {item[4]}\n{first_line[5]}: {item[5]}\n\n')
    print('Time cost:', f'{int((time.time()-t0))}ms')
    return True


if __name__ == '__main__':
    # query()
    query_sql()
