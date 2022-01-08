import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import from_email, password




def sendSMTP(mess):        
    msg = MIMEMultipart()

    to_email = 'dax0068@gmail.com'
    message = mess

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()