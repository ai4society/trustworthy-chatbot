import pandas as pd
import os
import shutil

if os.path.exists('Chatbot'):
    shutil.rmtree('Chatbot', ignore_errors=True, onerror=None)

shutil.copytree('rasa_template', 'Chatbot')

nlu_path = 'Chatbot/data/nlu.yml'
rules_path = 'Chatbot/data/rules.yml'
domain_path = 'Chatbot/domain.yml'

intent_data_path = 'data/input/Chat_intent.csv'

QA_df = pd.read_csv(intent_data_path)

def add_nlu_data(intent, question):
    nlu_data = f"""
- intent: {intent}
  examples: |
    - {question}
    """
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
    nlu_list.append(add_nlu_data(QA_df['Intent'][i], QA_df['Question'][i]))
    rules_list.append(add_rules_data(QA_df['Intent'][i]))   
    domain_list.append(add_domain_data(QA_df['Intent'][i], QA_df['Answer'][i]))
    intnet_list.append(add_intents_to_domain(QA_df['Intent'][i]))
    
# add nlu_list content to nlu.yml
with open(nlu_path, 'a') as f:
    f.write('\n')
    for item in nlu_list:
        f.write(item)

with open(rules_path, 'a') as f:
    f.write('\n')
    for item in rules_list:
        f.write(item)
        
# add domain_list content to domain.yml before session_config:
with open(domain_path, 'r') as f:
    domain_data = f.read()
    domain_data = domain_data.replace('session_config:', ''.join(domain_list) + '\nsession_config:')

with open(domain_path, 'w') as f:
    f.write(domain_data)

# add intent_list content to domain.yml before responses:
with open(domain_path, 'r') as f:
    domain_data = f.read()
    domain_data = domain_data.replace('responses:', ''.join(intnet_list) + '\n\nresponses:')

with open(domain_path, 'w') as f:
    f.write(domain_data)

    