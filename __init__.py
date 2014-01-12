import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('config')
app.config["MONGODB_SETTINGS"] = {'DB': "refill"}
app.config["SECRET_KEY"] = 'quickrefillsyeah'
db = MongoEngine(app)

lm = LoginManager()
lm.init_app(app)

from app import views, models
