#imports
import nltk
from nltk import ngrams
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import string
from nltk.stem.wordnet import WordNetLemmatizer

import warnings
warnings.simplefilter('ignore')
import json
import pandas as pd

#clean the data
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def get_clean_text(text, flag):
    
    if flag == 0:
        stop_free = ' '.join([word for word in text.lower().split() if word not in stop])
    else:
        stop_free = text
        
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = ' '.join([lemma.lemmatize(word) for word in punc_free.split()])
    return normalized.split()

def extract_intent(text):
    # print(text)
    
    clean_text =  get_clean_text(text, 0)
    
    bigram = list(ngrams(clean_text, 2))
    
    if len(bigram) == 0:
        clean_text = get_clean_text(text, 1)
    
    bigram = list(ngrams(clean_text, 2))
    trigram = list(ngrams(clean_text,3))
    fourgram = list(ngrams(clean_text,4))
    if len(fourgram) == 0 and len(trigram) == 0:
        intent_value = '_'.join(bigram[0])
    elif len(fourgram) == 0 and len(trigram) != 0:
        intent_value = '_'.join(trigram[0])
    elif len(fourgram) != 0:
        intent_value = '_'.join(fourgram[0])
        
    return intent_value

def get_new_intent(text):
    clean_text =  get_clean_text(text, 1)
    
    bigram = list(ngrams(clean_text, 2))
    trigram = list(ngrams(clean_text,3))
    fourgram = list(ngrams(clean_text,4))
    fivegram = list(ngrams(clean_text,5))
    
    if len(fivegram) != 0:
        return '_'.join(fivegram[0])
    elif len(fourgram) != 0:
        return '_'.join(fourgram[0])
    elif len(trigram) != 0:
        return '_'.join(trigram[0])
    elif len(bigram) != 0:
        return '_'.join(bigram[0])
        

QA_df = pd.read_csv('data/input/Chat.csv')
QA_df['Intent'] = QA_df['Question'].apply(extract_intent)

for i in range(len(QA_df)):
    for j in range(len(QA_df)):
        if i != j:
            if QA_df['Intent'][i] == QA_df['Intent'][j]:
                QA_df['Intent'][j] = get_new_intent(QA_df['Question'][j])
                QA_df['Intent'][i] = get_new_intent(QA_df['Question'][i])
                
# print()
# for i in range(len(QA_df)):
#     intent = extract_intent(QA_df['Question'][i])
#     QA_df['Intent'][i] = intent
#     print(intent)

QA_df.to_csv('data/input/Chat_intent.csv', index=False)
# print(QA_df)