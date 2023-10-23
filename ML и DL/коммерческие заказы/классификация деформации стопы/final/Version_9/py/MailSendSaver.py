import pandas as pd
import hashlib
import smtplib                                      # Импортируем библиотеку по работе с SMTP

# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.image import MIMEImage              # Изображения
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class message_send_saver():
    def __init__(self,mail_from,password):
        self.mail_from=mail_from
        self.password=password
    def send_message(self,photo,mail_to):

        
        # от кого
        fromaddr = self.mail_from
        # кому
        toaddr = mail_to
        # пароль
        mypass = self.password

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "результаты исследования"
        body = "Результаты исследования"
        msg.attach(MIMEText(body, 'plain'))
        with open(photo, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename="res.png")
            msg.attach(img)
        # server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server = smtplib.SMTP('smtp.yandex.ru', 587)
        server.starttls()

        server.login(fromaddr, mypass)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    def save_mail(self,mail_to,mail_database):
        table=pd.read_csv(mail_database)
        cyMail=hashlib.md5(mail_to.encode())
        #if cyMail.hexdigest() not in list(table['hashedMail']):
        print('почта сохранена')
        file=os.listdir('collectedData')[-1]
        print(file)
        table.loc[ len(table.index )] = [cyMail.hexdigest(),'collectedData/'+file]

        print('почта сохранена')
        table.to_csv(mail_database,index=False)
