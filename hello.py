from flask import Flask, render_template, session, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATAVASE_URI'] = \
    'mysql://musab:trash@localhost/database'+os.path.join(basedir, 'data.MySQL')
app.config['SQLALCHEMY_TRACK_MODIFACTIONS'] = False

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username


#class Role(db.Model):
    #...
    #users = db.relationship('User', backref='role')

#lass User(db.Model):
    #...
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
