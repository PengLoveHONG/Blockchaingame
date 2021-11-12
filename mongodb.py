import pymongo
from pymongo import MongoClient
import certifi
import time

from mongdb_connectionstring import connection_string

"============================================================================"

def game_creation(username, game_name, difficulty, connection):
    """
    This function creates a new game in the database.
    """
    # if the db already exists, then we can just connect to it
    
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db = cluster["game_database"]
    #check if db[game_name] exists
    if db[game_name].count_documents({}) != 0:
        return False
    else:
        collection = db[game_name]
        collection.insert_one({
                                "game_name": game_name, 
                                "username": username,
                                "balance": 5,
                                "difficulty": difficulty,
                                "connection": connection,})
        return ("added " + username)

"============================================================================"

def game_join(username, game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db = cluster["game_database"]
    # check if db[game_name] exists
    if db[game_name].count_documents({}) != 0:
        return True
    else:
        return False

def add_name(username, game_name, difficulty, connection):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    collection.insert_one({
                            "game_name": game_name, 
                            "username": username,
                            "balance": 5,
                            "difficulty": difficulty,
                            "connection": connection,})

    return ("added " + username)

"============================================================================"

def user_query(game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    # query "names" field into a list
    names = list(collection.find({}, {"username": 1, "_id": 0}))
    return (list(map(lambda x: x["username"], names)))


def balance_query(username, game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    balance = collection.find_one({"username": username}, {"balance": 1, "_id": 0})
    return balance["balance"]

"============================================================================"

def game_info_query(game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    difficulty = collection.find_one({"game_name": game_name}, {"difficulty": 1, "_id": 0})
    connection = collection.find_one({"game_name": game_name}, {"connection": 1, "_id": 0})
    return (difficulty["difficulty"], connection["connection"])

"============================================================================"

def init_blockchain(game_name, difficulty, connection):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())
    timestamp = time.time() / 60

    db=cluster["blockchain"]
    collection = db[game_name]
    collection.insert_one({
                    "blockchain_message": "0 0 0 0", 
                    "blockchain_hash": "f7a6c106dd2f1b3f0931bc9333e6d8772a1b7399f07ccd8b030952c1341aab16",
                    "timestamp": timestamp,
                    "previous_hash": "0 0 0 0",
                    "difficulty": difficulty,
                    "connection": connection,
                    "nonce_count": 0}

                    )
    return True

def query_blockchain(game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["blockchain"]
    collection = db[game_name]

    return collection.find_one({})

#print(game_info_query("test"))
#print(user_query("test"))
#print(balance_query("thomas", "test"))
#print(query_blockchain("test"))
#print time

