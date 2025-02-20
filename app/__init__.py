from flask import Flask, request
from .config import Config, TestConfig
from flask_smorest import Api
from app.utils.logger import setup_logging
from app.utils.error_handler import handle_error
from app.routes.blueprints import bp


# @bp.after_request
# def set_cors(response):
#     origin = request.headers.get('Origin')
#     response.headers['Access-Control-Allow-Origin'] = origin # here you can specify the domains that you want to allow.
#     response.headers['Access-Control-Allow-Credentials'] = 'true' # here you can specify if you want to allow credentials (cookies, authorization headers, etc)
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE, OPTIONS' # here you can specify the methods that you want to allow
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization' # here you can specify the headers that you want to allow
#     return response

def create_app(config_name="default") -> Flask:
    app = Flask(__name__)

    # Load configuration based on environment
    if config_name == "testing":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    # OpenAPI / Swagger configuration
    app.config["API_TITLE"] = "Student API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = ""  # All OpenAPI routes without prefix
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"  # Swagger UI served at /docs
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Setup logging
    setup_logging(app)

    # Initialize API and register blueprint
    api = Api(app)
    api.register_blueprint(bp, url_prefix='/api')

    # Global CORS header addition for all routes
    @app.after_request
    def cors_headers(response):
        origin = request.headers.get('Origin') or '*'
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # Register error handlers
    app.register_error_handler(404, handle_error)
    app.register_error_handler(500, handle_error)

    return app


def register_error_handlers(app: Flask) -> None:
    # Your error handler logic (if not using the ones in utils/error_handler.py)
    pass
