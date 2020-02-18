import os

basedir = os.getcwd()


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,"tthelperdev.db")}'


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,"tthelpertest.db")}'


# should be able to replace postgres uri with password and username that comes as a env variable
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,"tthelperprod.db")}'


app_environment = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}

