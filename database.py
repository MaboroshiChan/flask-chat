from pymongo import MongoClient
from enum import Enum

client = MongoClient('localhost', 27017)
db = client['chatbot']
collection = db['messages']

class Feedback(Enum):
    POSITIVE = 1
    NEGATIVE = -1

# create a new document in the database
def create_document(usr_id: str, chat_id: str, messages: list[dict[str, str]], feedback: Feedback)->None:
    collection.insert_one({
        "usr_id": usr_id,
        "chat_id": chat_id,
        "messages": messages,
        "feedback": feedback
    })

# get all documents from the database
def get_documents()->list[dict[str, str]]:
    return list(collection.find())

# get all documents from the database with a specific usr_id
def get_documents_by_usr_id(usr_id: str)->list[dict[str, str]]:
    return list(collection.find({"usr_id": usr_id}))

# get all documents from the database with a specific feedback
def get_documents_by_feedback(feedback: Feedback)->list[dict[str, str]]:
    return list(collection.find({"feedback": feedback}))

# get all documents from the database with a specific chat_id and usr_id
def get_documents_by_chat_id_and_usr_id(chat_id: str, usr_id: str)->list[dict[str, str]]:
    return list(collection.find({"chat_id": chat_id, "usr_id": usr_id}))

# calculate the average feedback for a specific user_id
def get_average_feedback_by_usr_id(usr_id: str)->float:
    docs = get_documents_by_usr_id(usr_id)
    if len(docs) == 0:
        return 0
    else:
        return sum([x['feedback'] for x in docs]) / len(docs)