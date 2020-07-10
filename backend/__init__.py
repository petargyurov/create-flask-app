import os

from flask import Flask, json
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException, InternalServerError

cache = Cache()
cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')

	cache.init_app(app, config=app.config['CACHE_CONFIG'])
	cors.init_app(app, supports_credentials=app.config['SUPPORT_CREDENTIALS'],
				  origins=[app.config['ORIGIN']])
	db.init_app(app)
	migrate.init_app(app, db)

	from backend.example.endpoints import example
	app.register_blueprint(example)

	# format errors as JSON responses
	@app.errorhandler(Exception)
	def handle_exception(e):
		if not isinstance(e, HTTPException):
			if os.environ['FLASK_ENV'] == 'production':
				e = InternalServerError()
			else:
				raise e

		response = e.get_response()
		response.data = json.dumps({
			"code"       : e.code,
			"name"       : e.name,
			"description": e.description,
		})
		response.content_type = "application/json"
		return response

	return app


from backend.models import *
