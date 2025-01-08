import pandas as pd
import os
import shutil
import json
import textwrap
import regex as re
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from typing import List
from datetime import datetime


def get_plain_text_length(answer: str):
    """Calculates the length of the text in characters after removing all links that may appear in the text

    Args:
       text: An answer to a user query which may or may not contain URLs
    Returns:
       answer_len: length of the answer with any URLs removed
    """
    # Regular expression pattern to match URLs
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    # Remove all URLs from the text
    text_without_links = re.sub(url_pattern, "", answer)

    # Calculate the length of the text without URLs
    answer_len = len(text_without_links)
    return answer_len


def summarize(answer: str, length: int = 3):
    """Summarizes a given answer to a user query to 3 sentences
    Args:
       answer: an answer to a given user query
       length: desired maximum length of the summary, defaults to 3 sentences
    Returns:
       summary_text: summary of an answer with specified number of sentences, including a disclaimer
    """

    # Initialize a Latent Semantic Analysis summarizer
    # alternatively could use a LuhnSummarizer()
    summarizer = LsaSummarizer()

    # Setting stop words to just be a single space,
    # allows us to consider all words in our summarization
    # instead of filtering out any
    summarizer.stop_words = [" "]

    # Creates a parser object using an english tokenizer
    # and summarizes it to 3 sentences
    parser = PlaintextParser.from_string(answer, Tokenizer("english"))
    summary = summarizer(parser.document, length)

    # joins sentences with newlines and returns
    summary_text = "\n".join([str(sentence) for sentence in summary])
    return (
        summary_text
        + "\nThis is a brief summary. For more details, please ask for the full answer."
    )


def get_nlu_yaml_string(intent: str, questions: List[str]):
    """Packages intent with question and its paraphrased equivalents in yaml block
    Args:
       intent: string representing the user's intent in query
       questions: list of strings representing equivalent ways of asking the same question
    Returns:
       yaml_str: formatted yaml string with intent and paraphrased questions
    """
    yaml_str = f"\n- intent: {intent}\n  examples: |"

    for question in questions:
        yaml_str += f"\n    - {question}"
    return yaml_str


def get_rules_yaml_string(intent: str):
    """Packages intent and corresponding action in yaml block for rules.yaml
    Args:
       intent: string representing the user's intent in query
    Returns:
       yaml_str: formatted rules yaml string with intent and corresponding utter action
    """
    yaml_str = f"\n- rule: Answer {intent}\n  steps:\n  - intent: {intent}\n  - action: utter_{intent}\n    "
    return yaml_str


def get_stories_yaml_string(intent: str):
    """Packages intent and corresponding action in yaml block for stories.yaml
       We use stories for providing users the option to ask for the summary of their longer answer if they want to.
    Args:
       intent: string representing the user's intent in query
    Returns:
       yaml_str: formatted stories yaml string with intent and corresponding utter action
    """
    yaml_str = f"\n- story: {intent} path\n  steps:\n  - intent: {intent}\n  - action: utter_summary_{intent}\n  - intent: full_answer\n  - action: utter_{intent}\n    "
    return yaml_str


def get_domain_yaml_string(intent: str, answer: str):
    """Packages intent and a corresponding answer in yaml block for domain.yaml
    Args:
       intent: string representing the user's intent in query
       answer: string represent answer to user's query
    Returns:
       yaml_str: formatted domain yaml string with intent and corresponding answer
    """
    yaml_str = (
        f"\n  utter_{intent}:\n  - text: |\n{textwrap.indent(answer, '      ')}\n    "
    )
    return yaml_str


def get_intent_yaml_string(intent: str):
    """Packages intent in yaml block for domain.yaml
    Args:
       intent: string representing the user's intent in query
    Returns:
       yaml_str: formatted yaml string with intent
    """
    domain_data = f"\n  - {intent}"
    return domain_data


def write_list_to_file(yaml_list: List[str], yaml_file: str):
    with open(yaml_file, "a", encoding="utf-8") as f:
        f.write("\n")
        for item in yaml_list:
            f.write(item)


def main():
    # Removes exisiting chatbot by default
    if os.path.exists("Chatbot"):
        shutil.rmtree("Chatbot", ignore_errors=True, onerror=None)

    # copy template to new chatbot directory
    shutil.copytree("rasa_template", "Chatbot")

    # questions, answers, sources, dates, etc.
    QA_df = pd.read_csv("data/input/Chat_intent.csv")
    # do not answer questions
    DNA_questions = pd.read_csv("data/input/DNA.csv")
    # paraphrased equivalents for each question
    paraphrased_dict = json.load(open("data/input/paraphrased.json", "r"))

    full_answer_nlu_string = """
- intent: full_answer
  examples: |
    - Tell me the full answer.
    - Can you provide the full answer?
    - I need the complete answer.
    - Could you give me the full answer?
    - What is the full answer?
    - Give me the complete answer, please.
    - Please provide the full answer.
    - Can you show me the entire answer?
    - I want the full answer.
    - Could you provide the entire answer?
    - Tell me the complete answer.
    - Show me the full answer.
    - I'd like to know the full answer.
    - Can I get the full answer, please?
    - What is the entire answer?
    - Provide me with the full answer.
    - Please give me the complete answer.
    - I want to see the entire answer.
    - Would you give me the full answer?
    - Can you explain the full answer to me?
    """

    """
      nlu_list: will contains strings that package multiple questions under the same intent
      rules_list: will contain strings that map an intent to a corresponding action from chatbot (e.g. intent: ask_for_time, action: provide_time)
      domain_list: will contain strings that map a RASA action to a corresponding answer
      intent_list: will contain intent strings in yaml format
      stories_list: will contain strings that package user intents, answer summaries, full answer intents, and full answers to provide users opportunity to ask for larger answer
    """
    full_answer_intent_string = get_intent_yaml_string("full_answer")

    dna_nlu_string = get_nlu_yaml_string("Do not answer", DNA_questions["Questions"])
    dna_rule_string = get_rules_yaml_string("Do not answer")
    dna_intent_string = get_intent_yaml_string("Do not answer")
    dna_domain_string = get_domain_yaml_string(
        "Do not answer", "Sorry, I am designed not to answer such a question."
    )

    # include intents for asking for the full answer as well as intents for questions that should not be answered
    nlu_list = [full_answer_nlu_string, dna_nlu_string]
    intent_list = [full_answer_intent_string, dna_intent_string]

    # include a rule for dna which maps a user dna intent to corresponding action
    # also map that action to a dna answer in domain
    # rules(stories) and domain strings for dna full answers are handled for each question individually
    domain_list = [dna_domain_string]
    rules_list = [dna_rule_string]

    stories_list = []

    # iterate over all QA pairs in the dataframe
    # and populate the lists with corresponding yaml strings
    for i in range(len(QA_df)):
        # replace all double quotes with single quotes
        QA_df.loc[i, "Answer"] = QA_df.loc[i, "Answer"].replace('"', "'")

        intent = QA_df["Intent"][i]
        question = QA_df["Question"][i]
        answer = QA_df["Answer"][i]

        try:
            timestamp = QA_df["Timestamp"][i]
            # convert date to format
            date = datetime.fromtimestamp(timestamp).strftime("%B %Y")
        except:
            date = ""

        if "Source" in QA_df.columns:
            source = QA_df["Source"][i]
        else:
            source = ""

        # year = QA_df["Year"][i]

        # get parphrases and calculate answer length
        paraphrased_questions = paraphrased_dict[question]
        plain_text_length = get_plain_text_length(answer)

        # combines question with its paraphrases under same intent
        nlu_string = get_nlu_yaml_string(intent, [question] + paraphrased_questions)
        nlu_list.append(nlu_string)

        if plain_text_length < 140:
            # Short enough to not summarize

            # maps user intent to corresponding chatbot action
            # each intent's corresponding action is named f'utter_{intent}'
            # this action will be linked to the answer string in domain.yml
            rule_string = get_rules_yaml_string(intent)
            rules_list.append(rule_string)

            domain_string = get_domain_yaml_string(
                intent, f"[Source: {source}; Date: {date}] {answer}"
            )
            domain_list.append(domain_string)
            # if year == 2024:
            #     domain_list.append(get_domain_yaml_string(intent, f"[Source: {source}; Date: Sept, 2024] {answer}"))
            # elif year == 2022:
            #     domain_list.append(get_domain_yaml_string(intent, f"[Source: {source}; Date: Apr, 2022] {answer}"))
        else:
            # length >= 140, so we do summarize our answer
            # instead of adding the answer to rules, we add it to stories
            # providing the user the option of asking for the fuller answer
            story_string = get_stories_yaml_string(intent)
            stories_list.append(story_string)

            # maps the providing summary RASA action to answer's summary
            answer_summary = summarize(answer)
            domain_string_summary = get_domain_yaml_string(
                f"summary_{intent}", answer_summary
            )
            domain_list.append(domain_string_summary)

            # maps the providing answer RASA action to answer
            domain_string_answer = get_domain_yaml_string(
                intent, f"[Source: {source}; Date: {date}] {answer}"
            )
            domain_list.append(domain_string_answer)
            # if year == 2024:
            #     domain_list.append(get_domain_yaml_string(intent, f"[Source: {source}; Date: Sept, 2024] {answer}"))
            # elif year == 2022:
            #     domain_list.append(get_domain_yaml_string(intent, f"[Source: {source}; Date: Apr, 2022] {answer}"))

        # store user intent
        intent_list.append(get_intent_yaml_string(intent))

    domain_path = "Chatbot/domain.yml"

    write_list_to_file(nlu_list, "Chatbot/data/nlu.yml")
    write_list_to_file(rules_list, "Chatbot/data/rules.yml")
    write_list_to_file(stories_list, "Chatbot/data/stories.yml")

    # add domain_list content to domain.yml,
    # it is defined right before actions
    with open(domain_path, "r", encoding="utf-8") as f:
        domain_data = f.read()
        domain_data = domain_data.replace(
            "actions:", "".join(domain_list) + "\n\nactions:"
        )

    with open(domain_path, "w", encoding="utf-8") as f:
        f.write(domain_data)

    # add intent_list content to domain.yml
    # it is defined right before responses
    with open(domain_path, "r", encoding="utf-8") as f:
        domain_data = f.read()
        domain_data = domain_data.replace(
            "responses:", "".join(intent_list) + "\n\nresponses:"
        )

    with open(domain_path, "w", encoding="utf-8") as f:
        f.write(domain_data)


if __name__ == "__main__":
    main()
