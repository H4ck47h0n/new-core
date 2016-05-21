#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
import os
from flask.ext.login import LoginManager
lm = LoginManager()
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.secret_key = "fuckxiasisdsa"
db = SQLAlchemy(app)
lm.init_app(app)
import core.models
import core.views
