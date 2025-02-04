import logging
import os
import json
from typing import Any, Dict
from flask import Flask

class CloudWatchFormatter(logging.Formatter):
    """Custom formatter for CloudWatch Logs"""
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            'level': record.levelname,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage()
        }
        
        if hasattr(record, 'props'):
            log_entry.update(record.props)

        return json.dumps(log_entry)

def setup_logging(app: Flask) -> None:
    """
    Setup logging for both local development and AWS Lambda environments.
    """
    # Set the base logging level
    app.logger.setLevel(logging.INFO)

    # Clear any existing handlers
    app.logger.handlers.clear()

    # Create handlers
    console_handler = logging.StreamHandler()
    
    # Use different formatters based on environment
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        formatter = CloudWatchFormatter()
    else:
        # Local development formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s'
        )
        
        # Add file handler only for local development
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    # Log startup message
    app.logger.info('Application startup')
