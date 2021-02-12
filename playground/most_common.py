import pandas as pd

INPUT_DIR = '../input/'
OUTPUT_DIR = '../output/'

train = pd.read_csv(INPUT_DIR+'en_train.csv')

d = train.groupby(['before', 'after']).size()
d = d.reset_index().sort_values(0, ascending=False)
d = d.loc[d['before'].drop_duplicates(keep='first').index]
d = d.loc[d['before'] != d['after']]
d = d.set_index('before')['after'].to_dict()


test = pd.read_csv(INPUT_DIR+'en_test.csv')
test['after'] = test.before.apply(lambda x: d[x] if x in d.keys() else x)

test['id'] = test.sentence_id.astype(str) + '_' + test.token_id.astype(str)
test[['id', 'after']].to_csv(OUTPUT_DIR+'submission.csv', index=False)
