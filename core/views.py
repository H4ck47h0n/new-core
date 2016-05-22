#!/usr/bin/env python
# encoding: utf-8

from . import app, db, lm
import flask.ext.login as flask_login
from .models import User
from functools import wraps
from flask.ext.login import current_user, login_required, login_user, logout_user
from flask import request, render_template, session,redirect,url_for
from flask import jsonify as jsonfy
from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=31)

# from functools import wraps
# def authorize(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwds):
#         user = session.get('username', None)
#         if user:
#             return fn(user=user)
#         else:
#             return "you need to login"
#     return wrapper
@lm.user_loader
def load_user(id):
	user = User.query.filter_by(id=id).first()
	return user


@app.route("/")
def index():
	return "Welcome"
@app.route("/chat/")
def chat():
	return render_template("chat.html")
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		users = User.query.all()
		# try:
		# 	name = request.get_json()['username']
		# 	password = request.get_json()['password']
		# except Exception,e:
		# 	print(e)
		name = request.form["name"]
		password = request.form["password"]
		try:
			user = User.query.filter_by(username=name).all()[0]
		except Exception,e:
			return jsonfy(
				{"status": "false",
				 "message": str(e)
				 })
		if password == user.password:
			login_user(user,remember=True)
			return  redirect(url_for("index"))
		else:
			return jsonfy({
				"status": "false",
				"message": "The password is wrong"
			})
	elif request.method == "GET":
		return render_template("login.html")


@app.route("/logout")
def logout():
	logout_user()
	return jsonfy({
		"status": "success",
		"message": "logout success"
	})
@app.route("/fake")
def fake():
    return redirect(url_for("chat"))
@app.route("/signup")
def signup():
	return render_template("singup.html")

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
						'password'], exiting=exiting, sex=sex, age=age)
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
		elif 1 > 0:  # That requried the user to login
			if request.method == "DELETE":
				data = request.get_json()
				name = data['name']
				print(name)
				if data['name'] in username:
					user = User.query.filter_by(username=name).all()[0]
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
				try:
						name_ = username
						user = User.query.filter_by(username=name_).all()[0]
				except Exception,e:
					return jsonfy({
					"status":"false",
					"message":str(e)
					})
				info = {
						"name": user.username,
						"avator": user.avator,
						"profile": {
							"age": user.age,
							"sex": user.sex,
							"interests": user.exiting
						}
					}
				return jsonfy(info)
			else:
				return jsonfy({
									"status": "false",
									"message": "No login account found"
								})


@app.route("/friends", methods=["GET"])
def friends():
	if 1 > 0:
		username = session["username"]
		id = session["id"]
		user = User.query.filter_by(username=username).all()[0]
		likes = user.likes.split(',')
		friends = []
		for like in likes:
			friend = User.query.filter_by(id=id).all()[0]
			friends.append(friend.username)
		return jsonfy(set(friends))
	else:
		return jsonfy({
					"status": "false",
					"message": "You need to login"
				})


@app.route("/friends/<username>", methods=["POST", "DELETE"])
def add_friends(username):
	if 1 > 0:
		if request.method == "POST":
			user_now_name = session["username"]
			id_now = str(session["id"])
			if user_now_name == username:
				return jsonfy({
									"satus": "false",
									"message": "You can't add youself as your friends"
								})
			else:
				try:
					user_add = User.query.filter_by(username=user_now_name).all()[0]
					user_now = User.query.filter_by(id=id_now).all()[0]
					if id_now in user_add.likes:
						return jsonfy({
								"status": "false",
							"message": "You are ever be the Friends"

						})
					elif id_now in user_add.dislikes:
						return jsonfy({
							"status": "false",
							"message": "The man has been you dislike list"
						})
					elif str(user_add.id) not in user_now.likes or str(user_add.id) not in user_now.dislikes:
						if user_now.id in user_add.willlike:
							user_add.likes = user_add.likes + \
								"," + str(user_now.id)
							user_now.likes = user_now.likes + \
									"," + str(user_add.id)
							user_add.willlike = usr_add.willlike.replace(
							   "," + str(usr_add.id), "")
							db.session.add(user_add)
							db.session.add(usr_now)
							db.commit()
							return jsonfy({
								"status": "success",
								"message": "Success to add the people to your friend list"
							})
						else:
							user_now.willlike = user_now.willlike + \
							"," + str(usr_add.id)
							db.session.add(user_now)
							db.session.commit()
						return jsonfy({
								"status": "success",
								"message": "success to add the people to you willlike list"
							})
				except:
					return jsonfy({
						"status":"success",
						"message":"There are some errors, which may cause that you can't use the system now"
						})
		elif request.method=="DELETE":
			try:
				user_delete = User.query.filter_by(username=username).all()[0]
			except:
				return jsonfy({
					status: "false",
					message: "There is no such a  account exit"
				})
			user_now = User.query.filter_by(username=session["username"])
			if user_delete.id in user_now.likes:
				user_delete.likes = user_delete.likes.replace("," + str(user_now.id), "")
				user_now.likes = user_now.likes.replace("," + str(user_delete.id), "")
				db.session.add(user_delete)
				db.session.add(user_now)
				db.session.commit()
				return jsonfy({
									"status": "success",
									"message": "Successfully delete the friend"
								})
			else:
				return jsonfy({
							"status": "false",
							"message": "You are not friends yet"
						})
		else:pass

@app.route("/char/random")
def random_chat():
	pass

# app.run(host="0.0.0.0",debug=True)
