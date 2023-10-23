from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
from foot_classifier import Foot_classifier
from MailSendSaver import message_send_saver
from email_validator import validate_email, EmailNotValidError

class Input_photo(BaseModel):
    photo: str

class Input_result(BaseModel):
    mail: str
    photo: str
    
app = FastAPI()

predictor=Foot_classifier()
ms=message_send_saver('Ortuga.SguMed@yandex.ru','pzsbymrrhvfujiwo')
database='database.csv'

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/mail")
async def send_mail(res:Input_result):
    print('--------------------------------------------------')
    try:
        #url_get=finder(apikey,dict(item)['listcity'],)
        print(dict(res))
        photo=dict(res)['photo']
        mail=dict(res)['mail']
        try:

          # Check that the email address is valid. Turn on check_deliverability
          # for first-time validations like on account creation pages (but not
          # login pages).
            emailinfo = validate_email(mail, check_deliverability=False)

          # After this point, use only the normalized form of the email address,
          # especially before going to a database query.
            email = emailinfo.normalized
            print(photo)
            print(mail)
            #print(url_get.__dict__)
            ms.save_mail(mail,database)
            ms.send_message(photo,mail)
            otvet='message sended,mail saved'
        except EmailNotValidError as e:
            print(str(e))
            otvet='EmailNotValidError' 
    except:
        otvet='somethingWrong'
    return otvet

@app.post("/makePrediction")
async def makePrediction(photo:Input_photo):
    print('--------------------------------------------------')
    try:
        #url_get=finder(apikey,dict(item)['listcity'],)
        photo=dict(photo)['photo']
        #print(photo)
        name='res.png'
        predictor.make_classification(photo,name)
        resp=name
        #print(url_get.__dict__)
    except Exception as e:
        print(e)
        resp='somethingWrong'
    return resp
