# revised g0

from typing import Any, Text, Dict, List, Union, Optional

import rasa.core.tracker_store
from rasa.shared.core.trackers import DialogueStateTracker
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
from datetime import datetime, timezone, timedelta
#import panda as pd


class ActionSaveConversation(Action):

    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #now = datetime.now()
        #input_time = now.strftime("%H:%M:%S")
        
        conversation_id = str(tracker.sender_id)
        conversation = tracker.events
        #input_str_u = tracker.latest_message.get('text')
         
        count_u = 0
        count_b = 0
        # print(conversation)
        import os
        if not os.path.isfile('chats.csv'):
            with open('chats.csv','w') as file:
                file.write("input_time|conversation_id|count|intent|user_input| entity_name|entity_value|action|bot_reply|\n")
        chat_data=''
        for i in conversation:
            now = datetime.now()
            input_time = now.astimezone(timezone(timedelta(hours=-4))).strftime('%Y-%m-%d %H:%M:%S.%f')
            if i['event'] == 'user':
               str_count_u = 'U'+str(count_u)
               chat_data+= input_time+'|' + conversation_id + '|' + str_count_u+'|' +i['parse_data']['intent']['name']+'|' + i['text'] +'|' + '\n'
               count_u = count_u+ 1
               print('user: {}'.format(i['text']))
               if len(i['parse_data']['entities']) > 0:
                    chat_data += i['parse_data']['entities'][0]['entity']+'|'+i['parse_data']['entities'][0]['value']+'|'
                    print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
                          i['parse_data']['entities'][0]['value'])
               else:
                    chat_data+=""
            elif i['event'] == 'bot':
                str_count_b = 'B'+str(count_b)
                print('Bot: {}'.format(i['text']))
                try:
                    chat_data+=input_time+'|' + conversation_id + '|' + str_count_b+'|' +'|'+'|' + '|' +'|' + i['metadata']['utter_action']+'|'+ i['text'] + '\n'
                    count_b = count_b+ 1
                except KeyError:
                    pass
        else:
            with open('chats.csv','a') as file:
                file.write(chat_data)

        dispatcher.utter_message(text="")
        

        return []

class ActionSessionId(Action):
    def name(self) -> Text:
        return "action_session_id"

    async def run(
    self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        conversation_id=tracker.sender_id
        dispatcher.utter_message("The conversation id is {}".format(conversation_id))
        return []
