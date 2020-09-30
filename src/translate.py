import csv
import six
import sys
from google.cloud import translate_v2 as translate


split = ['../split/#.csv']
for i in range(97, 123):
    split.append(f'../split/{chr(i)}.csv')

first_line = ['Abbreviation', 'Meaning', 'Translation', 'Wikipedia', 'Verified']

translator = translate.Client()


def translate(text, source='en', target='zh-CN', raw=False):
    text = text.decode("utf-8") if isinstance(text, six.binary_type) else text
    # I don't know why, Google says that.
    t_result = translator.translate(text, target_language=target, source_language=source)
    if raw:
        return t_result
    else:
        return t_result['translatedText']


for i in split:
    tmp = []
    with open(i, encoding='utf-8', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            tmp.append(row)
    for j in tmp:
        try:  # bad network
            if not j[2]:
                result = translate(j[1])
                j[2] = result
                sys.stdout.write('\r' + f'Get: {j[1]}')
        except:
            pass
    with open(i, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(sorted(tmp))
    print(i, 'Done')
