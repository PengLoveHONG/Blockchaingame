from flask import Flask, render_template, redirect, url_for, request, jsonify
from werkzeug.utils import redirect
import pymongo
from pymongo import MongoClient
import certifi

from mongdb_connectionstring import connection_string
from mongodb import game_creation, game_join, user_query, balance_query, add_name

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
        
        try:
            game_name_create = request.form['GameNameCreate']
        except:
            game_name_join = request.form['GameNameJoin']

        if game_name_create != "NA":
            game_creation(username, game_name_create)
            return redirect(url_for('lobby', game_name=game_name_create, username=username))
        
        if game_name_join != "NA":
            if game_join(username, game_name_join) == False: #adds name to db
                return render_template('play.html', error="Game does not exist")
            else:
                if (username in user_query(game_name_join)):
                    return render_template('play.html', error="Username has been taken")
                else:
                    add_name(username, game_name_join)
                    return redirect(url_for('lobby', game_name=game_name_join, username=username))

        else:
            return render_template('play.html')
    else:
        return render_template('play.html', error=error)
    

    


@application.route('/lobby/<game_name>/<username>', methods=["POST", "GET"]) #CREATE A FUNCTION THAT ALTERS THE USERNAME URL SO PEOPLE CANNOT ENTER OTHERS GAME BY NAME
def lobby(game_name, username):

    #queries the mongodb database and grabs the names within the given game_name
    #the webpage lobby.html should dynamically update with the database, requering aevery 5 seconds
    list_of_players = user_query(game_name)

    return render_template('lobby.html', username=username, game_name=game_name, list_of_players=list_of_players)


@application.route('/game/<game_name>/<username>/game', methods=["POST", "GET"])
def game(game_name, username):
    balance = balance_query(username, game_name)
    return render_template('game.html', username=username, game_name=game_name, balance=balance)



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





