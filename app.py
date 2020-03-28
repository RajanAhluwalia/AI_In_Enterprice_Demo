#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:15:08 2020

@author: rajan
"""

from flask import Flask, json
from flask import jsonify
from flask import flash, request
#from werkzeug import generate_password_hash, check_password_hash
from mysql.connector import MySQLConnection

app = Flask(__name__)

def create_conn():
    conn = MySQLConnection(host="localhost", user="root", passwd="credable", database="flask_app")
    #print(conn)
    return conn



@app.route('/')
def hello():
    return {'Welcome':' to my first Flask Application'}


@app.route('/create', methods=['GET'])
def create():
    try:
	    sql = "CREATE TABLE `flask_app`.`users` (`student_id` INT NOT NULL AUTO_INCREMENT,  `first_name` VARCHAR(45) NULL,  `last_name` VARCHAR(45) NULL,  `dob` VARCHAR(45) NULL,  `amount_due` FLOAT NULL,  PRIMARY KEY (`student_id`))"
	    conn = create_conn()
        cursor = conn.cursor()
	    cursor.execute(sql)
	    conn.commit()
        resp = jsonify('Table created successfully!')
        resp.status_code = 200
        return resp

    except Exception as e:
        return handle_unexpected_error(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/add', methods=['POST'])
def add_user():
    try:
        _json = request.json
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _dob = _json['dob']
        _amount_due = _json['amount_due']

        # validate the received values
        if _first_name and _last_name and _dob and _amount_due and request.method == 'POST':
    
            # save edits
            sql = "INSERT INTO users(first_name, last_name, dob, amount_due) VALUES(%s, %s, %s, %s)"
            data = (_first_name, _last_name, _dob, _amount_due)
            conn = create_conn()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/users', methods=['GET'])
def users():
    try:
        conn = create_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/users/<int:id>', methods=['GET'])
def fetchOne(id):
    try:
	    print(id)
        conn = create_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE student_id=%s", (id,))
        row = cursor.fetchone()
	    resp = jsonify(row)
	    resp.status_code = 200
	    return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['POST'])
def update_user():
    try:
        _json = request.json
        _student_id = _json['student_id']
        _first_name = _json['first_name']
        _last_name = _json['last_name']
        _dob = _json['dob']
        _amount_due = _json['amount_due']
        # validate the received values
        if _first_name and _last_name and _dob and _amount_due and _student_id and request.method == 'POST':
        
            # save edits
            sql = "UPDATE users SET first_name=%s, last_name=%s, dob=%s, amount_due=%s WHERE student_id=%s"
            data = (_first_name, _last_name,_dob,_amount_due, _student_id)
            conn = create_conn()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        conn = create_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE student_id=%s", (id,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    message = str(error.args)
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'UnexpectedException',
            'message': 'An unexpected error has occurred. ' + message
        }
    }

    return jsonify(response), status_code


if __name__ == "__main__":
    app.run()
