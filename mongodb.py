import pymongo
from pymongo import MongoClient
import certifi

from mongdb_connectionstring import connection_string

"============================================================================"

def game_creation(username, game_name):
    """
    This function creates a new game in the database.
    """
    # if the db already exists, then we can just connect to it
    
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db = cluster["game_database"]
    
    collection = db[game_name]
    collection.insert_one({
                            "game_name": game_name, 
                            "username": username,
                            "balance": 5,})
    return False

"============================================================================"

def game_join(username, game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db = cluster["game_database"]
    # check if db[game_name] exists
    if db[game_name].count_documents({}) != 0:
        return True
    else:
        return False

def add_name(username, game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    collection.insert_one({
                            "game_name": game_name, 
                            "username": username,
                            "balance": 5,})

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
#print(user_query("test"))
#print(balance_query("thomas", "test"))