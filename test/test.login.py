#!/usr/bin/env python
# encoding: utf-8

from requests import requests as rq
cookie = ""
def login(name,pw):
    rep = rq.post("http://127.0.0.1:5000/login",json={
        "username":name,
        "password":pw
    })
    print(rep.text
          )
    cookie = rep.cookies
def index():
    rep = rq.get("http://127.0.0.1:5000",cookies=cookie)
    print(rep.text)


login("fuck","shit"
      )

print(cookie)
index()
