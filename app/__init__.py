from flask import Flask, jsonify

from app.config import AppConfig
from app.controllers import *
from app.extends.error import HttpError
from app.extensions import cors, redis_client


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    register_errorhandler(app)
    register_blueprints(app)
    register_extensions(app)

    return app


def register_errorhandler(app: Flask):
    @app.errorhandler(HttpError)
    def handle_http_error(error: HttpError):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(offiaccount_bp)


def register_extensions(app: Flask):
    cors.init_app(app)
    redis_client.init_app(app)
