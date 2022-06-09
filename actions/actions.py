# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ReminderScheduled, ReminderCancelled
#from utils.database_connect import dataUp
#from ..utils.database_connect import dataUp
#from utils.database_connect import dataUp
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://root:root@clustertfg.9afluby.mongodb.net/?retryWrites=true&w=majority")
db = cluster["rasa"]
collection = db["test"]
#results = list(collection.find({"q1":"q14:null"}))

#print(result["q1"])

def dataUp(sender, message, column):

        #sender = "test"
        '''
        post = {"sender":"{}".format(sender),"q1".format(column):"{}".format(message),"q2":"q2:null","q3":"q3:null",
                "q5":"q5:null","q6":"q6:null","q7":"q7:null","q8":"q8:null",
                "q9":"q9:null","q10":"q10:null","q11":"q11:null","q12":"q12:null","q13":"q13:null",
                "q14":"q14:null","q15":"q15:null","q16":"q16:null"
                }
        '''
        issender = list(collection.find({"sender": "{}".format(sender)}))
        if len(issender) == 0:
                #if (column == "q1"):
                        # result = list(collection.find({"q1": "q1:null"})[0]["q1"])
                        #results = list(collection.find({"q1": "q1:null"}))
                        # first time insert
                        #if len(results) == 0:
                post = {"sender": "{}".format(sender), "q1": "{}".format(message),
                        "q2": "q2:null", "q3": "q3:null",
                        "q5": "q5:null", "q6": "q6:null", "q7": "q7:null", "q8": "q8:null",
                        "q9": "q9:null", "q10": "q10:null", "q11": "q11:null", "q12": "q12:null",
                        "q13": "q13:null",
                        "q14": "q14:null", "q15": "q15:null", "q16": "q16:null"
                        }
                collection.insert_one(post)
                        # not first time, then update
                       # else:
                       #         collection.update_one({"sender": "{}".format(sender)},
                        #                              {"$set": {"{}".format(column): "{}".format(message)}})
        else:
                final = column + ":" + message
                collection.update_one({"sender": "{}".format(sender)},
                                      {"$set": {"{}".format(column): "{}".format(final)}})
class ActionDb(Action):
    def name(self) -> Text:
        return "action_db"
    def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            usertext = tracker.latest_message['text']
            #intentname= tracker.latest_message['intent'].get('name')
            sender = tracker.sender_id

            realtext = usertext[3:].lower()
            colum  = usertext[:2].lower()
            dataUp(sender, realtext, colum)
            if ("not at all" in realtext or "slightly" in realtext or "moderately" in realtext):
                dispatcher.utter_message(response="utter_negative_reply")
            
            if ("fairly" in realtext or "extremely" in realtext):
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
            if ("not at all" in realtext or "slightly" in realtext or "moderately" in realtext):
                dispatcher.utter_message(response="utter_negative_reply")
            
            if ("fairly" in realtext or "extremely" in realtext):
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
from datetime import datetime, timedelta
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





class ActionSetReminder(Action):

    def name(self) -> Text:
        return "action_schedule_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #
        date = datetime.now()+timedelta(seconds=10)
        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            name="my_reminder",
            kill_on_user_message=False,
        )
        #dispatcher.utter_message(text="Now is: " + current_time)

        return [reminder]
class ActionReactToReminder(Action):

    def name(self) -> Text:
        return "action_react_to_reminder"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("triggered")
        dispatcher.utter_message(text="works")

        return []
class ForgetReminders(Action):
    """Cancels all reminders."""

    def name(self) -> Text:
        return "action_forget_reminders"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        print("cancelled")

        # Cancel all reminders
        return [ReminderCancelled()]