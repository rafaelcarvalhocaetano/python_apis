from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/api-mongo-react'
mongo = PyMongo(app)

# Settings
CORS(app)

# Database
db = mongo.db.users


@app.route('/', methods=['GET'])
def initialRouter():
  return "API - PYTHON-3 FOR REACT"

@app.route('/users', methods=['POST'])
def createUser():
  id = db.insert({
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password']
  })
  if (id):
    return jsonify(str(ObjectId(id)))
  else:
    return "Deu"
    

@app.route('/users', methods=['GET'])
def getAllUsers():
  users = []
  for user in db.find():
    users.append({
      '_id': str(ObjectId(user['_id'])),
      'name': user['name'],
      'email': user['email'],
      'password': user['password'],
    })
  return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUsersById(id):
  user = db.find_one({'_id': ObjectId(id)})
  dataJSON = {
    '_id': str(ObjectId(user['_id'])),
    'name': user['name'],
    'email': user['email'],
    'password': user['password'],
  }
  return jsonify(dataJSON)

@app.route('/users/<id>', methods=['PUT'])
def updateUserById(id):
  dataJSON = {
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password'],
  }
  db.find_one_and_update({'_id': ObjectId(id)}, {'$set': dataJSON})
  
  return jsonify(dataJSON)

@app.route('/users/<id>', methods=['DELETE'])
def deleteUserById(id):
  user = db.find_one_and_delete({'_id': ObjectId(id)})
  dataJSON = {
    '_id': str(ObjectId(user['_id'])),
    'name': user['name'],
    'email': user['email'],
    'password': user['password'],
  }
  return jsonify(dataJSON)


if __name__ == '__main__':
  app.run(debug=True)