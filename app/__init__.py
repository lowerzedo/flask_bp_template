from flask import Flask
from flask_cors import CORS
from app.api import api_bp
from app.helpers.error_handler import handle_error

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Register error handler
    app.register_error_handler(Exception, handle_error)
    
    return app