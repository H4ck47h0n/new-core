#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=["POST"])
def index():
    posts = request.get_json()
    return "name  is %r , password is %r" % (posts["username"], posts["password"])

app.run()
