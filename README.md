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
| REST API  |    ✔️    |    Slight modification on top of Flask's usual Blueprint object to allow for easy declaration of input and output schemas    |   Flask, Marshmallow, Webargs    |
| Auth  |    TODO    |    TODO    |   N/A    |
| Error Handling  |    ✔️   |    Customisable JSON error responses with obfuscation for non-HTTP errors in a production environment    |   Flask    |
| Logging  |    ✔️  |    Pre-configured, enriched logging with a console handler and a rotating file handler    |   Default Python Logging Library    |
| Caching  |    ✔️    |    Support for caching endpoints and memoizing functions    |   Flask-Caching    |
| Scheduler  |    ✔️   |    A scheduler lets you schedule code in your app to be run periodically or at specifc times.    |   Flask-APScheduler (APScheduler)    |
| Config  |    ✔️    |    TODO    |   N/A    |
| ORM  |    ✔️    |    Database ORM layer for easy, programmatic database usage   |   Flask-SQLAlchemy (SQLAlchemy)    |
| Migrations  |    ✔️    |    Handles database changes    |   Flask-Migrate (alembic)    |
| Auto-documentation  |    TODO    |    TODO    |   N/A    |
| Admin Dashboard  |    TODO    |    TODO    |   N/A    |
| Utils  |    TODO    |    TODO    |   N/A    |

## Why Flask?
Because I like Flask; it's flexible and powerful.

## Error Handling

When your application raises an error, it sends a custom JSON response with the 
appropriate status code. An error response has three fields:

- `code`: the response status
- `description`: the error description (can be provided when you `raise` and error or left to the default)
- `name`: the name/type of the error

Non-HTTP errors are converted to `InternalServerError`.
The description for non-HTTP errors **is only shown in a development environment.** 
Production environments will simply output the default `InternalServerError` description.

##### Example `NotFound` response
In this example we have provided a custom error message. If we hadn't, the default 404 description would be used. 
```json
{
  "code": 404, 
  "description": "User does not exist!", 
  "name": "Not Found"
}
```

##### Example `ZeroDivisionError` response in a *development* environment
It is useful to know the actual error during development
```json
{
  "code": 500, 
  "description": "ZeroDivisionError('division by zero')", 
  "name": "Internal Server Error"
}

```
##### Example `ZeroDivisionError` response in a *production* environment
The same error as above will look like this in production
```json
{
  "code": 500, 
  "description": "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.", 
  "name": "Internal Server Error"
}
```


## Logging

Logging is a crucial part of any application. The template comes pre-configured 
with two handlers:

- console output
- (rotating) file output 

The default output looks like this:
```python
2020-07-23 16:28:35,502 | ERROR | example.endpoints.get_user::27 | GET | /user | id=4 | 404 NOT FOUND | User with ID=4 not found in database
2020-07-23 16:29:02,868 | INFO | backend.__init__.log_request::66 | GET | /user | id=1 | 200 OK
```
which is based on this format:
```python
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