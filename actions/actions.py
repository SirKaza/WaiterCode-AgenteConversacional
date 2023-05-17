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
# from utils.database_connect import dataUp
# from ..utils.database_connect import dataUp
# from utils.mongodatabase import dataUp
import pymongo
from pymongo import MongoClient
twoDigits = ["Q10_ANS", "Q11_ANS", "Q12_ANS", "Q13_ANS", "Q14_ANS", "Q15_ANS", "Q16_ANS"]
#cluster = MongoClient("mongodb+srv://root:root@clustertfg.9afluby.mongodb.net/?retryWrites=true&w=majority") #anterior tfg
cluster = MongoClient("mongodb+srv://marccasanova:rNDivjwxbCn8cU5F@cluster0.gi4mjq0.mongodb.net/?retryWrites=true&w=majority")
db = cluster["rasa"]
collection = db["test"]
#This function stores user's answers into the database
def dataUp(sender, message, column):
    issender = list(collection.find({"sender": "{}".format(sender)}))
    #If the sender does not exist, then we create a new row and initialize everything
    if len(issender) == 0:
        post = {"sender": "{}".format(sender), "q1": "{}".format(message),
                "q2": "q2:null", "q3": "q3:null",
                "q5": "q5:null", "q6": "q6:null", "q7": "q7:null", "q8": "q8:null",
                "q9": "q9:null", "q10": "q10:null", "q11": "q11:null", "q12": "q12:null",
                "q13": "q13:null",
                "q14": "q14:null", "q15": "q15:null", "q16": "q16:null"
                }
        collection.insert_one(post)
    # If the sender does exist, then we use update function to store the answer into the correspondent column

    else:
        final = column + ":" + message
        collection.update_one({"sender": "{}".format(sender)},
                              {"$set": {"{}".format(column): "{}".format(final)}})

#This custom action takes care of the db query.
class ActionDb(Action):
    def name(self) -> Text:
        return "action_db"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        usertext = tracker.latest_message['text'].lower()
        intentname= tracker.latest_message['intent'].get('name')
        sender = tracker.sender_id
        #here we slice the user's message, "qx + user's input", and extract the internal command "qx " and the input "user's input"
        if (intentname in twoDigits):
            #Realtext is the user's input
            realtext = usertext[4:]
            # Column is the internal command that also matches with the columns of the db
            colum = usertext[:3]
            #Call the function to perform db queries
            dataUp(sender, realtext, colum)
        else:
            realtext = usertext[3:]
            colum = usertext[:2]
            dataUp(sender, realtext, colum)
        #If the user answers negatively, then we try consolate the user
        if ("not at all" in realtext or "slightly" in realtext or "moderately" in realtext):
            dispatcher.utter_message(response="utter_negative_reply")
        # If the user answers positively, then we express our happiness to the user
        if ("fairly" in realtext or "extremely" in realtext):
            dispatcher.utter_message(response="utter_positive_reply")
        # If the user meant to skip, then we say don't worry
        if ("skip" in realtext):
            dispatcher.utter_message(response="utter_dont_worry")
        # As long as the questions of the GEQ are not answered, we send an introduction of the likert-scale used in this project
        if (tracker.latest_message['intent'].get('name') != "Q14_ANS"):
            dispatcher.utter_message(response="utter_introduction")

'''
class ActionDbTwoDigits(Action):
    def name(self) -> Text:
        return "action_db_two_digits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        usertext = tracker.latest_message['text'].lower()
        sender = tracker.sender_id
        realtext = usertext[4:]
        colum = usertext[:3]
        dataUp(sender, realtext, colum)
        if ("not at all" in realtext or "slightly" in realtext or "moderately" in realtext):
            dispatcher.utter_message(response="utter_negative_reply")

        if ("fairly" in realtext or "extremely" in realtext):
            dispatcher.utter_message(response="utter_positive_reply")
        if ("skip" in realtext):
            dispatcher.utter_message(response="utter_dont_worry")
        if (tracker.latest_message['intent'].get('name') != "Q14_ANS"):
            dispatcher.utter_message(response="utter_introduction")

'''

#this function handles the last two open questions.
class ActionOpenQuestion(Action):
    def name(self) -> Text:
        return "action_open_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        usertext = tracker.latest_message['text'].lower()
        intentname = tracker.latest_message['intent'].get('name')
        sender = tracker.sender_id
        if (intentname == "Q15_ANS"):
            realtext = usertext[8:]
            colum = usertext[:3]
            dataUp(sender, realtext, colum)
            dispatcher.utter_message(response="utter_q16")
        if (intentname == "Q16_ANS"):
            realtext = usertext[8:]
            colum = usertext[:3]
            dataUp(sender, realtext, colum)
            dispatcher.utter_message(response="utter_end")


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
        dispatcher.utter_message(text="Now is: " + current_time)
        return []

''' 
The reminder actions was implemented for timeout condition, but unfortunaly it does not work in VR environment
class ActionSetReminder(Action):

    def name(self) -> Text:
        return "action_schedule_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #
        date = datetime.now() + timedelta(seconds=10)
        reminder = ReminderScheduled(
            "EXTERNAL_reminder",
            trigger_date_time=date,
            name="my_reminder",
            kill_on_user_message=False,
        )
        # dispatcher.utter_message(text="Now is: " + current_time)

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
'''