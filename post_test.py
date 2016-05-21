#!/usr/bin/env python
# encoding: utf-8


from requests import requests as rq

resp = rq.post("http://127.0.0.1:5000",
               json={"username": "dengqi", "password": "shshshshsh"})

print resp.text
