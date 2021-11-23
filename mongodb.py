import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
import random
import time
import hashlib
import numpy as np

from mongdb_connectionstring import connection_string
"============================================================================"

def random_matrix_connection(n_users,connection_quality, users_list): #randomly generate a matrix of connections between users using numpy
    import numpy as np
    user_dict ={}
    matrix = np.random.rand(n_users,n_users)
    count = 0
    for i in range(n_users):
        for j in range(n_users):
            if i == j:
                matrix[i][j] = 2
            else:
                if matrix[i][j] > (1 - connection_quality) * (1 + 1 / float(n_users)):
                    matrix[i][j] = 1
                    count += 1
                else:
                    matrix[i][j] = 0
    for k in range(0,len(matrix.tolist())):
        for h in range(len(matrix[k])):
            if matrix[k][h] == 2.0:
                pass
            if matrix[k][h] == 1.0:
                if users_list[k] in user_dict:
                    user_dict[users_list[k]].append(users_list[h])
                else:
                    user_dict[users_list[k]] = [users_list[h]]
    print(matrix.astype(int))
    return user_dict

#print(random_matrix_connection(10,0.5,['a','b','c','d','e','f','g','h','i','j']))

#matrix = (random_matrix_connection(10,0.5,['a','b','c','d','e','f','g','h','i','j']))
#print(matrix['a'])
#simulate the network on the blockchain

#connected_players = random_matrix_connection(5, 1, ['thomas1', 'thaosm1','dasda','asgaga','awtqwtq'])
#print(connected_players['thomas1'])

def add_connections_to_db(game_name, connected_players, players):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    for i in range(len(players)): 
        #update the connected_to field in the db with the connected players
        collection.update_one({"username": players[i]}, {"$set": {"connected_to": connected_players[players[i]]}})
    

#add_connections_to_db("test", connected_players, ['thomas1', 'thaosm1'])
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
                                "connection": connection,
                                "ready": False,
                                "game": False, #game in session?
                                "connected_to": [],
                                })
        return ("added " + username)

def game_status(game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    game_status = collection.find_one({"game_name": game_name}, {"game": 1, "_id": 0})
    return game_status["game"]

def game_start(game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    collection.update_many({"game": False}, {"$set": {"game": True}})
    return "game started"


def all_ready(game_name): #checks if every player in the game is ready
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    ready_states = list(collection.find({}, {"ready": 1, "_id": 0}))
    ready_states = list(map(lambda x: x["ready"], ready_states))
    if all(ready_states):
        return True
    else:
        return False

#print(all_ready("test"))
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
                            "connection": connection,
                            "ready": False,
                            "game": False, #game in session?
                            "connected_to": [], 
                            })

    return ("added " + username)

"============================================================================"

def user_query(game_name):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    # query "names" field into a list
    names = list(collection.find({}, {"username": 1, "_id": 0}))
    names = list(map(lambda x: x["username"], names))

    ready_states = list(collection.find({}, {"ready": 1, "_id": 0}))
    ready_states = list(map(lambda x: x["ready"], ready_states))

    return (names, ready_states)

#print(user_query("test")[0])

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

def set_ready(game_name, player):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    collection.update_one({"username": player}, {"$set": {"ready": True}})
    return True

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
                            "ledger":"0 0 0 0\nf7a6c106dd2f1b3f0931bc9333e6d8772a1b7399f07ccd8b030952c1341aab16"
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

def add_block(game_name, from_username, to_username:list, previous_hash, last_nonce):

    
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())
    db=cluster[game_name]
    collection = db[from_username]

    timestamp = time.time() / 60
    block_height = collection.find_one({"username": from_username}, {"block_height": 1, "_id": 0})
    block_height = block_height["block_height"] + 1
    ledger = collection.find_one({"username": from_username}, {"ledger": 1, "_id": 0})
    ledger = ledger["ledger"]
    ledger = ledger + "\n" + last_nonce  + "\n" + previous_hash + "\n" + "[" + from_username + " + found nonce" + "]"
    #print(new_ledger)
    block_hash = hashlib.sha256(ledger.encode()).hexdigest()
    new_ledger = ledger + "\n" + block_hash + "\n -----------------------------------------------------"

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
    
    for i in range(len(to_username)):

        collection = db[to_username[i]]
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

    return (previous_hash, block_hash, block_height, new_ledger)


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
def find_connected_players(game_name, username):
    #find connected to field in the game_database
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster["game_database"]
    collection = db[game_name]
    connected_players = collection.find_one({"username": username}, {"connected_to": 1, "_id": 0})
    connected_players = connected_players["connected_to"]
    return connected_players

#print(find_connected_players("test", "thoams"))


def current_block(game_name, username):
    cluster = MongoClient(connection_string, tlsCAFile=certifi.where())

    db=cluster[game_name]
    collection = db[username]

    #print the first document in the collection
    
    block = collection.find_one({"username": username})
    blockchain_message = block["previous_hash"]
    block_hash = block["block_hash"]
    block_height = block["block_height"]
    ledger = block["ledger"]

    return (blockchain_message, block_hash, block_height, ledger)

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
    ledgers = []
    for request in requests:
        #print(request)
        #grab the value of the block height in the dictionary
        id = request["_id"]
        block_ids.append(id)
        block_height = request["block_height"]
        #print(type(block_height))
        heights.append(block_height)
        block_hashes.append(request["block_hash"])
        ledger = request["ledger"]
        ledgers.append(ledger)

    
    return (heights, block_hashes, block_ids, ledgers)
    
    
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

#print(current_block("test1", "thomas"))