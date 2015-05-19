from flask_application.models import db, FlaskDocument


class Company(FlaskDocument):
    updated = db.DateTimeField()
    created = db.DateTimeField()
    symbol = db.StringField(max_length=8)
    cid = db.DecimalField()
    name = db.StringField(max_length=256)
    price = db.ReferenceField('Price')

class Price(FlaskDocument):
    date = db.DateTimeField()
    price = db.FloatField()
    cid = db.ReferenceField(Company)

class DBState(FlaskDocument):
    updateid = db.DecimalField()
    date = db.DateTimeField()
    count = db.DecimalField()
