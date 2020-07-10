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
| Logging  |    TODO    |    TODO    |   N/A    |
| Caching  |    ✔️    |    Support for caching endpoints and memoizing functions    |   Flask-Caching    |
| Config  |    ✔️    |    TODO    |   N/A    |
| ORM  |    ✔️    |    Database ORM layer for easy, programmatic database usage   |   Flask-SQLAlchemy (SQLAlchemy)    |
| Migrations  |    ✔️    |    Handles database changes    |   Flask-Migrate (alembic)    |
| Auto-documentation  |    TODO    |    TODO    |   N/A    |
| Admin Dashboard  |    TODO    |    TODO    |   N/A    |
| Utils  |    TODO    |    TODO    |   N/A    |

## Why Flask?
Because I like Flask; it's flexible and powerful.