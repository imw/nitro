from flask_application.models import db, FlaskDocument


class Company(FlaskDocument):
    updated = db.DateTimeField()
    created = db.DateTimeField()
    symbol = db.StringField(max_length=8,unique=True)
    cid = db.DecimalField(unique=True)
    name = db.StringField(max_length=256,unique=True)

class Price(FlaskDocument):
    date = db.DateTimeField()
    price = db.FloatField()
    company = db.ReferenceField(Company)
