from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from workers import celery
import smtplib
from jinja2 import Template
from weasyprint import HTML
from API import getLoggedData,UsersAPI,UserAPI,checkIfLogged,UserDataSummaryAPI 
import csv
from celery.schedules import crontab
#os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
HTML('https://weasyprint.org/').write_pdf('weasyprint-website.pdf')

SENDER="trackerBackend@email.com"
celery.conf.enable_utc = False
celery.conf.timezone = 'Asia/Calcutta'

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, send_reminder.s(), name='sending daily reminder')
    sender.add_periodic_task(10,create_pdf.s(),"monthly_report_sent")

def send_mail(to,subject,message,attachment=None):
    mes=MIMEMultipart()
    mes["From"]="emails@trackers.com"
    mes["To"]=to
    mes["Subject"]=subject
    mes.attach(MIMEText(message,"html"))
    if attachment:
        with open(attachment,'rb') as attach:
            part=MIMEBase("application","octet-stream")
            part.set_payload(attach.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",f"attachment;filename={attachment}")
        mes.attach(part)
    s=smtplib.SMTP(host="localhost",port=1025)
    s.login(SENDER,"")
    s.send_message(mes) 
    s.quit()

def make_pdf(data,report):
    with open(report,'r') as file:
        temp=Template(file.read()).render(data=data)
        html=HTML(string=temp)
        file="Monthly_report.pdf"
        html.write_pdf(target="./Reports/"+file)
    return(file)


@celery.task
def make_csv(user_id,trackerID):
    user=UserAPI().get(user_id)
    try:
        obj1=getLoggedData()
        data=obj1.get(user_id,trackerID,"a")
        data1=[]
        for items in data:
            datas={}
            datas['Date-time']=items.Time.strftime("%d/%m/%Y, %H:%M:%S")
            datas['Log']=items.note
            datas['Description']=items.Description
            data1.append(datas)
        with open('./Reports/Tracker.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = ["Date-time","Description","Log"])
            writer.writeheader()
            writer.writerows(data1)
        send_mail(user['email'],"CSV attachment","find the csv attachment below","./Reports/Tracker.csv")
    except:
        send_mail(user['email'],"No data for Tracker","We found no data for tracker, log some values to generate a csv")

@celery.task
def send_reminder():
    usersapi=UsersAPI()
    users=usersapi.get()
    for user in users:
        flag=checkIfLogged().get(user['id'])
        if(not flag):
            with open("./templates/reminder.html") as file:
                template=Template(file.read())
                message=template.render(username=user['username'])
            send_mail(user['email'],"Reminder to Log your Progress",message)

@celery.task
def create_pdf():
    users=UsersAPI().get()
    summ=UserDataSummaryAPI()
    for user in users:
        data=summ.get(user["id"])
        if(len(data[0])==0 and len(data[1])==0):
            continue
        file=make_pdf(data,"./templates/report.html")
        send_mail(user['email'],"Monthly Report","<p>Below attached is the pdf of your monthly rerport</p>","./Reports/"+file)
    print("sent pdf")



    



