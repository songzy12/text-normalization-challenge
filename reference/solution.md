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