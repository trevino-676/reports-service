import os

from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt import jwt

app = Flask(__name__)
app.config.from_object("config.Config")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

mongo = PyMongo(app, authSource="admin")