from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd
import json
import warnings
from typing import List

# tokenizer will tokenize text and model will paraphrase
tokenizer = AutoTokenizer.from_pretrained("prithivida/parrot_paraphraser_on_T5")
model = AutoModelForSeq2SeqLM.from_pretrained("prithivida/parrot_paraphraser_on_T5")


warnings.filterwarnings("ignore")


# Init models (make sure you init ONLY once if you integrate this to your code)
# parrot = Parrot()


def paraphrase_question_list(questions: List[str]):
    """Generates paraphrases for each question in the inputted list
    Args:
       question: list of strings which are user queries
    Returns:
       all_paraphrases: nested list with each element being a list of paraphrases corresponding to a question
    """
    all_paraphrases = []

    # generate paraphrases for each question
    for question in questions:
        paraphrases = []

        # tokenizes the question
        input_tokens = tokenizer(question, return_tensors="pt").input_ids

        generated_tokens = model.generate(
            input_tokens,
            max_length=100,  # Maximum length of output sequence
            num_beams=10,  # beam search width
            early_stopping=True,  # stops when no better sequences are found
            top_p=0.99,
            top_k=30,
            num_return_sequences=6,  # returns 6 different paraphrases
        )

        # decodes all tokens into english
        paraphrases = [
            tokenizer.decode(paraphrase_tokens, skip_special_tokens=True)
            for paraphrase_tokens in generated_tokens
        ]

        # stores result
        all_paraphrases.append(paraphrases)

    return all_paraphrases


def main():
    # read questions and generate paraphrases for each questions
    QA_df = pd.read_csv("data/input/Chat_intent.csv")
    questions = QA_df["Question"].tolist()
    question_set = set(questions)
    paraphrased_list = paraphrase_question_list(questions)

    # iterate over list of all paraphrases and remove all duplicates
    for i in range(len(paraphrased_list)):
        for paraphrase in paraphrased_list[i]:
            if paraphrase in question_set:
                paraphrased_list[i].remove(paraphrase)
                paraphrased_list[i] = list(set(paraphrased_list[i]))

    # zip corresponding question and its paraphrases and package into a dictionary
    dict_paraphrased = {
        question: paraphrases
        for question, paraphrases in zip(questions, paraphrased_list)
    }

    # save to json file
    with open("data/input/paraphrased.json", "w") as f:
        json.dump(obj=dict_paraphrased, fp=f, indent=4)


if __name__ == "__main__":
    main()
