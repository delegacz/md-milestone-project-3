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
def display():
    return render_template("home.html", 
                           playlists=mongo.db.playlists.find())


@app.route('/add')
def add():
    return render_template('add.html',
                            categories=mongo.db.categories.find())

@app.route('/insert', methods=['POST','GET'])
def inert_playlist():
    playlists=mongo.db.playlists
    playlists.insert_one(request.form.to_dict())
    return redirect(url_for('display'))



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=(os.environ.get('PORT')),
    debug=True)