# Template Backend

## Introduction

This is a template for a Flask based backend. It's structured as, but not limited to,
a REST API. It's purpose is to bootstrap backend projects with all the necessary
requisites of a good backend and alleviate the developer from some of the
typical burdens associated with backend development.


## Getting Started
Note that this template contains example endpoints, models, tests, etc.,
which serve to demonstrate each feature of the backend. You will most likely
not need any of the pre-created models or endpoints, but they serve as a good
starting point for your specific project.

### Pre-requisites
- Python 3
- PostgreSQL drivers (not strictly necessary if you choose a different database)

### Steps
1. Clone this repository
2. Create a virtual environment
3. Install requirements
4. Create a PostgreSQL database
5. Create a `config.py` file and populate it with your config
6. Run `flask db upgrade` to update the database with the example models 
    - alternatively, first create your own models in `models.py` and delete the existing migrations
7. Run the app
 

## REST API ✔️
Using Flask-Rebar we can easily create robust endpoints with defined input and output
schemas. Despite the heavy focus on creating REST endpoints, we still retain the 
ability to render templates.

## Auth 🔄
Flask-Rebar provides a basic authenticator and support for custom ones. As a starting point,
this template comes with a default header authenticator that is enabled for all endpoints.

All requests must be sent with the `X-AUTH-API-KEY` header, where its value must match
the `AUTH_KEY` defined in your `config.py`. The names for the header and the key variable
are also configurable.

##### TODO
- disable auth requirements whilst in dev (?)
- custom authenticator with scope support
## Error Handling ✔️
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

## Logging  ✔️
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

## Caching  ✔️
Support for caching endpoints and memoizing functions using Flask-Caching.

## Scheduler ✔️
A scheduler lets you schedule code in your app to be run periodically or at specific times using Flask-APScheduler.
The current example adds a job during app creation which is defined in `config.py`.
Since the tasks run outside of any request context, the example demonstrates how you would
access the database via the application context. 

The scheduler's default timezone is set to `UTC`. Jobs are configured to be stored in your database.
##### TODO
- Protect the scheduler endpoints (if they are exposed)

## Config ✔️
Create a `config.py` file under your app module. In this case under `backend`.
This file is picked up when you create the app and instantiates a number of 
important variables required for the app to work. It's the place where you will
store secrets, like database passwords, so **never commit this file to your repository.**

```python
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# FLASK
APP_HOST = "localhost"
APP_PORT = 5000
SECRET_KEY = "<your_secret_key>"

# AUTH
AUTH_HEADER = "X-AUTH-API-KEY"
AUTH_KEY = "<your_auth_key>"
AUTH_ALLOWED_CLIENT = "client"

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
		'func'            : 'backend.jobs.example_job:print_number_of_users',
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

## ORM ✔️
Database ORM layer for easy, programmatic database usage, using Flask-SQLAlchemy.

## Migrations ✔️
Handles database changes using Flask-Migrate.

## Tests 🔄
Example tests for app creation, endpoints, etc.

##### TODO
- Add database mocking to test examples
- Add auth tests

## Coverage ❌

## Auto-documentation 🔄
Flask-Rebar provides support for generating docs based on the OpenAPI (Swagger) spec.
The Swagger endpoints have been disabled since they shouldn't be accessible in production
for most projects.
##### TODO
- separate documentation generation from app creation
- documentation generation should be part of the CI/CD pipeline

## Admin Dashboard ❌
An admin dashboard allows for non-programmatic access to your backend, allowing
you to easily make configuration changes and monitor your application in real-time.

##### Proposed features:
- separate authentication from main app
- interact with database models
- preview logs
- metrics
- access scheduler API

## Utils ❔
I might include some useful functions in this template if I can think of anything
generic enough that deserves a place here.