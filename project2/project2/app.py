import os

from flask import Flask, render_template,redirect,url_for,session,request,json
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit
import json
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

messages = {}

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")
@app.route("/enter",methods=["POST"])
def enter():
    username = request.form.get("username")
    session["user"] = username
    return redirect(url_for("chat"))
@app.route("/chat",methods=["GET"])
def chat():
    if not "user" in session:
        return redirect(url_for("index"))
    else:
        return render_template("chat.html")
@socketio.on("submit channel")
def newChannel(data):
    name = data["name"]
    emit("announce channel",{"name":name},broadcast=True)
    messages[name] = []
    print(messages)
@socketio.on("submit message")
def newMessage(data):
    message = data["message"]
    channel = data["channel"]
    index = data["index"]
    emit("announce message",{"message":message,"channel":channel},broadcast=True)
    messages[channel].append(message)
    print(messages)
@app.route("/getMessages",methods=["GET"])
def getMessages():
    return messages