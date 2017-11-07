## Dataset

###en_train.csv

```
sentence_id, token_id, class, before, after
```

###en_test.csv

```
sentence_id, token_id, before
```

###en_smaple_submission.csv

```
id, after
```

## EDA

EDA: exploratory data analysis

https://www.kaggle.com/headsortails/watch-your-language-update-feature-engineering

## Baseline

Change nothing: **0.9231**

### normalizer{0, 0_}

Change to the most frequent pattern in training set: **0.9867**

### normalizer1

[More data](https://www.kaggle.com/google-nlu/text-normalization/downloads/text-normalization.zip) && num2words && measure rules: 

### normalizer2

decimal, digit, money rules: 

Actually this is of no use, since only 4 inches instance not appeared in training set.

## Method

### normalizer

[Big data](https://storage.googleapis.com/text-normalization/en_with_types.tgz) && num2words && measure rules: **0.9954**