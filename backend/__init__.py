from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('backend.cfg')
    cors.init_app(app, supports_credentials=app.config['SUPPORT_CREDENTIALS'],
                  origins=[app.config['ORIGIN']])
    db.init_app(app)
    migrate.init_app(app, db)

    from backend.example.endpoints import example
    app.register_blueprint(example)

    return app


from backend.models import *