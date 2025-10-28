from flask import Flask, jsonify, request, url_for, redirect, render_template, session, flash
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
        
        # 🔍 Check if email already exists
        cursor.execute('SELECT * FROM members WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Email already exists → show error message
            error_message = 'Email already registered. Please use another email or log in.'
            return render_template('join.html', selected_package=selected_package, error=error_message)

        # ✅ Email not found → proceed to insert
        cursor.execute(
            'INSERT INTO members (name, email, password, phone, package) VALUES (%s, %s, %s, %s, %s)',
            (name, email, password, phone, package)
        )
        mysql.connection.commit()

        return redirect(url_for('member_home', name=name, email=email, package=package, phone=phone))
    
    return render_template('join.html', selected_package=selected_package)


@app.route('/member_home')
def member_home():
    if 'member' not in session:
        return redirect(url_for('member_login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM members WHERE id = %s', (session['member'],))
    member = cursor.fetchone()

    return render_template(
        'member_home.html',
        name=member['name'],
        email=member['email'],
        phone=member['phone'],
        package=member['package']
    )

@app.route('/member_login', methods=['GET', 'POST'])
def member_login():
    if request.method == 'POST' and all(k in request.form for k in ['email', 'password']):
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 🔍 First check if the email exists
        cursor.execute('SELECT * FROM members WHERE email = %s', (email,))
        member = cursor.fetchone()

        if not member:
            # Email not found
            error_message = 'Email not found. Please register first.'
            return render_template('member_login.html', error=error_message)

        # 🔐 If email exists, check the password
        if member['password'] != password:
            error_message = 'Incorrect password. Please try again.'
            return render_template('member_login.html', error=error_message)

        # ✅ Email and password match
        session['member'] = member['ID']
        session.permanent = True
        flash('Login successful!')
        return redirect(url_for('member_home'))

    return render_template('member_login.html')


@app.route('/logout')
def logout():
    session.pop('member', None)
    return redirect(url_for('home'))

@app.route('/membership', methods=['GET'])
def membership():
    return render_template('membership.html')

@app.route('/upgrade_membership', methods=['GET', 'POST'])
def upgrade_membership(): 
    if 'member' not in session:
        return redirect(url_for('member_login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM members WHERE id = %s',
        (session['member'],)
    )
    member = cursor.fetchone()

    if request.method == 'POST':
        new_package = request.form['package']
        cursor.execute(
            'UPDATE members SET package = %s WHERE id = %s',
            (new_package, session['member'])
        )
        mysql.connection.commit()

        flash('Membership upgraded successfully!')
        return redirect(url_for('member_home'))
    
    return render_template('upgrade_membership.html', member=member)

@app.route('/our-clubs')
def our_clubs():
    return render_template('our_clubs.html')

if __name__ == '__main__':
    app.run(debug=True)