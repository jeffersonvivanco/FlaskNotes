# FlaskNotes

Flask is a small framework by most standards, small enough to be called a "microframework." Flask was designed as an
extensible framework from the ground up; it provides a solid core with the basic services, while *extensions* provide
the rest. Because you can pick and choose the extension packages you want, you end up with a lean stack that has no
bloat and does exactly what you need.

Flask has 2 main dependencies. The routing, debugging, and Web Server Gateway Interface (WSGI) subsystems come from
Werkzeug, while template support is provided by Jinja2. Werkzeug and Jinja2 are authored by the core developer of Flask.

## Basic app structure

### The request-response cycle

#### Application and request contexts
When Flask receives a request from a client, it needs to make a few objects available to the view function that will handle
it. A good example is the *request object*, which encapsulates the HTTP request sent by the client. To avoid cluttering
view functions with lots of arguments that may or may not be needed, Flask uses *contexts* to temporarily make certain
objects globally accessible.

Note how in the view function `request` is used as if it was a global variable. In reality, `request` cannot be a global
variable if you consider that in a multithreaded server the threads are working on different requests from different clients
at the same time, so each thread needs to see a different object in `request`.  Contexts enable Flask to make certain
variables globally accessible to a thread without interfering with the other threads.

A thread is the smallest sequence of instructions that can be managed independently. It is common for a process to have
multiple active threads, sometimes sharing resources such as memory or file handles. Multithreaded web servers start a
pool of threads and select a thread from the pool to handle each incoming request.

There are 2 contexts in Flask: the *application context* and the *request context*.

| variable name | context | description
| --- | --- | --- |
| `current_app` | Application context | The application instance for the active application. |
| `g` | Application context | An object that the app can use for temp storage during the handling of a req. This var is reset with each req. |
| `request` | Request context | The req object, which encapsulates the contents of a HTTP req sent by the client. |
| `session` | Request context | The user session, a dict that the app can use to store values that are "remembered" between reqs. |

Flask activates (or pushes) the app and req contexts before dispatching a req and then removes them when the req is handled.

#### Request dispatching
When the app receives a req from a client, it needs to find what view function to invoke to service it. For this task,
Flask looks up the URL given in the request in the application's *URL map*, which contains a mapping of URLs to the
view functions that handle them. Flask builds this map using the `app.route` decorators or the equivalent nondecorator
version `app.add_url_rule()`. To see what the URL map in a Flask app looks like call, `app.url_map`

#### Request hooks
Sometimes it is useful to execute code before or after each request is processed. For example, at the start of each
request, it may be necessary to create a database connection, or authenticate the user making the request. Request hooks
are implemented as decorators. These are 4 hooks supported by Flask.

* `before_first_request`: register a function to run before the first request is handled
* `before_request`: register a function to run before each request
* `after_request`: register a function to run after each request, if no unhandled exceptions occurred.
* `teardown_request`: register a function to run after each request, even if unhandled exceptions occurred.

A common pattern to share data between request hook functions and view functions is to use the `g` context variable.
For example, a `before_request` handler can load the logged in user from the database and store it in `g.user`. Later,
when the view function is invoked, it can access the user from there.

## Application programming interface
In recent years, there has been a trend in web applications to move more and more

## Deployment

### The heroku platform
The development web server that comes will Flask will perform poorly because it was not designed to run in a production
environment. 2 production-ready web servers that work well with Flask applications are Gunicorn and uWSGI.

Install -> `pip3 install gunicorn`

To run the app under Gunicorn, use the following command:
`gunicorn manage:app`

The `manage:app` argument indicates the package or module that defines the app to the left of the colon and the name
of the application instance inside that package on the right.














