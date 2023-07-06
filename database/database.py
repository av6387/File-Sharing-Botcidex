#(©)CodeXBotz
#(©)VysakhTG

import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']
group_data = database['groups']
delay_data = database['delay']


async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)


async def add_group(id):
    data = group_data.find_one({'id':int(id)})
    if data:
        return
    group_data.insert_one({'id': int(id)})
    return

async def total_chat_count():
    count = group_data.count_documents({})
    return count

async def get_all_chats():
    return group_data.find({})

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return
