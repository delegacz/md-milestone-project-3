import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
##loading credenditls from seperate file
from credentials import auth_data, auth_string
from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
#enviorement virables loading
load_dotenv()
DBNAME = os.getenv("DBNAME")
DATABASEURI = os.getenv("URI")
#calling api for spotify token
token_response = requests.post('https://accounts.spotify.com/api/token',
                    data = auth_data,
                    headers = auth_string,)  
token_response_data = token_response.json()
##token
the_token = token_response_data['access_token']

app = Flask(__name__)

#Connecting to database
app.config["MONGO_DBNANE"] = DBNAME
app.config["MONGO_URI"] = DATABASEURI

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def display():
    def get_playlist_image(id):
        image_response = requests.get('https://api.spotify.com/v1/playlists/' + id + '/images',
                           headers={'Authorization':'Bearer '+ the_token})
        if(image_response.status_code == 200):
            image_response_data = image_response.json()
            image_url = image_response_data[0]['url']
            return image_url
        else:
            image_url='./static/img/missing.jpg'
            return image_url

    all_categories = mongo.db.categories.find()    
    return render_template("home.html", playlists=mongo.db.playlists.find(), get_playlist_image=get_playlist_image, categories=all_categories)

@app.route('/category/<category_id>')
def display_category():
    the_categories = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    def get_playlist_image(id):
        image_response = requests.get('https://api.spotify.com/v1/playlists/' + id + '/images',
                           headers={'Authorization':'Bearer '+ the_token})
        if(image_response.status_code == 200):
            image_response_data = image_response.json()
            image_url = image_response_data[0]['url']
            return image_url
        else:
            image_url='./static/img/missing.jpg'
            return image_url
    return render_template("home.html", playlists=mongo.db.playlists.find(), get_playlist_image=get_playlist_image, category=the_categories)

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

@app.route('/playlist/<playlist_id>')
def display_tracks(playlist_id):
    the_playlist = mongo.db.playlists.find_one({'_id': ObjectId(playlist_id)})
    def status_check(id):
        status_response = requests.get('https://api.spotify.com/v1/playlists/'+ id +'/', headers={'Authorization':'Bearer '+ the_token})
        if(status_response.status_code == 200):
            return True
        else:
            return False

    def get_playlist_tracklist(id):
        tracklist_response = requests.get('https://api.spotify.com/v1/playlists/'+ id +'/tracks', headers={'Authorization':'Bearer '+ the_token})
        track_list = []
        count = 0
        if(tracklist_response.status_code==200):
                tracklist_response_data = tracklist_response.json()
                maxium_of_values = len(tracklist_response_data['items'])
                while count < maxium_of_values:
                    track_list.append(tracklist_response_data['items'][count]['track'])
                    count+=1
                else:
                    return track_list
        else:
            track_list = False
    return render_template('playlist_details.html', playlist=the_playlist, get_playlist_tracklist=get_playlist_tracklist, status_check=status_check)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=(os.environ.get('PORT')),
    debug=True)