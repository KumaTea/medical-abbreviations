import os
import csv
import six
import sys
import requests
from common import first_line
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as google_tl
try:
    from local import cert_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cert_path
except ImportError:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = input('Input your GOOGLE_APPLICATION_CREDENTIALS:') or ''


split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')

translator = google_tl.Client()


def translate_from_wiki(wiki, variation='zh-cn'):
    result = requests.get(wiki)
    soup = BeautifulSoup(result.text, features='lxml')
    tr = soup.find('a', lang='zh', class_='interlanguage-link-target')
    if tr:
        zh_result = requests.get(tr['href'].replace('/wiki/', f'/{variation}/'))
        soup = BeautifulSoup(zh_result.text, features='lxml')
        zh = soup.find('h1', id='firstHeading', lang='zh-Hans-CN')
        if zh:
            print('Get Wikipedia result!')
            return zh.text
    return ''


def translate_word(text, source='en', target='zh-CN', wiki=None, return_type=False):
    text = text.decode("utf-8") if isinstance(text, six.binary_type) else text
    # I don't know why, Google says that.
    result = ''
    tr_type = 'n'

    if wiki and 'wiki' in wiki.lower():
        w_result = translate_from_wiki(wiki)
        if w_result:
            result = w_result
            tr_type = 'w'
    if not result:
        t_result = translator.translate(text, target_language=target, source_language=source)
        result = t_result['translatedText']
        tr_type = 'g'

    if return_type:
        return result, tr_type
    else:
        return result


def translate():
    for item in split:
        tmp = []
        with open(item, encoding='utf-8', newline='') as f:
            content = csv.reader(f)
            next(content)
            for row in content:
                tmp.append(row)
        for j in tmp:
            if not j[5]:  # verified
                try:  # bad network
                    if not j[2]:
                        result = translate_word(j[1], wiki=j[3])
                        j[2] = result
                        sys.stdout.write('\r' + f'Get: {j[1]}')
                except:
                    pass
        with open(item, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(first_line)
            writer.writerows(sorted(tmp))
        print(item, 'Done')


if __name__ == '__main__':
    translate()
