from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def hello_world():
    return render_template('index.html', name='Jeff')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return redirect('/')
    username = request.form['username']
    return redirect(url_for('home', username=username))


@app.route('/home/<username>')
def home(username):
    return render_template('home.html', username=username)


app.run()
