from flask import Flask, jsonify, request, url_for, redirect, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = '!@#$'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ftl-gym'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET', 'POST'])
def join():

    selected_package = request.args.get('package', '')

    if request.method == 'POST' and all(k in request.form for k in ['name', 'email', 'password', 'phone', 'package']):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        package = request.form['package']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO members (name, email, password, phone, package) VALUES (%s, %s, %s, %s, %s)',
            (name, email, password, phone, selected_package)
        )
        mysql.connection.commit()

        return redirect(url_for('member_home', name=name, package=selected_package))
    
    return render_template('join.html', selected_package=selected_package)


@app.route('/member_home')
def member_home():
    name = request.args.get('name')
    package = request.args.get('package')
    return render_template('member_home.html', name=name, package=package)


@app.route('/membership', methods=['GET'])
def membership():
    return render_template('membership.html')

@app.route('/our-clubs')
def our_clubs():
    return render_template('our_clubs.html')

if __name__ == '__main__':
    app.run(debug=True)