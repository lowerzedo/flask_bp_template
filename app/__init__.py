from flask import Flask
from .config import Config
from .routes.blueprint import blueprint
from .utils.logger import setup_logging

def create_app(config_class=Config) -> Flask:
    """
    Create and configure the Flask application.

    :param config_class: Configuration class to use.
    :return: Configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Setup logging
    setup_logging(app)

    # Register Blueprints
    app.register_blueprint(blueprint, url_prefix='/example')

    # Register error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app: Flask) -> None:
    """
    Register custom error handlers for the Flask app.

    :param app: Flask application instance.
    """
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
