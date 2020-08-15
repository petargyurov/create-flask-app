# Template Backend

## Introduction

This is a template for a Flask based backend. It's structured as, but not limited to,
a REST API. It's purpose is to bootstrap backend projects with all the necessary
requisites of a good backend and alleviate the developer from some of the
typical burdens associated with backend development.

## Features
Click on each feature to read more about it.

| Feature  | Status  |  Description |  Library |
|---|---|---|---|
| REST API  |    ✔️    |    Support for input and output schemas    |   Flask-Rebar    |
| Auth  |    TODO    |    TODO    |   N/A    |
| Error Handling  |    ✔️   |    Customisable JSON error responses    |   Flask-Rebar    |
| Logging  |    ✔️  |    Pre-configured, enriched logging with a console handler and a rotating file handler    |   Default Python Logging Library    |
| Caching  |    ✔️    |    Support for caching endpoints and memoizing functions    |   Flask-Caching    |
| Scheduler  |    ✔️   |    A scheduler lets you schedule code in your app to be run periodically or at specifc times.    |   Flask-APScheduler (APScheduler)    |
| Config  |    ✔️    |    A data file used to configure your app. It separates sensitive data from your codebase.    |   Flask    |
| ORM  |    ✔️    |    Database ORM layer for easy, programmatic database usage   |   Flask-SQLAlchemy (SQLAlchemy)    |
| Migrations  |    ✔️    |    Handles database changes    |   Flask-Migrate (alembic)    |
| Tests  |    In Progress    |    Example tests for app creation, endpoints, etc. Uses a mock database.    |   pytest-flask (pytest)    |
| Coverage  |    TODO    |    TODO    |   N/A    |
| Auto-documentation  |    ✔️    |    Automatically generate documentation for your endpoints using the OpenAPI spec.    |   Flask-Rebar    |
| Admin Dashboard  |    TODO    |    TODO    |   N/A    |
| Utils  |    TODO    |    TODO    |   N/A    |


## Getting Started

### Create the config file
Create a `config.py` file under your app module. In this case under `backend`.
This file is picked up when you create the app and instantiates a number of 
important variables required for the app to work. It's the place where you will
store secrets, like database passwords, so **never commit this file to your repository.**

Here is a the minimal requirement for what your config file should look like. 

```python
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# FLASK
APP_HOST = "localhost"
APP_PORT = 5000
SECRET_KEY = "<your_secret_key>"

# CACHE
CACHE_CONFIG = {
	"CACHE_TYPE"           : "simple",
	"CACHE_DEFAULT_TIMEOUT": 60,
}

# CORS
ALLOWED_ORIGINS = ["localhost"]

# DATABASE
DATABASE_USER = "backend"
DATABASE_PASSWORD = "<your_database_password>"
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_NAME = "backend"
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SCHEDULER
JOBS = [
	{
		'id'              : 'example',
		'func'            : 'backend.tasks.example_task:print_number_of_users',
		'trigger'         : 'interval',
		'seconds'         : 10,
		'replace_existing': True,
	},
]
SCHEDULER_TIMEZONE = 'UTC'
SCHEDULER_JOBSTORES = {
	'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
}
SCHEDULER_JOB_DEFAULTS = {
	'coalesce'     : False,
	'max_instances': 1
}
SCHEDULER_API_ENABLED = False
```

## Error Handling

When your application raises an error, it sends a JSON response with the 
appropriate status code. Non-HTTP errors are converted to `InternalServerError`.
See the Flask-Rebar [docs on errors](https://flask-rebar.readthedocs.io/en/latest/quickstart/basics.html#errors) for more info.

##### Example `Forbidden` response
In this example we have provided a custom error message and some optional additional data. 

```json
{
  "msg": "You can't do that!", 
  "reason": "missing credentials"
}
```

## Logging

Logging is a crucial part of any application. The template comes pre-configured 
with two handlers:

- console output
- (rotating) file output 

The default output looks like this:
```
2020-07-23 16:28:35,502 | ERROR | example.endpoints.get_user::27 | GET | /user | id=4 | 404 NOT FOUND | User with ID=4 not found in database
2020-07-23 16:29:02,868 | INFO | backend.__init__.log_request::66 | GET | /user | id=1 | 200 OK
```
which is based on this format:
```
datetime | level | location_in_code | method | path | query_params | status | description
```

If you don't like something about this format you can easily change it in the config that is 
defined in `logger.py`

#### Log Enrichment

The `CustomFormatter` class allows us to get more information about errors and other events
that occur in our app, in particular, the location in code of each error. You can extend this
class to add other information, for example, adding the user agent.

Note that not all log events that come through will come from requests. As such, you won't
always have the request context; in these cases it is important to still pass a value
for all fields that the formatter expects.

#### A Note on the Werkzeug Logger
The default `werkzeug` logger is hardcoded and difficult to turn off or re-format; for this
reason it is "softly" turned off, i.e.: its level is set to `ERROR`. This is to avoid
duplicate logging and to avoid a more complex formatting solution. If you wish to fully
turn off or to properly customise the output of the default Werkzeug logger, you can
create a custom request handler that inherits from `WSGIRequestHandler` and overrides
the `_log` method. 

```python
from werkzeug.serving import WSGIRequestHandler, _log


class MyRequestHandler(WSGIRequestHandler):
    def log(self, type, message, *args):
        pass  # or use _log to pass whatever you want
```
Then pass this to your application
```python
app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'], request_handler=MyRequestHandler)
```