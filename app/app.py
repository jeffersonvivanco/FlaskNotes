from flask import Flask, render_template, redirect, request, url_for, make_response, abort
import os


# All Flask applications must create an application instance.
# The web server passes all requests it receives from clients to this object for handling, using a protocol called
# Web Server Gateway Interface (WSGI)
app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def index():
    return redirect('index.html')


@app.route('/user')
def user():
    # default status code is 200, you can change it by passing a second argument
    # third argument is a dictionary of headers that are added to the HTTP response
    return '<h1>Not found</h1>', 400


# note: dynamic components can also be defined with a type. For example /user/<int:id>, flask supports int, float & path
# using response object
@app.route('/user/<username>')
def user_with_name(username):
    user_agent = request.headers.get('User-Agent')
    response = make_response('<h1>Hello {}</h1><h2>user-agent: {}'.format(username, user_agent))
    response.set_cookie('answer', '32')
    return response


# A redirect is typically indicated with a 302 resp status code and the URL to redirect to given in a Location header.
# Redirects are commonly used with web forms
@app.route('/hello/<username>')
def hello(username):
    return redirect('/user/{}'.format(username))


# abot() is used for error handling, it raises an exception
@app.route('/bye')
def not_found():
    abort(404)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    # server startup, stop app by hitting CTRL - C
    # During development it is convenient to enable debug mode, which activates the debugger and the reloader
    # The web server provided by Flask is not intended for production use.
    app.run(host='0.0.0.0', port=port, debug=True)
