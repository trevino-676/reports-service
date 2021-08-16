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

from app.routes import payroll_routes

app.register_blueprint(payroll_routes)

from app.routes import retention_routes

app.register_blueprint(retention_routes)

from app.routes.provider_routes import detailed_routes

app.register_blueprint(detailed_routes)
