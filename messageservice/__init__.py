import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)

from messageservice.routes import blueprint
app.register_blueprint(routes.blueprint)

from messageservice.errors import blueprint
app.register_blueprint(errors.blueprint)
