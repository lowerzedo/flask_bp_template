import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    
    # MySQL configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'database')
    
    # Oracle configuration (placeholder)
    ORACLE_HOST = os.environ.get('ORACLE_HOST', 'localhost')
    ORACLE_PORT = int(os.environ.get('ORACLE_PORT', 1521))
    ORACLE_SERVICE = os.environ.get('ORACLE_SERVICE', 'orcl')
    ORACLE_USER = os.environ.get('ORACLE_USER', 'user')
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD', 'password')
    
    # MSSQL configuration (placeholder)
    MSSQL_SERVER = os.environ.get('MSSQL_SERVER', 'localhost')
    MSSQL_USER = os.environ.get('MSSQL_USER', 'user')
    MSSQL_PASSWORD = os.environ.get('MSSQL_PASSWORD', 'password')
    MSSQL_DB = os.environ.get('MSSQL_DB', 'database')
