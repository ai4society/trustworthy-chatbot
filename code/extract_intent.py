"""Takes Chat.csv with QA pairs, and creates a new column consisting of unique user intents for each query. Saves to Chat_intent.csv"""

import nltk
from nltk import ngrams
from nltk.corpus import stopwords
import string
from nltk.stem.wordnet import WordNetLemmatizer
import warnings
import json
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(
    description="""Takes input csv with QA pairs (defaults to CSV), and creates a new column consisting of unique user intents for each query. Saves to Chat_intent.csv"""
)

# define kwarg for file
parser.add_argument("-f", "--file", help="Path to the input CSV file")


args = parser.parse_args()

csv_file = args.file

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
warnings.simplefilter("ignore")

# set of all filler words that don't contribute to meaning (at, is, the, etc.)
stop = set(stopwords.words("english"))
# set of all ASCII punctuation
punctuation = set(string.punctuation)
# converts words to their base form (runs to run, apples to apple, etc.)
lemma = WordNetLemmatizer()

intent_values = {}  # keeps track of all extracted intents


def get_clean_text(text: str, remove_stop=True):
    """
    Args:
      text: string to be cleaned
      remove_stop: flag that controls if stop words like at, is, the, etc. are removed
    Returns:
      base_words: list of all words in the text converted to base form
    """

    # remove stop words if desired
    if remove_stop:
        words = text.lower().split()
        text = " ".join([word for word in words if word not in stop])

    # remove punctuation
    text = "".join(ch for ch in text if ch not in punctuation)

    # return the list of words converted to their base form
    base_words = [lemma.lemmatize(word) for word in text.split()]
    return base_words


def extract_intent(question: str):
    """Given a user question, extracts the intent by removing all stop words and punctuation and converting all words to base words
    Args:
       question: User question string
    Returns:
       intent_value: a string with underscores seperating the keywords of the question
    """
    if not question:
        raise RuntimeError("Empty question passed into extract_intent method")

    # get a list of all base words in the question excluding stop words and punctuation
    clean_text = get_clean_text(question, True)

    # if we can't create bigrams after removing stop words, we try it without removing
    bigrams = list(ngrams(clean_text, 2))
    if not bigrams:
        clean_text = get_clean_text(question, False)

    # get bigrams, trigrams, and fourgrams
    bigrams = list(ngrams(clean_text, 2))
    trigrams = list(ngrams(clean_text, 3))
    fourgrams = list(ngrams(clean_text, 4))

    # Return the most detailed and unique string possible representing intent of query
    # key assumption here is that no two questions will have the first four same keywords
    # TODO, try to do away with this assumption
    # maybe keep a set that keeps track of previous intent values
    # and generate a longer intent if already seen
    if not fourgrams:
        if not trigrams:
            intent_value = "_".join(bigrams[0])
        else:
            intent_value = "_".join(trigrams[0])
    else:
        intent_value = "_".join(fourgrams[0])

    return_intent = intent_value
    if intent_value in intent_values:
        return_intent += str(intent_values[intent_value])
    intent_values[intent_value] = intent_values.get(intent_value, 0) + 1
    return return_intent


def get_new_intent(text: str):
    """Creating new intent for a given text
    Args:
       text: string for which we are generating new intent
    Returns:
       intent_value: a string with underscores seperating the keywords of the question
    """
    clean_text = get_clean_text(text, False)

    # get ngrams from n = 2 to n = 5
    bigram = list(ngrams(clean_text, 2))
    trigram = list(ngrams(clean_text, 3))
    fourgram = list(ngrams(clean_text, 4))
    fivegram = list(ngrams(clean_text, 5))

    # Return most detailed string possible
    if fivegram:
        intent_value = "_".join(fivegram[0])
    elif fourgram:
        intent_value = "_".join(fourgram[0])
    elif trigram:
        intent_value = "_".join(trigram[0])
    elif bigram:
        intent_value = "_".join(bigram[0])
    else:
        raise RuntimeError(
            "Inputted text to get_new_intent() function did not have enough words to generate bigrams"
        )
    return intent_value


def main():
    if not csv_file:
        csv_file = "Chat.csv"
    elif not csv_file.endswith(".csv"):
        raise RuntimeError(
            f"You've supplied file name {csv_file}, which is not a csv file"
        )
    csv_file = os.path.join("data", "input", csv_file)
    # read question answer pairs and create intent for each question

    try:
        QA_df = pd.read_csv(csv_file)
    except Exception as e:
        raise RuntimeError(f"There was an error opening file {csv_file}, {e.msg}")
    QA_df["Intent"] = QA_df["Question"].apply(extract_intent)

    intents = QA_df["Intent"].to_list()
    assert len(intents) == len(set(intents))

    for i in range(len(QA_df)):
        for j in range(len(QA_df)):
            if i == j:
                continue

            # handle duplicate intents for questions
            if QA_df["Intent"][i] == QA_df["Intent"][j]:
                QA_df["Intent"][j] = get_new_intent(QA_df["Question"][j])
                QA_df["Intent"][i] = get_new_intent(QA_df["Question"][i])

    # saves to new csv file with a new file representing intents
    QA_df.to_csv("data/input/Chat_intent.csv", index=False)


if __name__ == "__main__":
    main()
