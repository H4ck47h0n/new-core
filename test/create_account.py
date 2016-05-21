#!/usr/bin/env python
# encoding: utf-8


from requests import  requests as rq


from random import choice

def hehe(name):
	resp = rq.post("http://127.0.0.1:5000/account/shit",json={
                "name":name,
                "password":"shit",
                "avator":"jsjsjsjsj",
                "profile":{
                    "age":1,
                    "sex":"F",
                    "interests":{
                        "1":choice([1,0,1,0]),
                        "2":choice([1,0,1,0]), 
			"3":"1",
			"4":"1",
			"5":choice([1,0,1,0]),
                    }

                }
	})


hehe("djt")
hehe("jiangmian")
hehe("ximgjig")
hehe("fuck")
hehe("maoche")
