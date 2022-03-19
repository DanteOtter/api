#!/usr/bin/python3
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
import mysql.connector, hashlib
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="plague"
)
cursor = db.cursor(buffered = True)
app = Flask(__name__)

disbase = {'name', 'Did', 'Infrate', 'Mortality', 'Tid'}
conbase = {'name', 'Cid', 'Infrate', 'Mortality', 'Population', 'Did'}
treatbase = {'tname', 'Tid', 'RecovRate', 'tlength'}


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    print(username + '\n' + password)
    cursor.execute('select count(1) from Users where Username=%s and Password=%s;', (username, password))
    if cursor.fetchone()[0]:
        return username
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/find_country', methods=['GET'])
#@auth.login_required
def find_country():
    ma = 'select * from Country where '
    index = 0
    for a in request.args:
        if str(a) not in conbase:
            abort(400)
        if index == 0:
            if str(a) == 'name':
                ma = ma + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + a +'=' + request.args[str(a)] + ''
        else:
            if str(a) == 'name':
                ma = ma + ' and ' + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + ' and ' + a +'=' + request.args[str(a)]
        index = index + 1
    cursor.execute(ma)
    return jsonify(cursor.fetchall())

@app.route('/add_country', methods=['POST'])
@auth.login_required
def add_country():
    ma = 'insert ignore into Country values ('
    try:
        for index, a in enumerate(request.args):
            if str(a) not in conbase:
                print(str(a))
                abort(400)
            if index == 0:
                    ma = ma + '"' + request.args[str(a)] + '"'
            else:
                    ma = ma + ',  ' + request.args[str(a)]
        cursor.execute(ma+')')
        db.commit()
        return make_response(jsonify( { 'Success': 'Country added!' } ), 200)
    except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.DataError ) as err:
        abort(400)

@app.route('/remove_country', methods=['POST'])
@auth.login_required
def remove_country():
    ma = 'delete from Country where '
    try:
        if len(request.args) > 1:
            abort(400)
        ma = ma + 'Cid=' + request.args['Cid']
        cursor.execute(ma)
        db.commit()
        return make_response(jsonify( { 'Success': 'Country Removed!' } ), 200)
    except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.DataError ) as err:
        abort(400)

@app.route('/find_disease', methods=['GET'])
#@auth.login_required
def find_disease():
    ma = 'select * from Disease where '
    index = 0
    for a in request.args:
        if str(a) not in disbase:
            abort(400)
        if index == 0:
            if str(a) == 'name':
                ma = ma + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + a +'=' + request.args[str(a)] + ''
        else:
            if str(a) == 'name':
                ma = ma + ' and ' + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + ' and ' + a +'=' + request.args[str(a)]
        index = index + 1
    cursor.execute(ma)
    return jsonify(cursor.fetchall())

@app.route('/add_disease', methods=['POST'])
@auth.login_required
def add_disease():
    ma = 'insert ignore into Disease values ('
    try:
        for index, a in enumerate(request.args):
            if str(a) not in disbase:
                print(str(a))
                abort(400)
            if index == 0:
                    ma = ma + '"' + request.args[str(a)] + '"'
            else:
                    ma = ma + ',  ' + request.args[str(a)]
        cursor.execute(ma+')')
        db.commit()
        return make_response(jsonify( { 'Success': 'Disease added!' } ), 200)
    except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.DataError ) as err:
        abort(400)

@app.route('/remove_disease', methods=['POST'])
@auth.login_required
def remove_disease():
    ma = 'delete from Disease where '
    try:
        if len(request.args) > 1:
            abort(400)
        ma = ma + 'Did=' + request.args['Did']
        cursor.execute(ma)
        db.commit()
        return make_response(jsonify( { 'Success': 'Disease Removed!' } ), 200)
    except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.DataError ) as err:
        abort(400)

@app.route('/update_disease', methods=['POST'])
@auth.login_required
def update_disease():
    ma = 'update Disease set Mortality=' + request.args['Mortality'] + ' where Did=' +request.args['Did']
    try:
        cursor.execute(ma)
        db.commit()
        return make_response(jsonify( { 'Success': 'Disease Updated!' } ), 200)
    except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.DataError ) as err:
        abort(400)

@app.route('/find_treatment', methods=['GET'])
#@auth.login_required
def find_treatment():
    ma = 'select * from Treatment where '
    index = 0
    for a in request.args:
        if str(a) not in treatbase:
            abort(400)
        if index == 0:
            if str(a) == 'name':
                ma = ma + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + a +'=' + request.args[str(a)] + ''
        else:
            if str(a) == 'name':
                ma = ma + ' and ' + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + ' and ' + a +'=' + request.args[str(a)]
        index = index + 1
    cursor.execute(ma)
    return jsonify(cursor.fetchall())

@app.route('/add_treatment', methods=['POST'])
@auth.login_required
def add_treatment():
    ma = 'insert ignore into Treatment values ('
    try:
        for index, a in enumerate(request.args):
            if str(a) not in disbase:
                print(str(a))
                abort(400)
            if index == 0:
                    ma = ma + '"' + request.args[str(a)] + '"'
            else:
                    ma = ma + ',  ' + request.args[str(a)]
        cursor.execute(ma+')')
        db.commit()
        return make_response(jsonify( { 'Success': 'Treatment added!' } ), 200)
    except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.DataError ) as err:
        abort(400)

@app.route('/remove_treatment', methods=['POST'])
@auth.login_required
def remove_treatment():
    ma = 'delete from Treatment where '
    try:
        if len(request.args) > 1:
            abort(400)
        ma = ma + 'Tid=' + request.args['Tid']
        cursor.execute(ma)
        db.commit()
        return make_response(jsonify( { 'Success': 'Treatment Removed!' } ), 200)
    except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.DataError ) as err:
        abort(400)

@app.route('/test_args', methods=['GET'])
#@auth.login_required
def test_args():
    ma = 'select * from Country where '
    index = 0
    for a in request.args:
        if index == 0:
            if str(a) == 'name':
                ma = ma + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + a +'=' + request.args[str(a)] + ''
        else:
            if str(a) == 'name':
                ma = ma + ' and ' + a +'="' + request.args[str(a)] + '"'
            else:
                ma = ma + ' and ' + a +'=' + request.args[str(a)]
        index = index + 1
        print(ma)
    return ma+"\n"

if __name__ == '__main__':
    app.run(debug=True, host='159.203.113.73')
