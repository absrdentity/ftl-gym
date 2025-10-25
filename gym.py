from flask import Flask, jsonify, request, url_for, redirect, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET'])
def join_membership():
    return render_template('join.html')

@app.route('/membership', methods=['GET'])
def membership():
    return render_template('membership.html')

if __name__ == '__main__':
    app.run(debug=True)