from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
tokenizer = AutoTokenizer.from_pretrained("prithivida/parrot_paraphraser_on_T5")
model = AutoModelForSeq2SeqLM.from_pretrained("prithivida/parrot_paraphraser_on_T5")

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import json

#Init models (make sure you init ONLY once if you integrate this to your code)
# parrot = Parrot()

# phrases is a list of strings to paraphrase
def paraphraser(phrases):
  return_list = []
  for phrase in phrases:
    temp = []
    # print("-"*100)
    # print("Input_phrase: ", phrase)
    # print("-"*100)
    input_ids = tokenizer(phrase, return_tensors="pt").input_ids
    generated_ids = model.generate(input_ids, max_length=100, num_beams=10, early_stopping=True, top_p= 0.99,
                                  top_k = 30, num_return_sequences=6)
    for i in range(len(generated_ids)):
      temp.append(tokenizer.decode(generated_ids[i], skip_special_tokens=True))
    
    return_list.append(temp)
  
  return return_list


QA_df = pd.read_csv('data/input/Chat_intent.csv')
question_list = QA_df['Question'].tolist()
paraphrased_list = paraphraser(question_list)
for i in range(len(paraphrased_list)):
  for k in paraphrased_list[i]:
    if k in question_list:
      paraphrased_list[i].remove(k)
      paraphrased_list[i] = list(set(paraphrased_list[i]))

# for i in range(len(paraphrased_list)):
#   print("Question: ", question_list[i])
#   print("Paraphrased: ", paraphrased_list[i])
#   print(len(paraphrased_list[i]))
#   print("-"*100)

dict_paraphrased = {}
for i in range(len(question_list)):
  dict_paraphrased[question_list[i]] = paraphrased_list[i]
# save to json file
object = json.dumps(dict_paraphrased, indent = 4)
with open('data/input/paraphrased.json', 'w') as f:
  f.write(object)