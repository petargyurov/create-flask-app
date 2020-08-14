import logging
from logging.config import dictConfig

from flask import Flask
from flask_apscheduler import APScheduler
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_rebar import Rebar
from flask_sqlalchemy import SQLAlchemy

from backend.logger import config

dictConfig(config)

rebar = Rebar()
registry = rebar.create_handler_registry()
cache = Cache()
cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()


def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')

	cache.init_app(app, config=app.config['CACHE_CONFIG'])
	cors.init_app(app, origins=app.config['ALLOWED_ORIGINS'])
	db.init_app(app)
	migrate.init_app(app, db)

	scheduler.init_app(app)
	scheduler.start()

	# IMPORTANT: import the views before rebar initialisation
	from backend.example.endpoints import get_user
	rebar.init_app(app)

	# suppress werkzeug logging (see README)
	log = logging.getLogger('werkzeug')
	log.setLevel(logging.ERROR)

	# log with our app logger
	@app.after_request
	def log_request(response):
		app.logger.info(response.status)
		return response

	return app


from backend.models import *
