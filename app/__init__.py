from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object("config.Config")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

mongo = PyMongo(app, authSource="admin")


from app.routes import sells_by_client_routes

app.register_blueprint(sells_by_client_routes)
