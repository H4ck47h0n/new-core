#!/usr/bin/env python
# encoding: utf-8

from requests import requests as rq

res = rq.post("http://127.0.0.1:5000/login",json={"username":"test","password":"test"})
print res.text
