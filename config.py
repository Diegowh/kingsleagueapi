import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    def __init__(self) -> None:
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    
class ProductionConfig(Config):
    DEBUG = False
    

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1
    

class TestingConfig(Config):
    TESTING = True