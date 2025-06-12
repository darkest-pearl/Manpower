from flask import Flask, render_template, request
from models import *
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://munira:trash@localhost:5432/flasky"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    db.create_all()
    today = datetime.datetime.now()
    employer = Employer(name='Tayseer Agency', national_id='1618', contact='002917453139', register_date=today)
    employer_handle = Employer(name='name', id='999999', national_id='0000', contact='12345', register_date=today)
    broker = Broker(name='Tayseer Agency', national_id='1618', contact='002917451322', register_date=today)
    broker_handle = Broker(name='name', id='999999', national_id='0000', contact='123', register_date=today)
    db.session.add(broker)
    db.session.add(broker_handle)
    db.session.add(employer)
    db.session.add(employer_handle)
    
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
