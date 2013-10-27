from sqlalchemy import create_engine
from schema import update_schema, content_facebook
from config import db

def get_connection_string():
    if db.get('type') == 'mysql':
        settings = db.get('mysql')
        host = settings.get('host')
        user = settings.get('user')
        db_name = settings.get('db_name')
        password = settings.get('pass')

        return "mysql://%s:%s@%s/%s?charset=utf8" % (user, password, host, db_name)

    elif db.get('type') == 'sqlite':
        return "sqlite:///memory"


def get_engine():
    return create_engine(get_connection_string(), echo=db.get('echo'))


def get_connection(engine):
    return engine.connect()

engine = get_engine()
conn = get_connection(engine)
