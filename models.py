from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    roles = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__(self, name=None):
        self.name = name

class Demo(Base):

    __tablename__ = "Demo table"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    demo_name = db.Column(db.String(120), unique=True)
    device_details = db.Column(db.String(120), unique=True)
    status = db.Column(db.Integer, unique=True)
    duration = db.Column(db.Integer, unique=True)
    description = db.Column(db.String(120), unique=True)
    start_date_time = db.Column(db.String(120), unique=True)

# Create tables.
Base.metadata.create_all(bind=engine)
