from flask import Flask
from flask_cors import CORS
from backend.config import Config

cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    cors.init_app(app, supports_credentials=app.config['SUPPORTS_CREDENTIALS'],
                  origins=[app.config['ORIGIN']])

    from backend.example.endpoints import example
    app.register_blueprint(example)

    return app