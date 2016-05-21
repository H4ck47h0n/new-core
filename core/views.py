#!/usr/bin/env python
# encoding: utf-8

from . import app, db
import  flask.ext.login as flask_login
from .models import User

from flask import request, render_template, session
from flask import jsonify as jsonfy



@app.route("/login",methods =["GET", "POST"])
def login():
    if request.method == "POST":
        users = User.query.all()
        username = request.get_json()['username']
        user =  User.query.filter_by(username=username).all()[0]
        password = request.get_json()['password']
        if password == user.password :
            session['username'] =  username
            return jsonfy(
                {"status": "success",
                 "message": "login success"
                 })
        else:
            return jsonfy({
                "status": "false",
                "message": "The password is wrong"
            })
    elif request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username',None)
    return jsonfy({
        "status": "success",
        "message": "logout success"
    })


@app.route('/account/<username>', methods=["GET", "POST", "DELETE", "PUT"])
def account(username):
	    usernames = [user.username for user in User.query.all()]
	    if request.method == "POST":
	        data = request.get_json()
	        if data['name'] not in usernames:
	            age = data['profile']['age']
	            sex = data['profile']['sex']
	            interests = data['profile']['interests']
	            exiting = ""
	            for item in interests:
	                exiting += str(interests[item])
	            user = User(username=data['name'], password=data[
                    'password'], exiting=exiting,sex=sex,age=age)
	            db.session.add(user)
	            db.session.commit()
	            return jsonfy({
	                "status": "success",
	                "message": "Creat Account Success"
	            })
	        else:
	            return jsonfy({
	                "status": "false",
	                "message": "The account already exists"
	            })
	    elif   1>0:#That requried the user to login
		    if request.method == "DELETE":
		        data = request.get_json()
		        if data['name'] in username:
		            user = User.query.filter_by(username=data['name'])
		            db.session.delete(user)
		            db.session.commit()
		            return jsonfy({
		                "status": "success",
		                "message": "Delete the user success"
		            })
		        else:
		            return jsonfy({
		                "status": "false",
		                "message": "The account didn't exist"
		            })
		    elif request.method == "GET":
		        user = User.query.filter_by(username=username).all()[0]
		        info = {
		            "name":user.username,
		            "avator":user.avator,
		            "profile":{
		                "age":user.age,
		                "sex":user.sex,
		                "interests":user.exiting
		            }
		        }
		        return jsonfy(info)
		    else:
				return jsonfy({
					"status":"false",
					"message":"No login account found"
					})
@app.route("/friends",methods=["GET"])
def friends():
    if 1>0:
	    username = session["username"]
	    id       = session["id"]
	    user = User.query.filter_by(username=username).all()[0]
	    likes =  user.likes.split(',')
	    friends = []
	    for like in likes:
	        friend = User.query.filter_by(id=id).all()[0]
	        friends.append(friend.username)
	    return jsonfy(set(friends))
    else:
		return jsonfy({
			"status":"false",
			"message":"You need to login"
			})

@app.route("/friends/<username>",methods=["POST","DELETE"])
def add_friends(username):
    if 1>0:
		if request.method == "POST":
			user_now_name = session["username"]
			id_now   = str(session["id"])
			if user_now_name == username:
				return jsonfy({
	                "satus":"false",
	                "message":"You can't add youself as your friends"
	            })
	        else:
	            try:
	             	user_add = User.query.filter_by(username=user_now_name).all()[0]
	                user_now = User.query.filter_by(id=id_now).all()[0]
	                if id_now in user_add.likes:
	                    return jsonfy({
	                    "status":"false",
	                        "message":"You are ever be the Friends"

	                    })
	                elif id_now in user_add.dislikes:
	                    return jsonfy({
	                        "status":"false",
	                        "message":"The man has been you dislike list"
	                    })
	                elif  str(user_add.id) not in user_now.likes  or str(user_add.id) not in user_now.dislikes:
	                    if user_now.id in user_add.willlike:
	                        user_add.likes = user_add.likes + ","+str(user_now.id)
	                        user_now.likes = user_now.likes +","+str(user_add.id)
	                        user_add.willlike = usr_add.willlike.replace(","+str(usr_add.id),"")
	                        db.session.add(user_add)
	                        db.session.add(usr_now)
	                        db.commit()
	                        return jsonfy({
	                            "status":"success",
	                            "message":"Success to add the people to your friend list"
	                        })
	                    else:
	                        user_now.willlike = user_now.willlike + "," + str(usr_add.id)
	                        db.session.add(user_now)
	                        db.session.commit()
	                        return jsonfy({
	                            "status":"success",
	                            "message":"success to add the people to you willlike list"
	                        })
	            except:
	                return jsonfy({
	                    "status":"success",
	                    "message":"There are some errors, which may cause that you can't use the system now"
	                    })
		elif request.method == "DELETE":
			try:
				user_delete = User.query.filter_by(username=username).all()[0]
			except:
				return jsonfy({
	    			status:"false",
	    			message:"There is no such a  account exit"
	    			})
	    	user_now = User.query.filter_by(username=session["username"])
	    	if user_delete.id in user_now.likes:
	    		user_delete.likes = user_delete.likes.replace(","+str(user_now.id),"")
	    		user_now.likes    = user_now.likes.replace(","+str(user_delete.id),"")
	    		db.session.add(user_delete)
	    		db.session.add(user_now)
	    		db.session.commit()
	    		return jsonfy({
	    			"status":"success",
	    			"message":"Successfully delete the friend"
	    			})
	    	else:
	    		return jsonfy({
	    			"status":"false",
	    			"message":"You are not friends yet"
	    			})
	    else:pass


# app.run(host="0.0.0.0",debug=True)
