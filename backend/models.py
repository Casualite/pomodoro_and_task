from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db=SQLAlchemy()
roles_users=db.Table('roles_users',db.Column('user_id',db.Integer(),db.ForeignKey('userLogin.id')),db.Column('role_id',db.Integer(),db.ForeignKey('role.id')))
class User(db.Model,UserMixin):
    __tablename__="userLogin"
    id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    password=db.Column(db.String,primary_key=False,nullable=False)
    email=db.Column(db.String)
    username=db.Column(db.String,unique=True,nullable=False)
    fs_uniquifier=db.Column(db.String(255),unique=True,nullable=False)
    active=db.Column(db.Boolean,nullable=False)
    child1=db.relationship('User_Tracker',cascade="all,delete",backref='userLogin')
    child2=db.relationship('Data',cascade="all,delete")
    roles=db.relationship('Role',secondary=roles_users,backref=db.backref('userLogin',lazy='dynamic'))

class Role(db.Model,RoleMixin):
    __tablename__="role"
    id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    name=db.Column(db.String(80),unique=True)
    description=db.Column(db.String(255))  

class Tracker(db.Model):
    __tablename__="tracker"
    ID=db.Column(db.String,primary_key=True,nullable=False,autoincrement=False)
    Name=db.Column(db.String,primary_key=False,nullable=False)
    TrackerType=db.Column(db.String,primary_key=False,nullable=False)
    Settings=db.Column(db.String,primary_key=False,nullable=True)
    Units=db.Column(db.String,primary_key=False,nullable=True)
    Description=db.Column(db.String,nullable=True)
    child1=db.relationship('User_Tracker',cascade="all,delete")
    child2=db.relationship('Data',cascade="all,delete")

class User_Tracker(db.Model):
    __tablename__="usertrackers"
    user_id=db.Column(db.Integer,db.ForeignKey(User.id))
    ID=db.Column(db.String,db.ForeignKey(Tracker.ID))
    Count=db.Column(db.Integer,primary_key=True,autoincrement=True)
    child1=db.relationship('Data',cascade="all,delete")

class Data(db.Model):
    __tablename__="data"
    EntryNo=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey(User.id))
    Tracker_ID=db.Column(db.String,db.ForeignKey(Tracker.ID))
    Time=db.Column(db.DateTime)
    Description=db.Column(db.Integer)
    usertrackers_count=db.Column(db.Integer,db.ForeignKey(User_Tracker.Count))
    note=db.Column(db.String)
    