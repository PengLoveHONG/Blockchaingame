from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import redirect
import pymongo
from pymongo import MongoClient
import certifi

#REMEMBER TO MAKE A REQUIREMENTS.TXT FILE

application = Flask(__name__)



@application.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')

@application.route('/play', methods=["POST", "GET"])
def play():
    return render_template('play.html')
    
if __name__ == "__main__":
    # turn debug off for prodcution deployment
    application.run(debug=True, host='0.0.0.0')

