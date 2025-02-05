import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "my_secret_key")
    DEBUG = os.environ.get("DEBUG", "True") == "True"

    # PAGINATION_PER_PAGE = 20
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class TestConfig:
    TESTING = True
