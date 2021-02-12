# encoding=utf8
########################################################
'''
READ MY COMMENT BELOW
'''
########################################################

import os
import operator
import gc
import re
import string
import code

from num2words import num2words

from helper import *

INPUT_DIR = r'./input'
OUTPUT_DIR = r'./output'


def train():
    print('Train start...')

    file = "en_train.csv"
    train = open(os.path.join(INPUT_DIR, "en_train.csv"), encoding='UTF8')
    line = train.readline()
    res_class = dict()
    total = 0
    not_same = 0
    while 1:
        line = train.readline().strip()
        if line == '':
            break
        total += 1
        pos = line.find('","')
        text = line[pos + 2:]
        if text[:3] == '","':
            continue
        text = text[1:-1]
        arr = text.split('","')
        # arr[0], arr[1] are 'before', 'after' now
        pos_class = line.find(',"')
        text_class = line[pos_class+2:pos]

        if arr[0] != arr[1]:
            not_same += 1

        if ('.'.join([arr[0], text_class])) not in res_class:
            res_class['.'.join([arr[0], text_class])] = dict()
            res_class['.'.join([arr[0], text_class])][arr[1]] = 1
        else:
            if arr[1] in res_class['.'.join([arr[0], text_class])]:
                res_class['.'.join([arr[0], text_class])][arr[1]] += 1
            else:
                res_class['.'.join([arr[0], text_class])][arr[1]] = 1

    train.close()
    print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))

    # res is now all the ['before']['after'] pairs
    gc.collect()
    return res_class


res_class = train()
print('len(res_class): {}'.format(len(res_class)))

sdict = {}
sdict['km2'] = 'square kilometers'
sdict['km'] = 'kilometers'
sdict['kg'] = 'kilograms'
sdict['lb'] = 'pounds'
sdict['dr'] = 'doctor'
sdict['m²'] = 'square meters'


def test():
    total = 0
    changes = 0

    test = open(os.path.join(INPUT_DIR, "en_test_2.csv"), encoding='UTF8')
    pred = open(os.path.join(OUTPUT_DIR, "pred_test.csv"), encoding='UTF8')

    out = open(os.path.join(OUTPUT_DIR, 'submission.csv'),
               "w", encoding='UTF8')
    out.write('"id","after"\n')

    line = test.readline().strip()
    line_pred = pred.readline().strip()
    while 1:
        line = test.readline().strip()
        try:
            line_pred = pred.readline().strip()
        except:
            code.interact(local=locals())
        if line == '':
            break

        pos = line.find(',')
        i1 = line[:pos]
        line = line[pos + 1:]

        pos = line.find(',')
        i2 = line[:pos]
        line = line[pos + 1:]

        line = line[1:-1]
        out.write('"' + i1 + '_' + i2 + '",')

        pos = line_pred.rfind(',')
        tag = line_pred[pos + 1:]
        label = tag

        before = line

        if ".".join([line, tag]) in res_class:
            srtd = sorted(res_class[".".join([line, tag])].items(
            ), key=operator.itemgetter(1), reverse=True)
            line = srtd[0][0]

            line = re.sub(r'\b_letter\b', ' ', line)
            for l in string.ascii_letters[:26]:
                line = re.sub(l+'_letter', l, line)
            line = ' '.join(filter(lambda x: x, line.split(' ')))

            out.write('"' + line + '"')
            changes += 1
        elif label == 'ADDRESS':
            try:
                norm = address(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'CARDINAL'
        elif label == 'CARDINAL':
            try:
                norm = cardinal(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'DATE'
        elif label == 'DATE':
            try:
                norm = date(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'DECIMAL'
        elif label == 'DECIMAL':
            try:
                norm = decimal(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'DIGIT',
        elif label == 'DIGIT':
            try:
                norm = digit(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'ELECTRONIC',
        elif label == 'ELECTRONIC':
            try:
                norm = electronic(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'FRACTION',
        elif label == 'FRACTION':
            try:
                norm = fraction(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'LETTERS',
        elif label == 'LETTERS':
            try:
                norm = letters(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'MEASURE',
        elif label == 'MEASURE':
            try:
                norm = measure(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'MONEY',
        elif label == 'MONEY':
            try:
                norm = money(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'ORDINAL',
        elif label == 'ORDINAL':
            try:
                norm = ordinal(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'PLAIN' nothing changes
        elif label == 'PLAIN':
            norm = before
            out.write('"' + norm + '"')
        # 'PUNCT',
        elif label == 'PUNCT':
            norm = before
            out.write('"' + norm + '"')
        # 'TELEPHONE',
        elif label == 'TELEPHONE':
            try:
                norm = telephone(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'TIME',
        elif label == 'TIME':
            try:
                norm = time(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        # 'VERBATIM'
        elif label == 'VERBATIM':
            try:
                norm = verbatim(before)
                out.write('"' + norm + '"')
                changes += 1
            except:
                out.write('"' + line + '"')
        else:
            print(line)
            # actually there are only four inches not appeared

            if len(line) > 1:
                val = line.split(',')
                # number with at most 1 ','
                if len(val) == 2 and val[0].isdigit() and val[1].isdigit():
                    line = ''.join(val)

            if line.isdigit():
                srtd = line.translate(SUB)
                srtd = srtd.translate(SUP)
                srtd = srtd.translate(OTH)
                out.write('"' + num2words(float(srtd)) + '"')
                changes += 1
            elif len(line.split(' ')) > 1:
                val = line.split(' ')
                for i, v in enumerate(val):
                    if v.isdigit():
                        srtd = v.translate(SUB)
                        srtd = srtd.translate(SUP)
                        srtd = srtd.translate(OTH)
                        val[i] = num2words(float(srtd))
                    # measure
                    elif v in sdict:
                        val[i] = sdict[v]

                out.write('"' + ' '.join(val) + '"')
                changes += 1
            elif re.match(INCH_TMP, line):
                line = INCH_transform(line)
                print(line)
                out.write('"' + line + '"')
                changes += 1
            else:
                out.write('"' + line + '"')

        out.write('\n')
        total += 1

    print('Total: {} Changed: {}'.format(total, changes))
    test.close()
    out.close()


test()
