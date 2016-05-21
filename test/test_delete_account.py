#!/usr/bin/env python
# encoding: utf-8


from requests import requests as rq

def delete(name):
    ras = rq.delete("http://127.0.0.1:5000/account/%s"%name,json={
        "name":name
    })
    print(ras.text)

while True:
    name = raw_input()
    delete(name)
