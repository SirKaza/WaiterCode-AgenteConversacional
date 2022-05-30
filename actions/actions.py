# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from utils.database_connect import dataUp

class ActionDb(Action):
    def name(self) -> Text:
        return "action_db"
    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            usertext = tracker.latest_message['text']
            #intentname= tracker.latest_message['intent'].get('name')
            sender = tracker.sender_id

            #dispatcher.utter_message(text="Hello World!")
            #if (intentname == "q1"):
            realtext = usertext[3:]
            #sql='INSERT INTO test.user (q1) VALUES ("{0}");'.format(realtext) 
            colum  = usertext[:2]
            dataUp(sender, realtext, colum)
            if (realtext=="not at all" or realtext=="slightly" or realtext=="moderately"):
                dispatcher.utter_message(response="utter_negative_reply")
            
            if (realtext == "fairly" or realtext == "extremely"):
                dispatcher.utter_message(response="utter_positive_reply")
            
            dispatcher.utter_message(response="utter_introduction")
class ActionDbTwoDigits(Action):
    def name(self) -> Text:
        return "action_db_two_digits"
    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            usertext = tracker.latest_message['text']
            sender = tracker.sender_id
            realtext = usertext[4:]
            colum  = usertext[:3]
            dataUp(sender, realtext, colum)
            if (realtext=="not at all" or realtext=="slightly" or realtext=="moderately"):
                dispatcher.utter_message(response="utter_negative_reply")
            
            if (realtext == "fairly" or realtext == "extremely"):
                dispatcher.utter_message(response="utter_positive_reply")
            if (tracker.latest_message['intent'].get('name') != "Q14_ANS"):
                dispatcher.utter_message(response="utter_introduction")
            
class ActionOpenQuestion(Action):
    def name(self) -> Text:
        return "action_open_question"
    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            usertext = tracker.latest_message['text']
            intentname= tracker.latest_message['intent'].get('name')
            sender = tracker.sender_id
            if (intentname == "Q15_ANS"):
                realtext = usertext[8:]
                colum  = usertext[:3]
                dataUp(sender, realtext, colum)
                dispatcher.utter_message(response="utter_q16")
            if (intentname == "Q16_ANS"):
                realtext = usertext[8:]
                colum  = usertext[:3]
                dataUp(sender, realtext, colum)
                dispatcher.utter_message(response="utter_end")
                #dataUp(sender, "hello", "mood_great")
                #dispatcher.utter_message(text="I felt challenged")
                #dispatcher.utter_message(response=)
'''
class ActionHelloWorld(Action):

      def name(self) -> Text:
          return "action_hello_world"
 
      def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
  
          dispatcher.utter_message(text="Hello World!")
          return []
'''
'''
class ActionSubmitSuggestionForm(Action):
    def name(self) -> Text:
        return "action_submit_suggestion_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        dispatcher.utter_message(template="utter_end")
        return []

class ActionTest(Action):

      def name(self) -> Text:
          return "action_test"
 
      def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
  
          dispatcher.utter_message(text="Hello World!")
          return []
'''
from datetime import datetime
class ActionWhatTime(Action):

      def name(self) -> Text:
          return "action_what_time"
 
      def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              #
              now = datetime.now()
              current_time = now.strftime("%H:%M:%S")
              dispatcher.utter_message(text="Now is: "+current_time)
              return []
