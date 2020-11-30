from flask import Flask, request, json, jsonify
from flask_pymongo import PyMongo
from flask_pymongo import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

mongo = PyMongo(app)

data_user = mongo.db.user

@app.route('/', methods=['GET'])
def home():
  return "Initialize API"

@app.route('/user', methods=['POST'])
def create_user():

  response = {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': generate_password_hash(request.json['password'])
  }
  if response['name'] and response['email'] and response['password']:
    try:
      data_user.insert(response)
      resp = jsonify("User added successfully")
      resp.status_code = 200
      return resp
    except Exception:
      return "Data error"
  else:
    return not_found()


@app.route('/user', methods=['GET'])
def findAllUser():
  users = data_user.find()
  resp = dumps(users)
  return resp

@app.route('/user/<id>', methods=['GET'])
def findByIdUser(id):
  users = data_user.find_one({'_id': ObjectId(id)})
  resp = dumps(users)
  return resp

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
  users = data_user.find_one_and_delete({'_id': ObjectId(id)})
  resp = dumps(users)
  return resp

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
  response = {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': generate_password_hash(request.json['password'])
  }
  users = data_user.find_one_and_update({'_id': ObjectId(id)}, response )
  resp = dumps(users)
  return resp


@app.errorhandler(404)
def not_found(error=None):
  message = {
    'status': 404,
    'message': 'Not found ' + request.url
  }

  resp = jsonify(message)
  resp.status_code = 400

  return resp


if __name__ == "__main__":
  app.run(port="8000", debug=True)