#mongodb+srv://root:<password>@clustertfg.9afluby.mongodb.net/?retryWrites=true&w=majority
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

