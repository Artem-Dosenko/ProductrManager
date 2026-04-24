from peewee import *

db = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Company(BaseModel):
    name = TextField()
    password = TextField()

class Product(BaseModel):
    name = TextField()
    price = FloatField()
    category = TextField()
    company = ForeignKeyField(Company, backref='products')


def init_db():
    db.connect()
    db.create_tables([Company, Product])