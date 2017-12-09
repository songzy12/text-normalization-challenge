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

### a_letter

```
$ grep dot baseline_ext_en.csv | wc -l
934
```

change all `a_letter` to `a`: **0.9957**

## ambiguous

```
LI: fifty one, fifty first, the fifty first, l i
```

build another dictionary with (before, class) as a key:  **0.9978**

## test_2

**0.9924** , rank 44



##  Rank 21 Solution

<https://www.kaggle.com/c/text-normalization-challenge-english-language/discussion/43901>

1. Use XGBoost with Context Label Data to predict test case's class.
2. For some class, apply customized normalize function.
3. Use XGBoost to deal with binary ambiguous case: like `-` and `:`.

## Rank 19 Solution

<https://www.kaggle.com/c/text-normalization-challenge-english-language/discussion/44049>

1. Reclassing: 40 classes
2. Sub-tokens: `-17.5` -> `-` `17` `.` `5`
3. Classifier: LSTM with token index, sub-token type indexes, sub-token length indexes, token w2v embedding.
4. Limiting output types: by adding a large positive constant to valid classes.
5. Ensemble: two models, one for same replacement, while all other classes from the second model.
6. 20% of training for validation. Adam optimizer. Cross entropy loss. Batch size 64. Epoch 10. 6 hours on GTX1060. Public dataset is used.

## Rank 4 Solution

<https://www.kaggle.com/c/text-normalization-challenge-english-language/discussion/43963>

1. Statistical approach: possible transformations for each word with context. Plain text and common transformations.
2. Pattern based approach: regular expression. Dates, times, numbers, phones, URLs.
3. ML approach: several LightGBM models for decoding on ambiguous cases, mostly binary decisions.