#!/usr/bin/env python
# encoding: utf-8

from requests import requests as rq

def getaccount(names):
    print(names)
    resp = rq.get("http://127.0.0.1:5000/account/%s"%(names))
    print(resp.text)

while True:
    names = str(raw_input())
    getaccount(names)
