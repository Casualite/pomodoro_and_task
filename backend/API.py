from datetime import datetime,timedelta
from xmlrpc.client import Boolean
from sqlalchemy import func
from models import db,User,Tracker,User_Tracker,Data
from flask_restful import Resource, marshal_with,reqparse,fields
from werkzeug.exceptions import HTTPException
from flask import make_response
from flask_restful import Api
import json
from flask_security import auth_required
import secrets
from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379'})
api=Api()
class NotFoundError(HTTPException):
    def __init__(self,response,description):
            self.response=make_response(description,response)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code,error_code,error_message):
        message={"error_code": error_code,"error_message": error_message}
        self.response=make_response(json.dumps(message),status_code)

login=reqparse.RequestParser()
login.add_argument('username')
login.add_argument('password')
login.add_argument('email')
login.add_argument('active',type=Boolean)
login_fields={"id":fields.Integer,"username":fields.String,"password":fields.String,"active":fields.Boolean,"fs_uniquifier":fields.String,"email":fields.String}
class LoginAPI(Resource):
    @cache.memoize(10)
    @marshal_with(login_fields)
    def get(self,user):
        s=User.query.filter_by(username=user).first()
        if(s==None):
            raise NotFoundError(404,"user not found")
        return(s)
    
    @marshal_with(login_fields)
    def post(self):
        args=login.parse_args()
        user=args.get('username')
        password=args.get('password')
        if(user[0].isnumeric() or password[0].isnumeric() or " " in user or " " in password):
            raise BusinessValidationError(400,'LOGIN001','Invalid Username or Password!')
        s=User.query.filter_by(username=user).first()
        if(s==None):
            email=args.get('email')
            s=User(username=user,password=password,email=email,fs_uniquifier=secrets.token_hex(10),active=True)
            db.session.add(s)
            db.session.commit()
            return(s,201)
        elif(password!=s.password or password==None):
            raise BusinessValidationError(400,'LOGIN002','Wrong Password!')
        else:
            s.active=True
            db.session.commit()
            return(s,200)

    @auth_required("token")   
    @marshal_with(login_fields)
    def put(self,user):
        args=login.parse_args()
        password=args.get('password');active=args.get('active')
        if(password[0].isnumeric() or " " in password):
            raise BusinessValidationError(400,'LOGIN001','Invalid Password!')
        s=User.query.get(int(user))
        if(s==None):
            raise NotFoundError(404,'User to be modified not found')
        s.password=password
        s.active=active
        s.fs_uniquifier=secrets.token_hex(10)
        db.session.commit()
        return(s,200)

    @auth_required("token")
    @marshal_with(login_fields)
    def delete(self,user):
        s=User.query.get(int(user))
        if(s==None):
            raise NotFoundError(404,'not found')
        db.session.delete(s)
        db.session.commit()
        return(s,200)
api.add_resource(LoginAPI,"/api/login/<user>","/api/login/")

tracker=reqparse.RequestParser()
tracker.add_argument('Name')
tracker.add_argument('TrackerType')
tracker.add_argument('Description')
tracker.add_argument('settings')
tracker.add_argument('units')
Tracker_fields={"ID":fields.String,"Name":fields.String,"TrackerType":fields.String,"Description":fields.String,"Settings":fields.String,"Units":fields.String}
class TrackerAPI(Resource):
    @marshal_with(Tracker_fields)
    def get(self,ID):
        s=Tracker.query.get(ID)
        if(s==None):
            raise NotFoundError(404,"Tracker not found")
        return(s)

    @auth_required("token")
    @marshal_with(Tracker_fields)
    def post(self,ID):
        args=tracker.parse_args()
        Name=args.get('Name');TrackerType=args.get('TrackerType');Settings=args.get('settings');units=args.get('units');Description=args.get('Description')
        s=Tracker.query.all()
        if(len(s)==0):
            counts=0
        else:
            counts=db.session.query(func.max(User_Tracker.Count)).scalar()
        db.session.add(User_Tracker(user_id=int(ID),ID=Name+str(counts+1)))
        s=Tracker(ID=Name+str(counts+1),Name=Name,TrackerType=TrackerType,Settings=Settings,Units=units,Description=Description)
        db.session.add(s)
        db.session.commit()
        return(s,201)
    @auth_required("token")
    @marshal_with(Tracker_fields)
    def put(self,ID):
        args=tracker.parse_args()
        Name=args.get('Name')
        TrackerType=args.get('TrackerType')
        Settings=args.get('settings')
        units=args.get('units')
        Description=args.get('Description')
        s=Tracker.query.get(ID)
        if(s==None):
            raise BusinessValidationError(404,"Tracker001","ID not found")
        s.Name=Name;s.TrackerType=TrackerType;s.Settings=Settings;s.Units=units;s.Description=Description
        db.session.commit()
        return(s,201)
    @auth_required("token")   
    def delete(self,ID):
        s=Tracker.query.get(ID)
        if(s==None):
            raise NotFoundError(404,'Tracker not found')
        db.session.delete(s)
        db.session.commit()
        return(200)
api.add_resource(TrackerAPI,"/api/Tracker/<ID>")

userTracker_fields={"ID":fields.String,"user_id":fields.Integer,"count":fields.Integer}
class userTrackerAPI(Resource):
    @auth_required("token")
    @cache.memoize(1)
    @marshal_with(userTracker_fields)
    def get(self,user):
        s=User_Tracker.query.filter_by(user_id=user).all()
        if(len(s)==0):
            raise NotFoundError(404,"user not found")
        return(s)
    @auth_required("token")
    def delete(self,user,ID):
        s=Tracker.query.filter_by(user_id=user,ID=ID).first()
        if(s==None):
            raise NotFoundError(404,"user not found")
        db.session.delete(s)
        db.session.commit()
api.add_resource(userTrackerAPI,"/api/userTracker/<int:user>","/api/userTracker/<int:user>/<ID>")

data=reqparse.RequestParser()
data.add_argument('Description')
data.add_argument('note')
data.add_argument('Time')
data_fields={"EntryNo":fields.Integer,"user_id":fields.Integer,"Tracker_ID":fields.String,"Time":fields.DateTime,"Description":fields.Integer,"note":fields.String,"usertrackers_count":fields.Integer}
class DataAPI(Resource):
    @auth_required("token")
    @marshal_with(data_fields)
    def get(self,Eno):
        s=Data.query.get(Eno)
        if(s==None):
            raise NotFoundError(404,'user and tracker combination not found')
        return(s)
    @auth_required("token")
    @marshal_with(data_fields)
    def post(self,user,ID):
        s=User_Tracker.query.filter_by(user_id=user,ID=ID).first()
        if(s==None):
            raise NotFoundError(404,'user and tracker combination not found')
        args=data.parse_args()
        Description=args.get('Description')
        note=args.get('note')
        s=User_Tracker.query.filter_by(user_id=user,ID=ID).first()
        s1=Data(user_id=user,Tracker_ID=ID,usertrackers_count=s.Count,Time=datetime.now(),Description=Description,note=note)
        db.session.add(s1)
        db.session.commit()
        return(s1,201)
    @auth_required("token")
    @marshal_with(data_fields)
    def put(self,user,ID,Eno):
        s1=Data.query.get(Eno)
        if(s1==None):
            raise NotFoundError(404,'user and tracker combination not found')
        args=data.parse_args()
        Time=args.get('Time')
        Description=args.get('Description')
        note=args.get('note')
        s2=User_Tracker.query.filter_by(user_id=str(user),ID=ID).first()
        s1.user_id=user
        s1.Tracker_ID=ID
        s1.usertrackers_count=s2.Count
        if(Time!='False'):
            s1.Time=datetime.strptime(Time,"%Y-%m-%dT%H:%M")
        s1.Description=Description
        s1.note=note
        db.session.commit()
        return(s1,'201')
    @auth_required("token")
    @marshal_with(data_fields)
    def delete(self,Eno):
        s=Data.query.get(Eno)
        if(s==None):
            raise NotFoundError(404,'user and tracker combination not found')
        db.session.delete(s)
        db.session.commit()
        return(s)
api.add_resource(DataAPI,"/api/Data/<int:user>/<ID>","/api/Data/<int:Eno>","/api/Data/<int:user>/<ID>/<int:Eno>")

class getLoggedData():
    def get(self,user,ID,time):
        if(time.isnumeric()):
            date=datetime(datetime.today().year, datetime.today().month, datetime.today().day)-timedelta(days=int(time))
            s=Data.query.filter(Data.user_id==user,Data.Tracker_ID==ID,Data.Time>=date).all()
        else:
            s=Data.query.filter(Data.user_id==user,Data.Tracker_ID==ID).all()
        if(len(s)==0):
            raise NotFoundError(404,'user and tracker and date combination not found')
        return(s)
class LogAPI(Resource):
    @auth_required("token")
    @marshal_with(data_fields)
    def get(self,user,ID,time):
        return(getLoggedData().get(user,ID,time))
api.add_resource(LogAPI,"/api/Data/Range/<int:user>/<ID>/<time>")
class DailyLog():
    def get(self,user,ID,time,type):
        log=getLoggedData()
        json=log.get(user,ID,str(time))
        json.sort(key=lambda x:x.Time)
        l=[]
        c=0
        c1=0
        date=json[0].Time
        s=0
        s2=0
        while(c<len(json)):
            if(json[c].Time.date()!=date.date()):
                if(type=="Multiple-choice"):
                    l.append({"Date":date,"Description":(s-s2)/(c-c1)})
                else:
                    l.append({"Date":date,"Description":s-s2})
                s2=s
                c1=c
                date=json[c].Time
            s+=int(json[c].Description)
            c+=1
        if(type=="Multiple-choice"):
            l.append({"Date":date,"Description":(s-s2)/(c-c1)})
        else:
            l.append({"Date":date,"Description":s-s2})
        return(l)
data_fields={"Date":fields.DateTime,"Description":fields.Integer}        
class DailyLogAPI(Resource):
    def getdate(self,s):
        d=s.split()
        l=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        return(d[0]+'/'+str(l.index(d[1])+1)+'/'+d[2])

    @cache.memoize(10)
    @auth_required("token")
    @marshal_with(data_fields)
    def get(self,user,ID,time,type):
        return(DailyLog().get(user,ID,time,type))
api.add_resource(DailyLogAPI,"/api/Data/Daily/<int:user>/<ID>/<time>/<type>")
#only to be accessed by backend jobs
data_fields={"id":fields.Integer,"username":fields.String,"email":fields.String}
class UserAPI():
    @marshal_with(data_fields)
    def get(self,user):
        k= User.query.get(user)
        return(k)
class UsersAPI():
    @marshal_with(data_fields)
    def get(self):
        k= User.query.all()
        return(k)

class checkIfLogged():
    def get(self,user):
        latest=Data.query.filter(Data.user_id==user).all()
        if(len(latest)==0):
            return(False)
        latest=latest[-1].Time
        if(latest.date()==datetime.now().date()):
            return(True)
        else:
            return(False)
class UserDataSummaryAPI():
    def get(self,user):
        m=[31,28,31,30,31,30,31,31,30,31,30,31]
        DailyLogs=DailyLog()
        Trackers=TrackerAPI()
        month=datetime.today().month-1
        if(month==0):
            month=12
        trackers=User_Tracker.query.filter_by(user_id=user).all()  
        l1=[]
        l2=[]
        for x in trackers:
            i=Trackers.get(x.ID)
            if(i['TrackerType']=="Numerical"):
                try:
                    l=DailyLogs.get(user,x.ID,m[month-1],"Numerical")
                except:
                    continue
                td=Trackers.get(x.ID)
                d={}
                d['Name']=td["Name"]
                d['Days tracked']=str(len(l))+"/"+str(m[month-1])
                s=0
                for x in l:
                    s+=int(x['Description'])
                d['avg']=s/len(l)
                l1.append(d)
            elif(i['TrackerType']=="Multiple-choice"):
                d={}
                try:
                    l=DailyLogs.get(user,x.ID,m[month-1],"Multiple-choice")
                except:
                    continue
                if(len(l)==0):
                    continue
                td=Trackers.get(x.ID)
                d['Name']=td["Name"]
                d['Days tracked']=str(len(l))+"/"+str(m[month-1])
                s=0
                for x in l:
                    s+=int(x['Description'])
                d['avg']=round(s/len(l))
                d['avg']=td['Settings'].split(",")[d['avg']]
                l2.append(d)
        return(l1,l2)