from sqlalchemy import engine, select, func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.engine.create import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, session

URL = "postgresql+psycopg2://postgres:root@localhost/suppliers"

engine = create_engine(URL)

def create_tables_with_data_transaction(engine):

    userList = [
        User(id=None, first_name = 'Andrey', last_name = 'Volkov', email = 'andrey.volkov@yandex.ru'),
        User(id=None, first_name = 'Maksim', last_name = 'Ivanov', email = 'maks_ivanov@gmail.com'),
        User(id=None, first_name = 'Alexei', last_name = 'Medvedev', email = None)
    ]

    roomList = [
        Room(id=None, number = 103, floor = 1, owner_id = 1),
        Room(id=None, number = 104, floor = 1, owner_id = 1),
        Room(id=None, number = 211, floor = 2, owner_id = 3)
    ]

    session = Session(engine)
    with session.begin():
        Base.metadata.create_all(engine)
        session.add_all(userList)
        session.add_all(roomList)
    session.close()

def selectWithJoin(engine):

    session = Session(engine)
    with session.begin():
        result = session.query(User.first_name, User.last_name, User.email, func.count()).join(User.rooms).group_by(User.id)
        print(result.all())
    session.close()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    rooms = relationship("Room")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

create_tables_with_data_transaction(engine)
selectWithJoin(engine)