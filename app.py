import os
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
#enviorement virables loading
load_dotenv()
DBNAME = os.getenv("DBNAME")
DATABASEURI = os.getenv("URI")

app = Flask(__name__)

#Connecting to database
app.config["MONGO_DBNANE"] = DBNAME
app.config["MONGO_URI"] = DATABASEURI

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def display():
    return render_template("home.html", 
                           playlists=mongo.db.playslist.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=(os.environ.get('PORT')),
    debug=True)