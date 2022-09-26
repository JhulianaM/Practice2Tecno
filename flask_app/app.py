from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask import request

import flask
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dbcontainer'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'

mysql = MySQL(app)

@app.route('/professors/<int:id>', methods=['GET'])
def professor_get_json(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, address, Convert(salary,char) AS salary FROM professor WHERE id = %i' %
                    id)
    data = cursor.fetchone()
    resp = flask.Response(json.dumps(data))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/professor', methods=['POST'])
def professor_post_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("INSERT INTO professor (first_name, last_name, city, address, salary) VALUES ('%s', '%s', '%s', '%s', %d)" % 
                   (data['first_name'], data['last_name'], data['city'], data['address'], data['salary']))
    
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/professors', methods=['PUT'])
def professor_put_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("UPDATE professor SET first_name='%s', last_name='%s', city='%s', address='%s', salary=%d WHERE id=%i" % 
                   (data['first_name'], data['last_name'], data['city'], data['address'], data['salary'], data['id']))
    
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp

#delete
@app.route('/professorsdelete', methods=['POST'])
def professor_delete_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("DELETE FROM professor WHERE id=%i" % 
                   (data['id']))
    
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/professorsdeleteget/<int:id>', methods=['GET'])
def professor_eliminar_json(id):
    return render_template('delete_professor.html')



@app.route('/professorlist', methods=['GET'])
def professor_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('list.html', professors=data)

@app.route('/professorupdate/<int:id>', methods=['GET'])
def professor_update_json(id):
    return render_template('update_professor.html')

@app.route('/professorcreate', methods=['GET'])
def professor_create_json():
    return render_template('create_professor.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
