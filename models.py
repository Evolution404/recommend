from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    context = db.Column(db.Text, nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('questions'))


class Answer(db.Model):
    __tablename__ = 'answer'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    context = db.Column(db.Text, nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship('Question', backref=db.backref('answers'))
    author = db.relationship('User', backref=db.backref('answers'))
