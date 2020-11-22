import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

from messageservice.api.routes import blueprint
app.register_blueprint(blueprint)

from messageservice.api.errorhandlers import blueprint
app.register_blueprint(blueprint)
