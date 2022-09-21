from toolauth import app
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    DATABASE = os.environ.get("DB_URI") or "toolauth.db"
