#!/usr/bin/python

import db
from flask import Flask, jsonify, request
from flask_cors import CORS
from time import sleep

app = Flask('chat')
CORS(app)

@app.route('/messages', methods=['GET'])
def GET_messages():
  token = request.headers.get('Authorization')
  print('token', token[7:])

  return jsonify(db.get_messages(token[7:]))

@app.route('/messages', methods=['POST'])
def POST_messages():
  message = request.get_json()
  print(message)
  return jsonify(db.create_message(message))


@app.route('/login', methods=['POST'])
def GET_login():
  user = request.get_json()

  return jsonify(db.login(user['username'], user['password']))



@app.route('/hello', methods=['GET'])
def GET_hello():
  sleep(10)
  return jsonify({"hello": "dennis"})


if __name__ == "__main__":
  app.run(debug=True)
