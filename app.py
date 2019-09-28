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

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

#Connecting to database
app.config["MONGO_DBNANE"] = DBNAME
app.config["MONGO_URI"] = DATABASEURI

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def display():
    return render_template("home.html", 
                           playlists=mongo.db.playlists.find())


@app.route('/add')
def add():
    return render_template('add.html',
                            categories=mongo.db.categories.find())

@app.route('/insert', methods=['POST','GET'])
def insert_playlist():
    playlists=mongo.db.playlists
    playlists.insert_one(request.form.to_dict())
    return redirect(url_for('display'))


@app.route('/edit/<playlist_id>')
def edit_playlist(playlist_id):
    the_playlist = mongo.db.playlists.find_one({'_id': ObjectId(playlist_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edit.html', playlist=the_playlist,
                                        categories=all_categories)

@app.route('/update_playlist/<playlist_id>',methods=['POST'])
def update_playlist(playlist_id):
    playlist = mongo.db.playlists
    playlist.update(
        {'_id': ObjectId(playlist_id)},
        {
            'name':request.form.get('name'),
            'category':request.form.get('category_name'),
            'description': request.form.get('description'),
            'spotify_id':request.form.get('spotify_id'),
            'spotify_link':request.form.get('spotify_link'),
        }
    )
    return redirect(url_for('display'))

@app.route('/delete_playlist/<playlist_id>')
def delete_playlist(playlist_id):
    mongo.db.playlists.remove({'_id': ObjectId(playlist_id)})
    return redirect(url_for('display'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=(os.environ.get('PORT')),
    debug=True)