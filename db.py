#!/usr/bin/python

import sqlite3
import jwt 

def connect():
  conn = sqlite3.connect('mydb.db')
  return conn

def validate(token):
  if not token:
    return False

  db = connect()
  cur = db.cursor()
  cur.execute("""
    SELECT 
      id
    FROM
      users
    WHERE
      token = ?
  """, (token,)
  )
  row = cur.fetchone()
  db.commit()
  if row:
    return True
  else:
    return False

def get_messages(token):
  messages = []

  if (not validate(token)):
    return { "success": False, "message": "invalid token" }

  db = connect()
  cur = db.cursor()
  cur.execute("""
    SELECT 
      id,
      text,
      user,
      created_on
    FROM
      messages;
  """)
  rows = cur.fetchall()

  for row in rows:
    message = {
      "id": row[0],
      "text": row[1],
      "user": row[2],
      "created_on": row[3]
    }
    messages.append(message)

  return messages



def create_message(message):
  db = connect()
  cur = db.cursor()
  cur.execute("""
    INSERT INTO messages
      (text, user, created_on)
      VALUES(?, ?, datetime());
  """, (
    message["text"],
    message["user"]
  ))
  db.commit()
  return { "success": True }

def login(user, password):
  db = connect()
  cur = db.cursor()
  cur.execute("""
    SELECT 
      id
    FROM
      users
    WHERE
      username = ? AND password = ?
  """, (user, password)
  )
  row = cur.fetchone()
  db.commit()

  if row is None:
    return { "success": False, "message": "User does not exist" }

  token = jwt.encode({}, "", algorithm="HS256")

  cur = db.cursor()
  cur.execute("""
    UPDATE users 
      SET token = ?
      WHERE id = ?
  """, (
    token,
    row[0]
  ))
  db.commit()

  return { "success": True, "id": row[0], "access_token": token }
