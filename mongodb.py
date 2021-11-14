import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
import random
import time
import hashlib

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

def init_blockchain(game_name, difficulty, connection, players): #user_query sends players list into this
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())
    timestamp = time.time() / 60

    db=cluster[game_name]
    #iterate through players name and give them their own version of the blockchain
    #check if the db[game_name] exists
    print(db.list_collection_names())


    for player in players:
        if db[player].count_documents({}) != 0:
            continue
        else:
            db[player].insert_one({
                            "username": player,
                            "timestamp": timestamp,
                            "block_height": 1,
                            "previous_hash": "0 0 0 0",
                            "transactions": [],
                            "last_nonce": "0 0 0 0",
                            "block_hash": "f7a6c106dd2f1b3f0931bc9333e6d8772a1b7399f07ccd8b030952c1341aab16",
                            "ledger":"0\nf7a6c106dd2f1b3f0931bc9333e6d8772a1b7399f07ccd8b030952c1341aab16"
                        })
    return True


def query_blockchain(game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["blockchain"]
    collection = db[game_name]

    return collection.find_one({})

def get_block_message_hash(game_name, username):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster[game_name]
    collection = db[username]
    block_message = collection.find_one({"username": username}, {"previous_hash": 1, "_id": 0})
    block_hash = collection.find_one({"username": username}, {"block_hash": 1, "_id": 0})
    block_height = collection.find_one({"username": username}, {"block_height": 1, "_id": 0})
    ledger = collection.find_one({"username": username}, {"ledger": 1, "_id": 0})

    return (block_message["previous_hash"], block_hash["block_hash"], block_height["block_height"], ledger["ledger"])

def add_block(game_name, from_username, to_username, previous_hash, last_nonce):

    
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())
    db=cluster[game_name]
    collection = db[from_username]

    timestamp = time.time() / 60
    block_height = collection.find_one({"username": from_username}, {"block_height": 1, "_id": 0})
    block_height = block_height["block_height"] + 1
    ledger = collection.find_one({"username": from_username}, {"ledger": 1, "_id": 0})
    ledger = ledger["ledger"]
    new_ledger = ledger + "\n" + last_nonce + "\n" + previous_hash 
    print(new_ledger)
    block_hash = hashlib.sha256(new_ledger.encode()).hexdigest()
    
    
    #get the block height of the first document

    #update first collection values
    collection.update_one(
        {"username": from_username},
        {"$set": {
            "timestamp": timestamp,
            "block_height": block_height,
            "previous_hash": previous_hash,
            "transactions": [],
            "last_nonce": last_nonce,
            "block_hash": block_hash,
            "ledger": new_ledger
        }}
    )

            
    collection = db[to_username]

    #update first collection values
    #add new document
    collection.insert_one(
        {"username": from_username,
        "timestamp": timestamp,
        "block_height": block_height,
        "previous_hash": previous_hash,
        "transactions": [],
        "last_nonce": last_nonce,
        "block_hash": block_hash,
        "ledger": new_ledger
        }
    )

    return (new_ledger, block_hash, block_height)


"============================================================================"
#update a players bitcoin balance
def update_balance(game_name, username, amount):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    collection.update_one({"username": username}, {"$inc": {"balance": amount}})
    return 

"============================================================================"
#takes all the players and determines a random pick
def pick_next(game_name, username):
    players = user_query(game_name)
    players = [i for i in players if i != username]
    chosen = random.choice(tuple(players))

    return chosen


def current_block(game_name, username):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster[game_name]
    collection = db[username]

    #print the first document in the collection
    
    block = collection.find_one({})

    return block

def new_block_requests(game_name, username):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = cluster[game_name]
    collection = db[username]
    #return all the documents in the collection in order
    blocks = list(collection.find({}))
    requests = blocks[1:]

    heights = []
    block_hashes = []
    block_ids = []
    for request in requests:
        print(request)
        #grab the value of the block height in the dictionary
        id = request["_id"]
        block_ids.append(id)
        block_height = request["block_height"]
        print(type(block_height))
        heights.append(block_height)
        block_hashes.append(request["block_hash"])
    
    return (heights, block_hashes, block_ids)
    
    
def remove_block(game_name, username, id):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = cluster[game_name]
    collection = db[username]
    #delete the first document in the collection
    #print the block with matching id
    collection.delete_one({"_id": ObjectId(id)})
    return

def accept_block(game_name, username, id):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = cluster[game_name]
    collection = db[username]
   
    block = collection.find_one({"_id": ObjectId(id)})
    #grab the block_height, previous_hash, last_nonce, block_hash, and ledger
    block_height = block["block_height"]
    previous_hash = block["previous_hash"]
    last_nonce = block["last_nonce"]
    block_hash = block["block_hash"]
    ledger = block["ledger"]

    #update the block 
    collection.update_one(
                {"username": username}, 
                {"$set": {
                            "block_height": block_height, 
                            "previous_hash": previous_hash, 
                            "last_nonce": last_nonce, 
                            "block_hash": block_hash, 
                            "ledger": ledger}})
    

    return

#print(game_info_query("test"))
#print(user_query("test"))
#print(balance_query("thomas", "test"))
#print(query_blockchain("test"))

#print(balance_query("thomas", "test"))
#print(update_balance("test","thomas", 5))
#print(balance_query("thomas", "test"))
#print(pick_next("test", "thomas"))

#print(get_block_message_hash("test", "thomas")[3])
#print(new_block_requests("test", "thomas1"))

