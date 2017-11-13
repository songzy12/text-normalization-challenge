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
import string
import code

from io import open

INPUT_PATH = r'./input'
DATA_INPUT_PATH = r'./input/en_with_types'
SUBM_PATH = r'./output'

#SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
#SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
#OTH = str.maketrans("፬", "4")
SUB = None
SUP = None
OTH = None

INCH_TMP = r'\d+""'

def inflect_transform(data):
    data = re.sub(r'-|,|\band\b', ' ', data)
    data = data.split(' ')
    data = [x for x in data if x is not '']
    return ' '.join(data)

def WEB_transform(data):
    if '.' not in data:
        return data
    before = data
    after = []
    m = {u'.':'dot', 
         u'/':'slash',
         u':':'colon',
         u',':'comma',
         u'-':'dash'}
    for char in data:
        if char in m:
            after.append(m[char])
        else:
            after.append(char)
    after = ' '.join(after)
    #print('before:', before)
    #print('after:', after)
    return ' '.join(after)

def INCH_transform(data):
    neo_data = data[:-2]
    return ' '.join([inflect_transform(num2words(int(neo_data))), 'inches'])

def train():
    print('Train start...')
    
    file = "en_train.csv"
    train = open(os.path.join(INPUT_PATH, "en_train.csv"), encoding='UTF8')
    line = train.readline()
    #res = dict()
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
        #if arr[0] not in res:
        #    res[arr[0]] = dict()
        #    res[arr[0]][arr[1]] = 1
        #else:
        #    if arr[1] in res[arr[0]]:
        #        res[arr[0]][arr[1]] += 1
        #    else:
        #        res[arr[0]][arr[1]] = 1

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
    
    #files = os.listdir(DATA_INPUT_PATH)
    #for file in files:
    #    train = open(os.path.join(DATA_INPUT_PATH, file), encoding='UTF8')
    #    while 1:
    #        line = train.readline().strip()
    #        if line == '':
    #            break
    #        total += 1
    #        pos = line.find('\t')
    #        text = line[pos + 1:]
    #        if text[:3] == '':
    #            continue
    #        arr = text.split('\t')
    #        if arr[0] == '<eos>':
    #            continue
    #        if arr[1] != '<self>':
    #            not_same += 1
    #
    #        if arr[1] == '<self>' or arr[1] == 'sil':
    #            arr[1] = arr[0]
    #
    #        if arr[0] not in res:
    #            res[arr[0]] = dict()
    #            res[arr[0]][arr[1]] = 1
    #        else:
    #            if arr[1] in res[arr[0]]:
    #                res[arr[0]][arr[1]] += 1
    #            else:
    #                res[arr[0]][arr[1]] = 1
    #    train.close()
    #    print(file + ':\tTotal: {} Have diff value: {}'.format(total, not_same))
    # res is now all the ['before']['after'] pairs
    gc.collect()
    #return res
    return res_class

def dump_res(res, path):
    with io.open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))

def load_res(path):
    with io.open(path) as f:
        res = json.loads(f.read())
    return res
    
#res = train()
res_path = './output/res.json'
res_class_path = './output/res_class.json'
#dump_res(res, path)
res_class = load_res(res_class_path)
res = load_res(res_path)

print('len(res): {}'.format(len(res)))
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

    m = {}
    
    out = open(os.path.join(SUBM_PATH, 'baseline_ext_class_en.csv'), "w", encoding='UTF8')
    out.write('"id","after"\n')
    test = open(os.path.join(INPUT_PATH, "en_test.csv"), encoding='UTF8')
    pred = open(os.path.join(SUBM_PATH, "pred_test.csv"), encoding='UTF8')
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

        if ".".join([line, tag]) in res_class:
            srtd = sorted(res_class[".".join([line, tag])].items(), key=operator.itemgetter(1), reverse=True)
            line = srtd[0][0]

            before = line
            line = re.sub(r'\b_letter\b', ' ', line)
            for l in string.ascii_letters[:26]:
                line = re.sub(l+'_letter', l, line)
            line = ' '.join(filter(lambda x: x, line.split(' ')))
            #if before != line:
            #    print('before:', before)
            #    print('after:', line) 

            out.write('"' + line + '"')
            m[".".join([before, tag])] = line 
            changes += 1


        elif line in res:
            #if len(res[line]) > 1:
            #    m[line] = [total, res[line]]
            if tag == 'ELECTRONIC' and '.' in line:
                line = WEB_transform(line)
            else:
                # here return the first (value, cnt) with line as key
                srtd = sorted(res[line].items(), key=operator.itemgetter(1), reverse=True)
                line = srtd[0][0]

                before = line
                line = re.sub(r'\b_letter\b', ' ', line)
                for l in string.ascii_letters[:26]:
                    line = re.sub(l+'_letter', l, line)
                line = ' '.join(filter(lambda x: x, line.split(' ')))
                #if before != line:
                #    print('before:', before)
                #    print('after:', line) 

            out.write('"' + line + '"')
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

    with open('output/ambi_class.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=4))

test()
