from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
import base64
from io import BytesIO #Converts data from Database into bytes

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    national_id = db.Column(db.String, nullable=False, unique=True)
    contact = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String, nullable=False)
    #-- File input is required here --#
    religion = db.Column(db.String, nullable=False)
    register_date = db.Column(db.Date, nullable=False)
    pob = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    no_of_child = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    education = db.Column(db.String, nullable=False)
    employer_id = db.Column(db.Integer, nullable=True)
    broker_id = db.Column(db.Integer, nullable=True)
    
    sent_1 = db.Column(db.Boolean, nullable=False)
    sent_2 = db.Column(db.Boolean, nullable=False)
    languages = db.Column(db.String, nullable=True)
    pport = db.Column(db.Boolean)
    
    #employer = db.relationship("employer", backref="employee", lazy=True)
    #broker = db.relationship("broker", backref="employee", lazy=True)
    #flight = db.relationship("flight", backref="employee", lazy=True)


    def add_passport(self, pass_no, poi, doi, exd):
        p = Passport(employee_id=self.id, pass_no=pass_no, place_of_issue=poi, date_of_issue=doi, date_of_expire=exd)
        db.session.add(p)
        self.pport = True
        db.session.commit()
    
    def add_grid(self, data, rendered_data):
        grid = GridContent(employee_id=self.id, data=data, rendered_data=rendered_data)
        db.session.add(grid)
        db.session.commit()
    
    def add_portrait(self, data, rendered_data):
        portrait = Portrait(employee_id=self.id, data=data, rendered_data=rendered_data)
        db.session.add(portrait)
        db.session.commit()

    def add_passpic(self, data, rendered_data):
        passpic = Passpic(employee_id=self.id, data=data, rendered_data=rendered_data)
        db.session.add(passpic)
        db.session.commit()

class Passport(db.Model):
    __tablename__ = "passport"
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    pass_no = db.Column(db.String, unique=True)
    place_of_issue = db.Column(db.String, nullable=False)
    date_of_issue = db.Column(db.Date, nullable=False)
    date_of_expire = db.Column(db.Date, nullable=False)

class Employer(db.Model):
    __tablename__ = "employer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=True)
    national_id = db.Column(db.String(10), nullable=False, unique=True)
    register_date = db.Column(db.Date, nullable=False)

    def add_employee(self, employee_id):
        employee = Employee.query.get(employee_id)
        employee.employer_id = self.id 
        db.session.commit()


class Broker(db.Model):
    __tablename__ = "broker"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact = db.Column(db.String, nullable=False)
    national_id = db.Column(db.String, nullable=False, unique=True)
    register_date = db.Column(db.Date, nullable=False)

    def add_employee(self, employee_id):
        employee = Employee.query.get(employee_id)
        employee.broker_id = self.id 
        db.session.commit()

class GridContent(db.Model):
    __tablename__ = 'gridphoto'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    rendered_data = db.Column(db.Text, nullable=False)

class Portrait(db.Model):
    __tablename__ = 'portrait'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    rendered_data = db.Column(db.Text, nullable=False)

class Passpic(db.Model):
    __tablename__ = 'passpic'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    rendered_data = db.Column(db.Text, nullable=False)


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False