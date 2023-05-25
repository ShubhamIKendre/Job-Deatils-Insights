import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def sendmail(html_content,Sender,Receiver):
    # Sender = "sikendre@mitaoe.ac"
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Available Job opportunities from JobInsights"
    msg['From'] = Sender
    msg['To'] = Receiver

    # Create the body of the message (a plain-text and an HTML version).
    text = "List all available jobs:- "


    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)
    part2 = MIMEText(html_content, 'html')
     # Attach parts into message container.
    msg.attach(part2)

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("templates/Data/Job_data.csv", "rb").read())
    encoders.encode_base64(part)
        
    part.add_header('Content-Disposition', 'attachment; filename="Job_data.csv"')

    msg.attach(part)
   

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('sikendre@mitaoe.ac.in', 'ounvpzebbouzcyaq')
    mail.sendmail(Sender, Receiver, msg.as_string())
    mail.quit()
