import os
import csv
import six
import sys
from google.cloud import translate_v2 as translate
try:
    from local import cert_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cert_path
except ImportError:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = input('Input your GOOGLE_APPLICATION_CREDENTIALS:') or ''


split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')

first_line = ['Abbreviation', 'Meaning', 'Translation', 'Wikipedia', 'Verified']

translator = translate.Client()


def translate_word(text, source='en', target='zh-CN', raw=False):
    text = text.decode("utf-8") if isinstance(text, six.binary_type) else text
    # I don't know why, Google says that.
    t_result = translator.translate(text, target_language=target, source_language=source)
    if raw:
        return t_result
    else:
        return t_result['translatedText']


def translate():
    for item in split:
        tmp = []
        with open(item, encoding='utf-8', newline='') as f:
            content = csv.reader(f)
            next(content)
            for row in content:
                tmp.append(row)
        for j in tmp:
            try:  # bad network
                if not j[2]:
                    result = translate_word(j[1])
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
