from flask import Flask


def create_app():
    app = Flask(__name__)

    from backend.example.endpoints import example
    app.register_blueprint(example)

    return app