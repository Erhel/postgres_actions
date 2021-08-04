from sqlalchemy import create_engine
from sqlalchemy.sql.schema import Column, Constraint, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import Integer, NULLTYPE, String
from config import config

URL = "postgresql+psycopg2://postgres:root@localhost/suppliers"

engine = create_engine(URL)
conn = engine.connect()
meta = MetaData()
users = Table(
    "users", meta, 
    Column("id", Integer, primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String),
    
)

rooms = Table(
    "rooms", meta,
    Column("id", Integer, primary_key=True),
    Column("number", Integer, nullable=False),
    Column("floor", Integer, nullable=False),
    Column("owner_id", Integer, ForeignKey('users.id'))
)

usersList = [
    {'first_name':'Andrey', 'last_name':'Volkov', 'email':'andrey.volkov@yandex.ru'},
    {'first_name':'Maksim', 'last_name':'Ivanov', 'email':'maks_ivanov@gmail.com'},
    {'first_name':'Alexei', 'last_name':'Medvedev', 'email':None}
]
roomsList = [
    {'number':103, 'floor':1, 'owner_id':1},
    {'number':104, 'floor':1, 'owner_id':1},
    {'number':211, 'floor':2, 'owner_id':3}
]

meta.create_all(engine)

conn.execute(users.insert(), usersList)
conn.execute(rooms.insert(), roomsList)