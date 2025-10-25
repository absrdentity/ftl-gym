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

@app.route('/join', methods=['GET', 'POST'])
def join_membership():
    if request.method == 'POST' and 'name' in request.form and 'email' and 'password' and 'phone' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO members VALUES (NULL, %s, %s, %s, %s)', (name, email, password, phone))
        mysql.connection.commit()
        return redirect(url_for('member_home'))
    else:
        return render_template('join.html')

@app.route('/membership', methods=['GET'])
def membership():
    return render_template('membership.html')

@app.route('/our-clubs')
def our_clubs():
    return render_template('our_clubs.html')

if __name__ == '__main__':
    app.run(debug=True)