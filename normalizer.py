#encoding=utf8
########################################################
'''
READ MY COMMENT BELOW
'''
########################################################

import os
import operator
from num2words import num2words
import gc
import io
import json
import re

INPUT_PATH = r'./input'
DATA_INPUT_PATH = r'./input/en_with_types'
SUBM_PATH = r'./output'

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
OTH = str.maketrans("፬", "4")

INCH_TMP = r'\d+""'

def inflect_transform(data):
    data = re.sub(r'-|,|\band\b', ' ', data)
    data = data.split(' ')
    data = [x for x in data if x is not '']
    return ' '.join(data)

def INCH_transform(data):
    neo_data = data[:-2]
    return ' '.join([inflect_transform(num2words(int(neo_data))), 'inches'])

def train():
    print('Train start...')
    
    file = "en_train.csv"
    train = open(os.path.join(INPUT_PATH, "en_train.csv"), encoding='UTF8')
    line = train.readline()
    res = dict()
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
        if arr[0] != arr[1]:
            not_same += 1
        if arr[0] not in res:
            res[arr[0]] = dict()
            res[arr[0]][arr[1]] = 1
        else:
            if arr[1] in res[arr[0]]:
                res[arr[0]][arr[1]] += 1
            else:
                res[arr[0]][arr[1]] = 1
    train.close()
    print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))
    
    files = os.listdir(DATA_INPUT_PATH)
    for file in files:
        train = open(os.path.join(DATA_INPUT_PATH, file), encoding='UTF8')
        while 1:
            line = train.readline().strip()
            if line == '':
                break
            total += 1
            pos = line.find('\t')
            text = line[pos + 1:]
            if text[:3] == '':
                continue
            arr = text.split('\t')
            if arr[0] == '<eos>':
                continue
            if arr[1] != '<self>':
                not_same += 1
    
            if arr[1] == '<self>' or arr[1] == 'sil':
                arr[1] = arr[0]
    
            if arr[0] not in res:
                res[arr[0]] = dict()
                res[arr[0]][arr[1]] = 1
            else:
                if arr[1] in res[arr[0]]:
                    res[arr[0]][arr[1]] += 1
                else:
                    res[arr[0]][arr[1]] = 1
        train.close()
        print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))
    # res is now all the ['before']['after'] pairs
    gc.collect()
    return res

def dump_res(res, path):
    with io.open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

def load_res(path):
    with io.open(path) as f:
        res = json.loads(f.read())
    return res
    
#res = train()
path = './output/res.json'
#dump_res(res, path)
res = load_res(path)

print('len(res): {}'.format(len(res)))

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
    out = open(os.path.join(SUBM_PATH, 'baseline_ext_en.csv'), "w", encoding='UTF8')
    out.write('"id","after"\n')
    test = open(os.path.join(INPUT_PATH, "en_test.csv"), encoding='UTF8')
    line = test.readline().strip()
    while 1:
        line = test.readline().strip()
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
        if line in res:
            # here return the first (value, cnt) with line as key
            srtd = sorted(res[line].items(), key=operator.itemgetter(1), reverse=True)
            out.write('"' + srtd[0][0] + '"')
            changes += 1
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
