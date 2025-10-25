from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = '!@#$'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ftl_gym'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET'])
def join_membership():
    return render_template('join.html')

@app.route('/membership', methods=['GET'])
def membership():
    return render_template('membership.html')

@app.route('/our-clubs')
def our_clubs():
    return render_template('our_clubs.html')

if __name__ == '__main__':
    app.run(debug=True)