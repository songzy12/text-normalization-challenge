import numpy as np
import pandas as pd

df = pd.read_csv('input/en_train.csv')

print df.head(10)
print df['class'], unique()

length = df.groupby(['sentence_id'], as_index=False).count()
length = length.groupby(['before'], as_index=False).count()
length['before'].describe()

df[df['class'] == 'PUNCT'].head()
df[df['class'] == 'DATE'].head(10)
