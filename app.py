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