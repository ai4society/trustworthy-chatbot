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

def extract_intent(text):
    stop_free = ' '.join([word for word in text.lower().split() if word not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = ' '.join([lemma.lemmatize(word) for word in punc_free.split()])
    
    clean_text =  normalized.split()
    
    bigram = list(ngrams(clean_text, 2))
    trigram = list(ngrams(clean_text,3))
    fourgram=list(ngrams(clean_text,4))
    if len(fourgram) == 0 and len(trigram) == 0:
        intent_value = '_'.join(bigram[0])
    elif len(fourgram) == 0 and len(trigram) != 0:
        intent_value = '_'.join(trigram[0])
    elif len(fourgram) != 0:
        intent_value = '_'.join(fourgram[0])
        
    return intent_value

# read json file to dict
# question_dic = json.load(open('sc_voter_faq.json'))
QA_df = pd.read_csv('data/input/Chat.csv')
QA_df['Intent'] = QA_df['Question'].apply(extract_intent)
# print()
# for i in range(len(QA_df)):
#     intent = extract_intent(QA_df['Question'][i])
#     QA_df['Intent'][i] = intent
#     print(intent)

QA_df.to_csv('data/input/Chat_intent.csv', index=False)
# print(QA_df)