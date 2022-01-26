from datetime import datetime
import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

url = "https://niftygateway-data-scraper.p.rapidapi.com/artists"

headers = {
    'x-rapidapi-host': "niftygateway-data-scraper.p.rapidapi.com",
    'x-rapidapi-key': "a15c0774b1mshe2ce3b0c058fe35p17bfd2jsna8411acde685"
    }

res = requests.get(url, headers=headers).json().get('data')
df = pd.DataFrame(res)
# print(df)
# print(res)
df.to_excel('stock-price.xlsx', index=False)
# df.to_excel('inventory.xlsx', index=False, columns=['symbol', 'open', 'dayHigh', 'dayLow', 'lastPrice'])



def send_mail(send_to,subject,text,files,server,port,username='',password='',isTls=True):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = send_to    
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(files, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={datetime.now().strftime("%Y-%m-%d")+"-"+files}')
    msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if isTls:
        smtp.starttls()
    smtp.login(username,password)
    smtp.sendmail(username, send_to, msg.as_string())
    smtp.quit()
    

message = f'''

Data dari api kosong tanggal {datetime.now().strftime('%Y-%m-%d')}

'''

send_mail('sendTo', 'SubjectEmail', message, 'filename.xslx', 'smtp.gmail.com', 587, 'youremail', "yourpassword")