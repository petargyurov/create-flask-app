import logging
import os
from logging.config import dictConfig

from flask import Flask, json
from flask_apscheduler import APScheduler
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException, InternalServerError

from backend.logger import config

dictConfig(config)
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
	# scheduler.start()

	from backend.example.endpoints import example
	app.register_blueprint(example)

	# turn off werkzeug logging below the error level to (see README)
	log = logging.getLogger('werkzeug')
	log.setLevel(logging.ERROR)

	# format errors as JSON responses
	@app.errorhandler(Exception)
	def handle_exception(e):
		if not isinstance(e, HTTPException):
			log_msg = repr(e)
			if os.environ['FLASK_ENV'] == 'production':
				e = InternalServerError()
			else:
				desc = repr(e)
				e = InternalServerError()
				e.description = desc
		else:
			log_msg = e.description

		response = e.get_response()
		response.data = json.dumps({
			"code"       : e.code,
			"name"       : e.name,
			"description": e.description,
		})
		response.content_type = "application/json"
		app.logger.error(f"{response.status} | {log_msg}")
		return response

	# log non-errors
	@app.after_request
	def log_request(response):
		if response.status[0] not in ['4', '5']:
			app.logger.info(response.status)
		return response

	return app


from backend.models import *
