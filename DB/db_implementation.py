from pathlib import Path
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from os import path

NAME_DB = 'sqlite3.db'
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_DB = path.join(BASE_DIR,NAME_DB)

Base = declarative_base()

class Activity(Base):
    __tablename__ = 'activity'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    activity = Column('activity',String)
    type = Column('type', String)
    participants = Column('participants', Integer)
    price = Column('price', Float)
    link = Column('link', String)
    key = Column('key', String)
    accessibility = Column('accessibility', Float)

    def __init__(self,activity,type,participants,price,link,key,accessibility):
        self.activity = activity
        self.type = type
        self.participants = participants
        self.price = price
        self.link = link
        self.key = key
        self.accessibility = accessibility

    def __repr__(self):
        return f'activity -> "{self.activity}", type -> "{self.type}", participants -> {self.participants}' \
               f'price -> {self.price}, link -> "{self.link}", key -> "{self.key}", accessibility -> "{self.accessibility}"'

class Activity_DB:
    def __init__(self):
        self.session = None
        self.engine = None

    def create_field(self,  activity: dict):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        activity_field = Activity(**activity)

        self.session.add(activity_field)
        self.session.commit()

    def get_latest_entries(self,quantity=5):
        if not self.session:
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

        latest_entries = self.session.query(Activity).order_by(Activity.id.desc()).limit(quantity).all()
        latest_entries = '\n'.join([str(entire) for entire in latest_entries])
        return latest_entries
    def connect(self):
        self.engine = create_engine(f'sqlite:///{PATH_DB}')
        return self

    def close(self):
        if self.engine:
            self.engine.dispose()
        self.session = None
        self.engine = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


