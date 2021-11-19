from flask import Flask, render_template, redirect, url_for, request, jsonify
from werkzeug.utils import redirect
import pymongo
from pymongo import MongoClient
import certifi

from mongdb_connectionstring import connection_string
from mongodb import (game_creation, game_join, query_blockchain, 
                    user_query, balance_query, add_name, 
                    game_info_query, init_blockchain, update_balance, 
                    get_block_message_hash, pick_next, current_block, 
                    add_block, new_block_requests, remove_block,
                    accept_block)

#REMEMBER TO MAKE A REQUIREMENTS.TXT FILE

application = Flask(__name__)

@application.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')

@application.route('/play', methods=["POST", "GET"])
def play():
    error=""

    if request.method == "POST":
        username = request.form['username']

        game_name_create = "NA" #initialize to fill
        game_name_join = "NA"
        
        """if (connection == "Select network connection level"):
            error = "Please select a network connection level"
            return render_template('play.html', error=error)

        if (difficulty == "Select difficulty level"):
            error = "Please select a difficulty level"
            return render_template('play.html', error=error)"""

        try:
            game_name_create = request.form['GameNameCreate']
        except:
            game_name_join = request.form['GameNameJoin']

        if game_name_create != "NA":
            difficulty = request.form['difficulty']
            connection = request.form['connection']
            connection_slider = request.form['slider']
            if (game_creation(username, game_name_create, difficulty, connection) == False):
                error = "Game name already exists"
                return render_template('play.html', error=error)
            else:
                game_creation(username, game_name_create, difficulty, connection)
                return redirect(url_for('lobby', game_name=game_name_create, username=username, difficulty=difficulty, connection=connection, connection_slider=connection_slider))
        
        if game_name_join != "NA":
            if game_join(username, game_name_join) == False: #adds name to db
                return render_template('play.html', error="Game does not exist")
            else:
                if (username in user_query(game_name_join)):
                    return render_template('play.html', error="Username has been taken")
                else:
                    difficulty = game_info_query(game_name_join)[0]
                    connection = game_info_query(game_name_join)[1]
                    #query the connection_slider value

                    add_name(username, game_name_join, difficulty, connection)
                    return redirect(url_for('lobby', game_name=game_name_join, username=username, difficulty=difficulty, connection=connection))

        else:
            return render_template('play.html')
    else:
        return render_template('play.html', error=error)
    


@application.route('/lobby/<game_name>/<username>/<difficulty>/<connection>/<connection_slider>', methods=["POST", "GET"]) #CREATE A FUNCTION THAT ALTERS THE USERNAME URL SO PEOPLE CANNOT ENTER OTHERS GAME BY NAME
def lobby(game_name, username, difficulty, connection, connection_slider):
    list_of_players = user_query(game_name)
    return render_template('lobby.html', username=username, game_name=game_name, list_of_players=list_of_players, difficulty=difficulty, connection=connection, connection_slider=connection_slider)
    

@application.route('/game/<game_name>/<username>', methods=["POST", "GET"])
def game(game_name, username):
    #function to add user to game cluster
    #each player has their own blockchain ledger
    
    #this is where the matrix player algo is created
    #WHEN THE START BUTTON IS CALLED, EVERYONE SHOULD START AT SAME TIME, or it should be a vote sys
    #Do a ready feature, so the names on the lobby change color


    balance = balance_query(username, game_name)
    players=user_query(game_name)
    query=game_info_query(game_name) #[0] is difficulty, [1] is connection
    difficulty=query[0]
    connection=query[1]
    init_blockchain(game_name, difficulty, connection, players)
    block = get_block_message_hash(game_name, username)
    blockchain_message = block[0]
    blockchain_hash = block[1]
    blockchain_height = block[2]
    ledger = block[3]
    


    if difficulty == "two":
        difficulty_num = "00"
    elif difficulty == "one":
        difficulty_num = "0"
    elif difficulty == "three":
        difficulty_num = "000"
    elif difficulty == "four":
        difficulty_num = "0000"


    #create the genesis block, add it to the database, everyone in the game is ajax querying the blockchain database and beginning the sha hash

    return render_template('game.html', 
                            username=username, 
                            game_name=game_name, 
                            balance=balance, 
                            difficulty=difficulty, 
                            connection=connection,
                            blockchain_message=blockchain_message,
                            blockchain_hash=blockchain_hash,
                            difficulty_num=difficulty_num,
                            blockchain_height=blockchain_height,
                            ledger = ledger
                            )
                            



"========================================|   API   |=========================================="

@application.route("/api_players/<game_name>", methods=["POST"]) #api to get the players in a game for ajax
def players_api(game_name):
    list_of_players = user_query(game_name)
    return jsonify("", render_template("lobby_component.html", game_name=game_name, list_of_players=list_of_players))

@application.route("/api_num_players/<game_name>", methods=["POST"]) #api to get the number of players in a game for ajax):
def num_players_api(game_name):
    list_of_players = (user_query(game_name))
    return jsonify("", render_template("playercount_component.html", list_of_players=list_of_players))

@application.route("/api_updatebalance/<game_name>/<username>", methods=["POST"]) #api to update the balance for ajax
def update_balance_api(game_name, username):
    update_balance(game_name, username, 5)
    balance = balance_query(username, game_name)
    return jsonify("", render_template("balance_component.html", balance=balance))

@application.route("/api_blockchain/<game_name>/<username>", methods=["POST"]) #api to get the blockchain for ajax
def block_api(game_name, username):
    block = current_block(game_name, username)
    return jsonify("", render_template("block_component.html", block=block))

@application.route("/api_addblockchain/<game_name>/<username>/<hashvalue>/<nonce>", methods=["POST"]) #api to add to the blockchain for ajax
def add_block_api(game_name, username, hashvalue, nonce):

    next_player = pick_next(game_name, username)
    message_hash = add_block(game_name, username, next_player, hashvalue, nonce)#calculates the new hash based on ledger and adds to next player

    blockchain_message = message_hash[0] #what is message_hash?
    blockchain_hash = message_hash[1]
    blockchain_height = message_hash[2]
    ledger = message_hash[3]

    return(jsonify("", render_template("block_component.html", blockchain_message=blockchain_message, blockchain_hash=blockchain_hash, blockchain_height=blockchain_height, ledger=ledger)))

@application.route("/api_recieveBlockchain/<game_name>/<username>", methods=["POST", "GET"]) #api to recieve the blockchain for ajax
def recieve_block_api(game_name, username):
    blocks = new_block_requests(game_name, username)
    heights = blocks[0]
    hashes = blocks[1]
    ids = blocks[2]
    ledgers = blocks[3]
    return(jsonify("", render_template("requests_component.html", game_name=game_name, username=username, heights=heights, hashes=hashes, ids=ids, ledgers=ledgers)))

@application.route("/api_accept_reject/<game_name>/<username>/<choice>/<id>", methods=["POST","GET"]) #api to accept or reject a request for ajax
def accept_reject_api(game_name, username, choice, id):

    #transactions need to include block rewards for the miner
    if choice == "accept": #accepting replaces the timestamp, block height, prevhash, transactions, lastnonce, and ledger for first document
        accept_block(game_name, username, id)
        remove_block(game_name, username, id)
        
    if choice == "reject":
        remove_block(game_name, username, id)
    
    block = current_block(game_name, username)
    blockchain_message = block[0]
    blockchain_hash = block[1]
    blockchain_height = block[2]
    ledger = block[3]
    return(jsonify("", render_template("block_component.html", blockchain_message=blockchain_message, blockchain_hash=blockchain_hash, blockchain_height=blockchain_height, ledger=ledger)))
    


if __name__ == "__main__":
    # turn debug off for prodcution deployment
    application.run(debug=True, host='0.0.0.0')

#Explore local storage for some of the data, it might be easier than constant queries




