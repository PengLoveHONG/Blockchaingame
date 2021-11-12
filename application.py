from flask import Flask, render_template, redirect, url_for, request, jsonify
from werkzeug.utils import redirect
import pymongo
from pymongo import MongoClient
import certifi

from mongdb_connectionstring import connection_string
from mongodb import game_creation, game_join, query_blockchain, user_query, balance_query, add_name, game_info_query, init_blockchain

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
            if (game_creation(username, game_name_create, difficulty, connection) == False):
                error = "Game name already exists"
                return render_template('play.html', error=error)
            else:
                init_blockchain(game_name_create, difficulty, connection)
                game_creation(username, game_name_create, difficulty, connection)
                return redirect(url_for('lobby', game_name=game_name_create, username=username, difficulty=difficulty, connection=connection))
        
        if game_name_join != "NA":
            if game_join(username, game_name_join) == False: #adds name to db
                return render_template('play.html', error="Game does not exist")
            else:
                if (username in user_query(game_name_join)):
                    return render_template('play.html', error="Username has been taken")
                else:
                    difficulty = game_info_query(game_name_join)[0]
                    connection = game_info_query(game_name_join)[1]

                    add_name(username, game_name_join, difficulty, connection)
                    return redirect(url_for('lobby', game_name=game_name_join, username=username, difficulty=difficulty, connection=connection))

        else:
            return render_template('play.html')
    else:
        return render_template('play.html', error=error)
    

    


@application.route('/lobby/<game_name>/<username>/<difficulty>/<connection>', methods=["POST", "GET"]) #CREATE A FUNCTION THAT ALTERS THE USERNAME URL SO PEOPLE CANNOT ENTER OTHERS GAME BY NAME
def lobby(game_name, username, difficulty, connection):
    list_of_players = user_query(game_name)
    return render_template('lobby.html', username=username, game_name=game_name, list_of_players=list_of_players, difficulty=difficulty, connection=connection)
    

@application.route('/game/<game_name>/<username>', methods=["POST", "GET"])
def game(game_name, username):
    balance = balance_query(username, game_name)
    query = query_blockchain(game_name)
    blockchain_message = query["blockchain_message"]
    blockchain_hash = query["blockchain_hash"]
    previous_hash = query["previous_hash"]
    difficulty = query["difficulty"]
    connection = query["connection"]

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
                            difficulty_num=difficulty_num
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


if __name__ == "__main__":
    # turn debug off for prodcution deployment
    application.run(debug=True, host='0.0.0.0')





