#!/usr/bin/python3

#redis server
#sudo service redis-server start
#redis-server --port 6380
#redis-cli -p 6380 
#mailhog "localhost:8025"
#celery
#cd ./src/api
#celery -A main.celery worker -l info
#celery -A main.celery beat --max-interval 1 -l info
from models import db
from flask import Flask
from flask_cors import CORS
from API import api,cache
from flask_security import Security, SQLAlchemySessionUserDatastore
from models import User,Role
import workers
from flask import current_app as app
from tasks import make_csv
app=Flask(__name__)
app.app_context().push()
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///projectDB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER']="AUTHENTICATION-TOKEN"
app.config['SECRET_KEY']="apple" 
app.config['SECURITY_PASSWORD_HASH']="bcrypt" 
app.config['SECURITY_PASSWORD_SALT']="banana" 
app.config['SECURITY_REGISTERABLE'] = False
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_UNAUTHORIZED_VIEW'] = None
app.config['SECURITY_USERNAME_ENABLE'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_USERNAME_ENABLE']=True
app.config['SECURITY_LOGIN_URL']='/get_token/login'
db.init_app(app)
with app.app_context():
    db.create_all()
api.init_app(app)
cache.init_app(app)
celery=workers.celery
celery.conf.update(
        broker_url = "redis://localhost:6380/1",
        result_backend = "redis://localhost:6380/2"
    )
celery.Task=workers.ContextTask

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)
@app.route("/make_csv/<int:user_id>/<ID>")
def func(user_id,ID):
    make_csv.apply_async([user_id,ID])
    
    
if (__name__=='__main__'):
        app.run(host='0.0.0.0',port=8800)

