import pandas as pd
import os
import shutil
import json

if os.path.exists('Chatbot'):
    shutil.rmtree('Chatbot', ignore_errors=True, onerror=None)

shutil.copytree('rasa_template', 'Chatbot')

nlu_path = 'Chatbot/data/nlu.yml'
rules_path = 'Chatbot/data/rules.yml'
domain_path = 'Chatbot/domain.yml'

intent_data_path = 'data/input/Chat_intent.csv'

QA_df = pd.read_csv(intent_data_path)
paraphrased_dict = json.load(open('data/input/paraphrased.json', 'r'))
DNA_questions = pd.read_csv('data/input/DNA.csv')

def add_nlu_data(intent, question, paraphrased_list):
    nlu_data = f"""
- intent: {intent}
  examples: |
    - {question}"""
    
    for paraphrased in paraphrased_list:
        nlu_data += f"""
    - {paraphrased}"""
    return nlu_data

def add_rules_data(intent):
    rules_data = f"""
- rule: Answer {intent}
  steps:
  - intent: {intent}
  - action: utter_{intent}
    """
    return rules_data

def add_domain_data(intent, answer):
    domain_data = f"""
  utter_{intent}:
  - text: "{answer}"
    """
    return domain_data

def add_intents_to_domain(intent):
    domain_data = f"""
  - {intent}"""
    return domain_data

nlu_list = []
rules_list = []
domain_list = []
intnet_list = []
for i in range(len(QA_df)):
    nlu_list.append(add_nlu_data(QA_df['Intent'][i], QA_df['Question'][i], paraphrased_dict[QA_df['Question'][i]]))
    rules_list.append(add_rules_data(QA_df['Intent'][i]))   
    domain_list.append(add_domain_data(QA_df['Intent'][i], QA_df['Answer'][i]))
    intnet_list.append(add_intents_to_domain(QA_df['Intent'][i]))

nlu_list.append(add_nlu_data('Do not answer', DNA_questions['Questions'][0], DNA_questions['Questions'][1:]))
rules_list.append(add_rules_data('Do not answer'))   
domain_list.append(add_domain_data('Do not answer', 'Sorry, I am not able to answer this question.'))
intnet_list.append(add_intents_to_domain('Do not answer'))

# add nlu_list content to nlu.yml
with open(nlu_path, 'a') as f:
    f.write('\n')
    for item in nlu_list:
        f.write(item)

with open(rules_path, 'a') as f:
    f.write('\n')
    for item in rules_list:
        f.write(item)
        
# add domain_list content to domain.yml before actions:
with open(domain_path, 'r') as f:
    domain_data = f.read()
    domain_data = domain_data.replace('actions:', ''.join(domain_list) + '\n\nactions:')

with open(domain_path, 'w') as f:
    f.write(domain_data)

# add intent_list content to domain.yml before responses:
with open(domain_path, 'r') as f:
    domain_data = f.read()
    domain_data = domain_data.replace('responses:', ''.join(intnet_list) + '\n\nresponses:')

with open(domain_path, 'w') as f:
    f.write(domain_data)

    