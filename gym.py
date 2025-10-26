from flask import Flask, jsonify, request, url_for, redirect, render_template, session
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

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        package = request.form['package']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO members (name, email, password, phone, package) VALUES (%s, %s, %s, %s, %s)',
            (name, email, password, phone, package)
        )
        mysql.connection.commit()

        return redirect(url_for('member_home', name=name,email=email, package=package, phone=phone))
    
    return render_template('join.html', selected_package=selected_package)


@app.route('/member_home')
def member_home():
    name = request.args.get('name')
    email = request.args.get('email')
    phone = request.args.get('phone')
    package = request.args.get('package')

    member = session.get('member')
    if not member:
        return redirect(url_for('member_login'))
    return render_template('member_home.html', name=name, package=package, email=email, phone=phone)

@app.route('/member_login', methods=['GET', 'POST'])
def member_login():
    if request.method == 'POST' and all(k in request.form for k in ['email', 'password']):
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM members WHERE email = %s AND password = %s',
            (email, password)
        )
        member = cursor.fetchone()

        if member:
            session['member'] = {
                'name': member['name'],
                'email': member['email'],
                'phone': member['phone'],
                'package': member['package']
            }
            return redirect(url_for('member_home', name=member['name'], package=member['package'], email=member['email'], phone=member['phone']))
        else:
            return 'Invalid email or password'

    return render_template('member_login.html')

@app.route('/logout')
def logout():
    session.pop('member', None)
    return redirect(url_for('home'))

@app.route('/membership', methods=['GET'])
def membership():
    return render_template('membership.html')

@app.route('/our-clubs')
def our_clubs():
    return render_template('our_clubs.html')

if __name__ == '__main__':
    app.run(debug=True)