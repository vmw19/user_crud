from flask import (
    Flask,
    request
)

from datetime import datetime
from app.database import user

app = Flask(__name__)

VERSION = "1.0.0"


@app.get('/ping')
def ping():
    out = {
        "status": "ok",
        "message":"pong"
    }
    return out

@app.get("/version")
def version():
    out = {
        "status": "ok",
        "version": VERSION,
        "server_time": datetime.now().strftime("%F %H:%M:%S")
    }
    return out

@app.get("/users")
def get_all_users():
    user_list = user.scan()
    out = {
        "status": "ok",
        "users": user_list
    }

    return out

@app.get("/users/<int:pk>")
def get_user_by_id(pk):
    record = user.select_by_id(pk)
    out = {
        "status": "ok",
        "user": record
    }
    if not record:
        out["status"] = "error"
        out["message"] = "not found"
        returnout, 404

    else:
        out ["user"] = record

    return out

@app.post("/users")
def create_user():
    user_data= request.json
    user.insert(user_data)
    return "", 204

@app.put("/users/<int:pk>")
def update_user(pk):
    user_data = request.json
    user.update(user_data, pk)
    return "", 204

@app.delete("/users/<init:pk")
def delete_user(pk):
    user.deactivate_user(pk)
    return "", 204